#!/usr/bin/env bash

echo 'Getting archive signing key'
export GPGTMP=$(mktemp -d /tmp/.gnupgXXXXXX)

gpg --homedir $GPGTMP --keyserver hkp://keyserver.ubuntu.com --recv-key 3cb9fd148f374fef
gpg --homedir $GPGTMP --export 'EMC Archive Signing Key' | tee /usr/share/keyrings/linuxcnc.gpg > /dev/null

echo 'deleting temp files'
rm -rf $GPGTMP

echo 'Updating apt repository list'
echo deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/linuxcnc.gpg] http://www.linuxcnc.org/ bookworm base 2.9-uspace 2.9-rt |  tee /etc/apt/sources.list.d/linuxcnc.list > /dev/null

echo deb-src [arch=amd64,arm64 signed-by=/usr/share/keyrings/linuxcnc.gpg] http://www.linuxcnc.org/ bookworm base 2.9-uspace 2.9-rt |  tee -a /etc/apt/sources.list.d/linuxcnc.list > /dev/null

echo 'Updating APT index'
apt -qq update

apt -y dist-upgrade
