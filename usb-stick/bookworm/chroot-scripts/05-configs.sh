#!/usr/bin/env bash

sed -i "s|^#\?.*AutomaticLoginEnable.*|AutomaticLoginEnable = true|" /etc/gdm3/daemon.conf
sed -i "s|^#\?.*AutomaticLogin .*=.*|AutomaticLogin = linuxcnc\nTimedLoginEnable = true\nTimedLogin = linuxcnc\nTimedLoginDelay = 0|" /etc/gdm3/daemon.conf

#rm -f /etc/ssh/*key*
#sed -e '$i \ntest -f /etc/ssh/ssh_host_dsa_key || dpkg-reconfigure openssh-server\n' /etc/rc.local

echo "127.0.1.1 linuxcnc" >> /etc/hosts

# http://unix.stackexchange.com/questions/111081/can-i-set-appearance-for-gnome-debian
#sed -i "/title_vertical_pad/s/value=\"[0-9]\{1,2\}\"/value=\"0\"/g" \
#    /usr/share/themes/Adwaita/metacity-1/metacity-theme-3.xml

gsettings set org.gnome.desktop.wm.preferences titlebar-font 'Cantarell Bold 8'
gsettings set org.gnome.desktop.background show-desktop-icons true
gsettings set org.gnome.nautilus.desktop volumes-visible true
