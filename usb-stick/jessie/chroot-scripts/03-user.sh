#!/usr/bin/env bash

adduser --disabled-password --gecos "" machinekit
usermod -aG  sudo,xenomai,kmem,netdev,plugdev machinekit

touch /root/.hushlogin
touch /home/machinekit/.hushlogin

echo "machinekit:mk" | chpasswd
