#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

apt -qqq -y install network-manager net-tools firmware-iwlwifi
apt -qqq -y install sudo console-setup
apt -qqq -y install linux-image-rt-amd64 linux-headers-rt-amd64
apt -qqq -y install linuxcnc linuxcnc-dev
apt -qqq -y install ethercat-master linuxcnc-ethercat
#apt -qqq -y install jstest-gtk joystick
apt -qqq -y install lightdm xfce4 xfdesktop4 xfce4-goodies xfce4-power-manager xfce4-session xfce4-terminal
apt -qqq -y install emacs-nox vim vim-scripts screen mutt chromium htop
