#!/usr/bin/env bash

apt -y remove --purge linux-image-amd64
apt -y --purge autoremove
apt autoclean
