#!/usr/bin/env bash

sed -i 's/XKBLAYOUT=\"us\"/XKBLAYOUT=\"de\"/g' /etc/default/keyboard
sed -i 's/XKBOPTIONS=\"\"/XKBOPTIONS=\"terminate:ctrl_alt_bksp\"/g' /etc/default/keyboard
