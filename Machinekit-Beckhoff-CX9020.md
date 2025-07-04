# Machinekit on Beckhoff CX9020 with Debian Jessie

This guide details the setup of [Machinekit](http://www.machinekit.io/) on a [Beckhoff CX9020](http://www.beckhoff.de/english.asp?embedded_pc/cx9020.htm) Embedded PC using a custom Debian Jessie image with a real-time kernel.

**⚠️ Legacy System Warning:** This guide was written in 2016 and targets older software versions, including Debian Jessie and Ubuntu 14.04 for the build environment. These are no longer maintained. This document is preserved for historical and reference purposes.

### Overview

The Beckhoff CX9020 is a DIN rail-mountable embedded system ideal for industrial control applications. To run a custom Linux distribution, the **CX9020-0100** variant is required, as it is configured to boot from a microSD card.

#### Key Specifications

*   **CPU:** 1 GHz ARM Cortex™-A8
*   **Flash Memory:** 512 MB microSD (expandable via two slots)
*   **RAM:** 1 GB DDR3 (non-expandable)
*   **Persistent Memory:** 128 KB NOVRAM
*   **Networking:** 2 x RJ45 10/100 Mbit/s
*   **Display:** 1 x DVI-D
*   **Connectivity:** 4 x USB 2.0
*   **Expansion:** 1 x optional interface slot

*   **Photo Gallery:** [Hardware Photos](https://goo.gl/photos/kc86sjNKajbgcdEr7)

---

### 1. Building the RT-PREEMPT Kernel and Debian Rootfs

The build process relies on scripts and patches from Beckhoff, which are designed for an **Ubuntu 14.04 LTS** build environment. Using a newer OS may cause issues (e.g., with `sfdisk`).

#### 1.1. Build Environment Setup

On a 64-bit Ubuntu 14.04 LTS system, prepare the necessary tools:

```bash
# Enable i386 architecture for multi-arch support
sudo dpkg --add-architecture i386
sudo apt-get update

# Install build dependencies
sudo apt-get install -y \
    multistrap qemu binfmt-support qemu-user-static \
    mercurial libtool autoconf lib32z1 lib32ncurses5-dev \
    lib32stdc++6 git make xz-utils bc wget

# Apply a fix for a multistrap bug in Ubuntu 14.04
sudo sed -i "s/\$forceyes //" /usr/sbin/multistrap
```

#### 1.2. Build Process

Follow the instructions provided by the [Beckhoff/CX9020 GitHub repository](https://github.com/Beckhoff/CX9020).

```bash
# Clone the repository
git clone https://github.com/Beckhoff/CX9020
cd CX9020

# Install the Linaro toolchain
./tools/install_linaro_gcc.sh

# Prepare and build U-Boot
./tools/prepare_uboot.sh v2015.07
make uboot

# Prepare and build the RT-PREEMPT kernel
./tools/prepare_kernel.sh 4.1 12 13
make kernel

# (Optional) Prepare and build the EtherLab master
./tools/prepare_etherlab.sh
make etherlab
```

#### 1.3. Create the SD Card Image

This step writes the Debian rootfs and kernel to a microSD card.

**⚠️ DANGER:** Be absolutely certain that you specify the correct device name for your SD card reader (e.g., `/dev/sdc`). Using the wrong device name **will destroy data** on your host system.

```bash
# Write the base system to the microSD card
sudo ./scripts/install.sh /dev/sdc

# (Optional) Install EtherLab to the rootfs
sudo ./scripts/52_install_etherlab.sh /tmp/rootfs
```

You now have a bootable microSD card with Linux 4.1.12-rt13 and Debian Jessie.

#### 1.4. Backup the Image (Recommended)

Create a backup of the freshly created image for easy restoration.

```bash
# Create a backup image file
sudo dd if=/dev/sdc of=CX9020-debian-jessie.img bs=4M status=progress
```

---

### 2. First Boot and System Configuration

Insert the microSD card into the primary slot of the CX9020 and power it on. The power LED should turn from yellow to green after a few seconds. The system draws approximately 0.16A at 24.0V.

![CX9020 Running Linux](pics/koppi-cnc-cx9020.jpg)

The first Ethernet port (`eth0`) is configured for DHCP, while the second has a static IP. See the [default network configuration](https://github.com/Beckhoff/CX9020/blob/master/tools/eth0.cfg) for details.

#### 2.1. SSH Access

For security, set up public key authentication.

1.  **On the CX9020:** Add your SSH public key to `/root/.ssh/authorized_keys`.
2.  **On your client machine:** Configure your `~/.ssh/config` for easy access:

    ```
    Host cx9020
      Hostname cx9020.local
      User root
      IdentitiesOnly yes
      IdentityFile ~/.ssh/id_rsa
    ```

Now you can connect with `ssh cx9020`.

#### 2.2. System Information

After logging in, you can inspect the system:

*   **Kernel Version:** `uname -a`
    ```
    Linux CX9020 4.1.12-rt13-CX9020-9+ #1 PREEMPT RT Fri Apr 29 01:09:47 CEST 2016 armv7l GNU/Linux
    ```
*   **CPU Info:** `cat /proc/cpuinfo`
*   **Memory:** `cat /proc/meminfo`
*   **Hardware:** `lshw -short`
*   **Loaded Modules:** `lsmod`

---

### 3. Using a Larger microSD Card

The default 512 MB card is small. To expand storage:

1.  Purchase a larger, high-quality microSD card (industrial grade is recommended).
2.  Write your backup image to the new card:
    ```bash
    sudo dd if=CX9020-debian-jessie.img of=/dev/sdX # Replace sdX with your card device
    ```
3.  Resize the root partition using `gparted /dev/sdX` to utilize the full capacity of the card.
4.  Install additional development tools on the CX9020:
    ```bash
    apt install htop wget screen vim git devscripts
    ```

To reduce wear on the flash storage, enable the `lazytime` mount option in `/etc/fstab`:

```diff
- /dev/mmcblk0p1        /       auto             errors=remount-ro       0       1
+ /dev/mmcblk0p1        /       auto    lazytime,errors=remount-ro       0       1
```

---

### 4. Real-Time Performance Benchmark

Use `cyclictest` to measure the real-time performance of the kernel.

1.  **Install dependencies:**
    ```bash
    apt install gnuplot libnuma-dev
    ```
2.  **Build `rt-tests`:**
    ```bash
    git clone git://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git
    cd rt-tests
    make all
    sudo cp ./cyclictest /usr/bin/
    ```
3.  **Run the test:**
    A quick test should show low latency:
    ```bash
    # cyclictest -t1 -p 80 -n -i 10000 -l 10000
    # /dev/cpu_dma_latency set to 0us
    policy: fifo: loadavg: 0.01 0.04 0.26 1/87 25906
    T: 0 (25906) P:80 I:10000 C:  10000 Min:     37 Act:   45 Avg:   47 Max:      70
    ```
    For a detailed histogram:
    ```bash
    time cyclictest -n -q -p 99 -a -t -D 1000 -i 250 -h 2000 -m > cyclictest-$(uname -r).plt
    ```
    This will generate a data file that can be plotted.

    ![Cyclictest Histogram](pics/cx9020-cyclictest-4.1.12-rt13-CX9020-9+.png)

    For comparison, see the [RT-Wiki Cyclictest page](https://rt.wiki.kernel.org/index.php/Cyclictest).

---

### 5. Machinekit Setup

You can install Machinekit from the official Debian repository or compile it from source.

*   **Packages:** http://deb.machinekit.io/debian/dists/jessie/
*   **Source:** https://github.com/machinekit/machinekit

The CNC configuration files for this setup are available in the `cx9020` branch of this repository: [koppi/mk/linuxcnc/configs/koppi-cnc](https://github.com/koppi/mk/tree/cx9020/linuxcnc/configs/koppi-cnc).

A `systemd` service script, `systemd-register.py`, is included to automatically start `mklauncher` on boot. Once running, you can connect to the CX9020 using a Machinekit client (e.g., Cetus) to control the CNC.

---

### Changelog

*   **2016-05-27:** [Video](https://www.youtube.com/watch?v=Xs5yllN3u6Q) of `siggen` HAL component test.
*   **2016-05-03:** Status update on `machinekit-rt-preempt` armhf package ([Issue #928](https://github.com/machinekit/machinekit/issues/928)).
*   **2016-05-02:** Initial tests with Machinekit.
*   **2016-05-01:** Benchmarked with `cyclictest` on a 64 GB microSD card.
*   **2016-04-30:** First successful boot of Debian Jessie.

### Contact

For questions, feel free to join the Gitter chat: [![Gitter](https://badges.gitter.im/koppi/mk.svg)](https://gitter.im/koppi/mk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)