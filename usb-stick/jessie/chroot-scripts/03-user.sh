#!/usr/bin/env bash

adduser --disabled-password --gecos "" machinekit
usermod -aG  sudo,xenomai,kmem,netdev,plugdev machinekit

touch /root/.hushlogin
touch /home/machinekit/.hushlogin

echo -e "# No sudo password for machinekit user\nmachinekit ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/90-machinekit

echo "machinekit:mk" | chpasswd
