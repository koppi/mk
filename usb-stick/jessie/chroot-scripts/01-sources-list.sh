#!/usr/bin/env bash

echo 'deb http://deb.dovetail-automata.com jessie main' > \
     /etc/apt/sources.list.d/machinekit.list;

apt-get update && apt-get --yes --force-yes install dovetail-automata-keyring
apt-get update
