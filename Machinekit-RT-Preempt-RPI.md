# Machinekit with RT-Preempt Kernel on Raspberry Pi

## Overview

This guide details the steps to set up a Machinekit installation with an EtherCAT master on a Raspberry Pi (3B, 4B, or newer) using a real-time (RT-Preempt) patched Linux kernel.

The main steps are:
1.  Install Raspberry Pi OS.
2.  Build and install a real-time Linux kernel.
3.  Install the IgH EtherCAT master.
4.  Set up Machinekit.
5.  Configure and test the system.

---

### 1. Install Raspberry Pi OS

Start by installing the latest version of Raspberry Pi OS on a microSD card. Use the official Raspberry Pi Imager for an easy installation. A "Lite" version is sufficient if you plan to run the Pi headless.

*   [Raspberry Pi OS download page](https://www.raspberrypi.com/software/)
*   [Raspberry Pi Imager](https://www.raspberrypi.com/software/)

After installation, boot the Raspberry Pi, connect it to the network, and ensure you can access it via SSH.

---

### 2. Build and Install an RT-Preempt Linux Kernel

#### 2.1. Download Kernel Sources

First, install the necessary tools for kernel building.

```bash
sudo apt update
sudo apt -y install git bc bison flex libssl-dev libncurses-dev
```

Next, download the Raspberry Pi kernel sources. We'll use a specific long-term support (LTS) branch. As of this writing, `rpi-6.1.y` is a good choice.

```bash
cd /usr/src
# Check for the latest stable branch on the repository page if needed
git clone -b 'rpi-6.1.y' --single-branch --depth 1 https://github.com/raspberrypi/linux.git
```

#### 2.2. Patch Kernel with RT-Preempt Patch

Download the corresponding RT-Preempt patch for your kernel version. You can find the kernel version in the `Makefile`.

```bash
cd /usr/src/linux
KERNEL_VERSION=$(make kernelversion)
echo "Kernel version is ${KERNEL_VERSION}"
```

Find the matching patch on the official kernel.org site. For example, for kernel `6.1.x`, you would look in the `6.1` folder.

```bash
# Example for a 6.1.x kernel. Adjust the version if necessary.
wget https://www.kernel.org/pub/linux/kernel/projects/rt/6.1/patch-6.1.55-rt15.patch.gz
zcat patch-6.1.55-rt15.patch.gz | patch -p1
```

Check for any rejected patch parts, which would indicate an incompatibility.
```bash
find -iname "*.rej"
```
If you find any `.rej` files, you might need a different patch version or a different kernel source branch.

#### 2.3. Configure the Kernel

For a Raspberry Pi 4 or newer (64-bit):
```bash
export KERNEL=kernel8
make bcm2711_defconfig
```

For a Raspberry Pi 3 (32-bit):
```bash
export KERNEL=kernel7
make bcm2709_defconfig
```

Now, launch the kernel configuration menu to enable the real-time preemption.

```bash
make menuconfig
```

In the configuration menu, make the following changes:

*   **Enable Full Real-Time Preemption:**
    > Kernel Features → Preemption Model → Fully Preemptible Kernel (RT)

    ![Kernel Config RT Preempt](pics/kernel-config-rt-preempt-01.png)

*   **Ensure High-Resolution Timers are enabled** (usually enabled by default):
    > General setup → Timers subsystem → High Resolution Timer Support

    ![Kernel Config High-Res Timers](pics/kernel-config-rt-preempt-02.png)

Save the configuration and exit `menuconfig`.

#### 2.4. Build and Install the Kernel

Now, build the kernel, modules, and device tree blobs. This will take a long time on a Raspberry Pi.

```bash
make -j$(nproc)
sudo make modules_install
```

Finally, install the new kernel and device tree files to the `/boot` directory.

```bash
# For RPi 4 or newer
sudo cp -v arch/arm64/boot/dts/broadcom/*.dtb /boot/
sudo cp -v arch/arm64/boot/Image /boot/$KERNEL.img

# For RPi 3
# sudo cp -v arch/arm/boot/dts/*.dtb /boot/
# sudo cp -v arch/arm/boot/zImage /boot/$KERNEL.img

sudo systemctl reboot
```

After rebooting, verify that the new kernel is running. The kernel name should contain `PREEMPT_RT`.

```bash
uname -a
```

---

### 3. Build and Install IgH EtherCAT Master

The IgH EtherCAT master can be installed from Debian packages, which is much simpler than building from source.

```bash
sudo apt install ethercat-master
```

After installation, configure the master by editing the configuration file:

```bash
sudo nano /etc/ethercat.conf
```

Set the `MASTER0_DEVICE` to the MAC address of your Ethernet port and specify the driver.

```
MASTER0_DEVICE="b8:27:XX:XX:XX:XX" # Find your MAC with `ip a`
DEVICE_MODULES="generic"
```

Then, start and enable the EtherCAT master service:

```bash
sudo systemctl start ethercat.service
sudo systemctl enable ethercat.service
```

Check the status to ensure it's running correctly:

```bash
sudo systemctl status ethercat.service
ethercat slaves
```

The `ethercat slaves` command should list all connected and powered EtherCAT slaves.

---

### 4. Setup Machinekit

Install Machinekit from the official repositories. Follow the instructions on the Machinekit website.

*   [Machinekit Download Page](http://www.machinekit.io/docs/getting-started/)

A typical installation looks like this:

```bash
sudo apt install -y lsb-release
sudo sh -c \
  'echo "deb http://deb.machinekit.io/debian $(lsb_release -sc) main" > \
  /etc/apt/sources.list.d/machinekit.list'
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 43DDF224
sudo apt-get update
sudo apt-get install -y machinekit-posix
```
*Note: `machinekit-posix` is for simulation and non-realtime use. For a real-time setup, you would typically install `machinekit-rt-preempt`.*

---

### 5. Latency Evaluation

To check the real-time performance of your system, you can use `cyclictest`.

```bash
sudo apt install -y rt-tests
sudo cyclictest -t1 -p 80 -n -i 10000 -l 100000
```

This will show you the minimum, average, and maximum latencies. The maximum latency is the most important value for determining a safe servo thread period for Machinekit. For a 1ms (1000µs) cycle time, the maximum latency should stay well below that, ideally under 100-150µs under full system load.

---

### Changelog

*   2023-10-27: Complete rewrite for modern Raspberry Pi OS and kernel.
*   2016-06-16: Add info about Machinekit setup.
*   2016-05-30: Initial version.