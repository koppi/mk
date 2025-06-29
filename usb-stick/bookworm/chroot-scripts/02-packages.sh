#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

# apt -y install firmware-iwlwifi
apt -y install console-setup
apt -y install linux-image-rt-amd64

apt -y install linuxcnc-doc-en
apt -y install linuxcnc-uspace
apt -y install linuxcnc-dev

apt -y install ntp
apt -y install jstest-gtk joystick
apt -y install gedit

#apt install aptitude tasksel
#tasksel install gnome-desktop --new-install
#aptitude -q --without-recommends -o APT::Install-Recommends=no -y install ~t^desktop$ ~t^gnome-desktop$
apt -y install gnome-core
#apt -y install gnome

#aptitude install gnome-desktop
#apt -y install gnome
#apt -y install lightdm
#/usr/lib/x86_64-linux-gnu/lightdm/lightdm-set-defaults -s gnome-fallback
#/usr/lib/x86_64-linux-gnu/lightdm/lightdm-set-defaults --autologin linuxcnc

apt -y install emacs-nox vim vim-scripts screen

apt -y autoclean
