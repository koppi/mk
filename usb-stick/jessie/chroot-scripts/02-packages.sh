#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

apt-get -y install firmware-linux-nonfree firmware-iwlwifi console-setup
apt-get -y install linux-image-xenomai.x86-amd64 linux-headers-xenomai.x86-amd64
apt-get -y install machinekit machinekit-dev machinekit-xenomai machinekit-posix

apt-get -y autoclean

apt-get -y install libczmq-dev python-zmq libjansson-dev libwebsockets-dev libxenomai-dev python-pyftpdlib cython
#apt-get -y install linux-tools-3.8 # for perf

apt-get -y autoclean

apt-get -y install ntp
apt-get -y install jstest-gtk joystick
apt-get -y install gedit

#apt-get install aptitude tasksel
#tasksel install gnome-desktop --new-install
#aptitude -q --without-recommends -o APT::Install-Recommends=no -y install ~t^desktop$ ~t^gnome-desktop$
apt-get -y install gnome-core
#apt-get -y install gnome

apt-get -y autoclean

#aptitude install gnome-desktop
#apt-get -y install gnome
apt-get -y install lightdm
#/usr/lib/x86_64-linux-gnu/lightdm/lightdm-set-defaults -s gnome-fallback
#/usr/lib/x86_64-linux-gnu/lightdm/lightdm-set-defaults --autologin machinekit

apt-get -y install wicd-curses vim vim-scripts screen
apt-get -y -f install

apt-get -y insall vlc-nox

apt-get -y autoclean
