#!/usr/bin/env bash

adduser --disabled-password --gecos "" linuxcnc
usermod -aG  sudo,kmem,netdev,plugdev linuxcnc

touch /root/.hushlogin
touch /home/linuxcnc/.hushlogin

echo -e "# No sudo password for linuxcnc user\nlinuxcnc ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/90-linuxcnc

echo "linuxcnc:1234" | chpasswd
