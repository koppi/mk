[Machinekit](http://www.machinekit.io/) + [Debian/Jessie](https://www.debian.org/releases/jessie/) on [Beckhoff CX9020](http://www.beckhoff.de/english.asp?embedded_pc/cx9020.htm).
 
### Overview

The CX9020 comes in different configurations, to get Linux running, you need to order the variant CX9020-0100, which is pre-configured to boot directly from the microSD card instead of using the internal bootloader. This variant is therefore suitable for operating systems with bootloaders on microSD cards (like Linux).

#### Specs

The CX9020 is a DIN rail-mountable embedded system
*   1 GHz ARM Cortex™-A8 CPU
* 512 MB microSD  (optionally expandable) flash memory, 2 microSD card slots
*   1 GB DDR3 RAM (non expandable) internal main memory
* 128 KB NOVRAM   (integrated) persistent memory
* 2 x RJ45 10/100 Mbit/s
* 1 x DVI-D
* 4 x USB 2.0
* 1 x optional interface

* Photos: [Hardware](https://goo.gl/photos/585GqHfQPs7fCpV87)

### Cross-compile RT-PREEMPT Linux kernel and setup a Debian/Jessie rootfs

Beckhoff has published shell scripts and patches at [github.com/Beckhoff/CX9020](https://github.com/Beckhoff/CX9020) to build a basic Linux system image. As of 2016-05-01 the scripts require an Ubuntu 14.04 LTS installation. I've tried the installation on an Ubuntu 16.04 installation and ran into a small problem with sfdisk. So for now, the Ubuntu 14.04 LTS installation is the recommended way of building the system image.

The system image build process requires about 2.65 GB hdd space available on the build system. Follow the instructions at [github.com/Beckhoff/CX9020](https://github.com/Beckhoff/CX9020):
```bash
# prepare your machine f.e.: 64-bit Ubuntu 14.04 LTS would require
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y multistrap qemu binfmt-support qemu-user-static mercurial libtool autoconf lib32z1 lib32ncurses5-dev lib32stdc++6 git make xz-utils bc wget

# fix multistrap bug in Ubuntu 14.04
sudo sed -i "s/\$forceyes //" /usr/sbin/multistrap

git clone https://github.com/Beckhoff/CX9020
cd CX9020
./tools/install_linaro_gcc.sh

# get and patch the u-boot sources
./tools/prepare_uboot.sh v2015.07

# build u-boot
make uboot

# get and patch a rt kernel
./tools/prepare_kernel.sh 4.1 12 13

# configure and build the kernel
make kernel

# get and patch etherlab (optional)
./tools/prepare_etherlab.sh

# configure and build the etherlab (optional)
make etherlab

# prepare sdcard with a small debian rootfs
#
# BE CAREFUL to specify the correct device name,
# or you might end up deleting your host's root partition!
./scripts/install.sh /dev/sdc

# install etherlab (optional)
./scripts/52_install_etherlab.sh /tmp/rootfs
```
You now have a Linux 4.1.12-rt13 + Debian/Jessie base system image.

Make a backup of the system image (optional, but recommended):
```bash
sudo dd if=/dev/sdc of=CX9020.img
```

Insert the microSD card into the first microSD card slot of the CX9020. Power on the system, the red power led turns yellow, and after about 2 secs, the power led should turn green:
![pics/koppi-cnc-cx9020.jpg](pics/koppi-cnc-cx9020.jpg)
My power supply's readouts: 24.0V / 0.16A.

The first  ethernet interface is pre-configured with a DHCP client.
The second ethernet interface is pre-configured with a static IP.
See: https://github.com/Beckhoff/CX9020/blob/master/tools/eth0.cfg

WIP

### Setup Machinekit

WIP

### ChangeLog

* 2016-04-30 – First steps at running Debian/Jessie.

### Contact

If you have any questions about the setup process feel free to join the [![Gitter](https://badges.gitter.im/koppi/mk.svg)](https://gitter.im/koppi/mk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge).
