#!/usr/bin/env bash

rm -f /etc/apt/apt.conf.d/01proxy

apt-get -y remove --purge postfix

apt-get autoclean
