# Machinekit auf Thinkpad X200

Übersicht Steuerung:
![Übersicht Steuerung](pics/IMG_20150515_172113.jpg)
 1. IBM Thinkpad X200 mit Debian Wheezy / Linux 3.8.1 / Machinekit 0.1 / Xenomai 2.6.3
 2. 24VDC 50W Netzteil
 3. Beckhoff EtherCAT Komponenten
 4. 24V-380V 40A 250V SSR-40 DA Solid State Relay Modul 3-32V
 5. Stromversorgung Kress / Staubsauger

Übersicht Steuerungselektronik:
![Übersicht Steuerungselektronik](pics/IMG_20150515_172220.jpg)
 1. Stromversorgung 24V von Netzteil
 2. Ethernet-Kabel vom Thinkpad zum EK1100 (EtherCAT-Koppler)
 3. Ausgang 1 vom EL2004 zum Solid State Relay Modul
 4. Eingang 1 vom EL1004 zum Not-Aus Schalter
 5. Eingang 2 vom EL1004 zum Tastkopf
 6. 24V Versorgung von Verteilerklemme EL9184 zur Bus-Klemme EL9100
 7. 24V Versorgung Schrittmotorendstufen EL7041-1000
 8. Ausgänge Schrittmotoren

Übersicht Fräsmaschine:
![Übersicht Fräsmaschine](pics/IMG_20150515_172548.jpg)
 1. Kleine CNC Fräsmaschine Portal 210 x 230 x 70 - [www.flohmarkt4u.de](http://www.flohmarkt4u.de/)
 2. Nema23 Stepper Motor 57BYGH627 - Wantai
 3. Kress 1050 FME-1 Fräsmotor - EAN: 4000649061895
 4. Red Sign Emergency Stop Push Button - eBay
 5. Eingang Tastkopf für Werkzeuglängensensor
 6. OBI LUX Maschinen Schraubstock 60x65mm - EAN: 4007871165254

# Installation Machinekit / LinuxCNC

### Thinkpad X200 BIOS Einstellungen

BIOS auf Werkseinstellungen zurücksetzen:

![Thinpad X200 BIOS reset](pics/2015-05-04 19.00.51.jpg)

## Installation Debian Wheezy

```bash
$ md5sum debian-live-7.8.0-i386-gnome-desktop+nonfree.iso
0e9a2b9561d7380ff3015c8f81d9f1e2  debian-live-7.8.0-i386-gnome-desktop+nonfree.iso
```

ISO auf USB-Stick kopieren:

```bash
$ sudo dd if=debian-live-7.8.0-i386-gnome-desktop+nonfree.iso of=/dev/sdX
```

Debian installieren und Rechner neu starten.

Im Thinkpad BIOS "Legacy USB" deaktivieren:

![Thinpad X200 BIOS – Legacy USB](pics/2015-05-14 01.18.55.jpg)

### Konfiguration WLAN

```/etc/network/interfaces``` anpassen:

```ini
auto wlan0
allow-hotplug wlan0
iface wlan0 inet static
  address 192.168.0.3
  netmask 255.255.255.0
  gateway 192.168.0.1
  wpa-ssid "SSID"
  wpa-psk "PASSWORT"
```

```bash
$ sudo ifup wlan0
$ /sbin/ifconfig wlan0
```

### Gnome Classic ohne Effekte mit LightDM

```bash
$ sudo aptitude install gnome-desktop
$ sudo apt-get -y install lightdm
$ sudo /usr/lib/x86_64-linux-gnu/lightdm/lightdm-set-defaults -s gnome-fallback
```

### Konfiguration sudo

sudo ohne Passwort:

```bash
$ su -
# visudo
```

Zeile anpassen:

```
%sudo   ALL=(ALL:ALL) ALL
```
in
```
%sudo   ALL=(ALL:ALL) NOPASSWD: ALL
```

Benutzer koppi" in Gruppe "sudo" aufnehmen:

```bash
$ su -
# usermod -aG sudo koppi
```

Danach Aus- und wieder Einloggen, damit Eintragung wirksam wird.

### Konfiguration SSHD

SSH Logins beschleunigen:

```bash
$ sudo su -c 'echo -e "UseDNS no" >> /etc/ssh/sshd_config
```

Keine Meldungen bei SSH-Login:

```bash
$ touch .hushlogin
```

## Installation Linux / Xenomai / Machinekit

Wir verwenden die Varianten Machinekit-Xenomai und -Posix.

Wie in http://www.machinekit.io/docs/packages-debian/ vorgehen.

Paketmanager konfigurieren:

```bash
$ sudo sh -c \
    "echo 'deb http://deb.dovetail-automata.com wheezy main' > \
	    /etc/apt/sources.list.d/machinekit.list; \
	    apt-get update ; \
	    apt-get install dovetail-automata-keyring"
$ sudo apt-get update
```

Machinekit Pakete installieren:

```bash
$ sudo apt-get install linux-image-xenomai.x86-amd64
$ sudo apt-get install linux-headers-xenomai.x86-amd64
$ sudo apt-get install machinekit-xenomai
$ sudo apt-get install machinekit-posix # non-RT ('Simulator')
```

### Konfiguration Linux / Xenomai

Anpassung der Kernel-Parameter in ```/etc/default/grub```

```ini
#GRUB_CMDLINE_LINUX_DEFAULT="quiet"
GRUB_CMDLINE_LINUX_DEFAULT="quiet xeno_hal.smi=1 lapic=notscdeadline hpet=disable i915.i915_enable_rc6=0 i915.powersave=0 intel_idle.max_cstate=1 processor.max_cstate=1 isolcpus=1 idle=poll"
```

Bootloader neu konfigurieren und neustarten:

```bash
$ sudo update-grub
$ sudo reboot
```

Nach Neustart:

```bash
$ uname -a
Linux x200 3.8-1-xenomai.x86-amd64 #1 SMP Debian 3.8.13-9 x86_64 GNU/Linux
```

Deaktivierung von SMI prüfen:

```bash
$ dmesg|grep Xeno
 I-pipe: head domain Xenomai registered.
 Xenomai: hal/x86_64 started.
 Xenomai: scheduling class idle registered.
 Xenomai: scheduling class rt registered.
 Xenomai: real-time nucleus v2.6.3 (Lies and Truths) loaded.
 Xenomai: debug mode enabled.
 Xenomai: SMI-enabled chipset found
 Xenomai: SMI workaround enabled
 Xenomai: starting native API services.
 Xenomai: starting POSIX services.
 Xenomai: starting RTDM services.
```

### Konfiguration Xenomai

Xenomai Latenzzeit-Test (– Dauer 10 Minuten, bei Möglichkeit >= 24h laufen lassen):

```bash
$ sudo sh -c 'echo 0 > /proc/xenomai/latency'
$ timeout 6000 xeno latency
```

Nach 10 Minuten "lat min" notieren und folgendes Init-Script anlegen, Variable LATENCY unten anpassen ("lat min" * 1000):

```bash
$ cat /etc/init.d/xenomai-latency 
#!/bin/sh -e
### BEGIN INIT INFO
# Provides:          xenomai-latency
# Required-Start:    xenomai
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Set /proc/xenomai/latency value
### END INIT INFO

INITNAME=/etc/init.d/xenomai-latency
FILENAME=/proc/xenomai/latency
LATENCY=830

test -e $FILENAME || exit 0

case "$1" in
  start)
        echo "$LATENCY" > $FILENAME
        ;;
  stop)
        ;;
  restart|force-reload)
        $0 start
        ;;
  *)
        echo "Usage: $INITNAME {start|stop|restart|force-reload}"
        exit 1
        ;;
esac

exit 0

```

Init-Script aktivieren:

```bash
$ sudo update-rc.d xenomai-latency defaults
```

## Konfiguration Machinekit

Benutzer in die Gruppen "xenomai" und "kmem" aufnehmen:

```bash
$ sudo usermod -aG xenomai,kmem koppi
```

Machinekit Latenzzeit Test:

```bash
$ latency-test
```

## Installation und Konfiguration EtherCAT-Master

Seit August 2013 gibt es die Möglichkeit, ein Debian-Paket zu bauen,
siehe https://github.com/sittner/ec-debianize

Installation:

```bash
$ git clone https://github.com/sittner/ec-debianize
$ cd ec-debianize
$ debian/configure -a
$ dpkg-checkbuilddeps
$ dpkg-buildpackage
$ cd ..
$ sudo dpkg -i etherlabmaster*deb
```

Installation ntp:

```bash
$ sudo apt-get -y install ntp
```

Benutzer in die Gruppe "ethercat" aufnehmen:

```bash
$ sudo usermod -aG ethercat koppi
```

Ausloggen, wieder Einloggen, Test:

```bash
$ sudo /etc/init.d/ethercat start
$ ethercat slaves
0  0:0  PREOP  +  EK1100 EtherCAT-Koppler (2A E-Bus)
1  0:1  PREOP  +  EL2004 4K. Dig. Ausgang 24V, 0.5A
2  0:2  PREOP  +  EL2004 4K. Dig. Ausgang 24V, 0.5A
3  0:3  PREOP  +  EL1004 4K. Dig. Eingang 24V, 3ms
4  0:4  PREOP  +  EL7041-1000 1K. Schrittmotor-Endstufe (50V, 5A, standard)
5  0:5  PREOP  +  EL7041-1000 1K. Schrittmotor-Endstufe (50V, 5A, standard)
6  0:6  PREOP  +  EL7041-1000 1Ch. Stepper motor output stage (50V, 5A, standard)
7  0:7  PREOP  +  EL2622 2K. Relais Ausgang, Schlie�er (230V AC / 30V DC)
```

## Konfiguration EL7041-1000 Schrittmotor-Endstufen

Siehe Beckhoff [BECKHOFF EL7031, EL7041-x00x, EP7041-000x: Commissioning](http://infosys.beckhoff.de/english.php?content=../content/1033/el70x1/html/bt_ecbasics_implementation210_ethport_02.htm&id=9823):

* [Configuration of the main parameters](http://infosys.beckhoff.de/english.php?content=../content/1033/el70x1/html/ex70x1_adjustments.htm&id=9833)

Ausgangsleistung auslesen:
```bash
$ for i in 4 5 6; do ethercat -p $i   upload --type uint16 0x8010 0x01; done
```
Ausgangsleistung (– hier: 2000mA) anpassen:
```bash
$ for i in 4 5 6; do ethercat -p $i download --type uint16 0x8010 0x01 2000; done
```

## LinuxCNC / EtherCAT HAL-Module

Installation als Debian-Paket:
```bash
$ git clone https://github.com/sittner/linuxcnc-ethercat
$ cd linuxcnc-ethercat
```
Austauschen ```linuxcnc-dev``` => ```machinekit-dev```:
```diff
diff --git a/debian/control b/debian/control
index 8a627be..83d36e8 100644
--- a/debian/control
+++ b/debian/control
@@ -2,10 +2,10 @@ Source: linuxcnc-ethercat
 Section: unknown
 Priority: extra
 Maintainer: linuxcnc <linuxcnc@localhost.localdomain>
-Build-Depends: debhelper (>= 8.0.0), linuxcnc-dev, etherlabmaster-dev
+Build-Depends: debhelper (>= 8.0.0), machinekit-dev, etherlabmaster-dev
 Standards-Version: 3.9.3

 Package: linuxcnc-ethercat
 Architecture: any
-Depends: ${shlibs:Depends}, ${misc:Depends}, linuxcnc, etherlabmaster
+Depends: ${shlibs:Depends}, ${misc:Depends}, machinekit, etherlabmaster
 Description: LinuxCNC EtherCAT HAL driver
```
Debian-Paket bauen und installieren:
```bash
$ sudo apt-get -y install machinekit-dev
$ dpkg-checkbuilddeps
$ debuild -uc -us
$ cd ..
$ sudo dpkg -i linuxcnc-ethercat*deb
```
alternativ: manuelle Installation
```bash
$ sudo apt-get -y install machinekit-dev
$ git clone https://github.com/sittner/linuxcnc-ethercat
$ make -C linuxcnc-ethercat all
$ sudo make -C linuxcnc-ethercat install
```

## Verkabelung

![pics/koppi-cnc-beckhoff.png](pics/koppi-cnc-beckhoff.png)

## Machinekit / LinuxCNC Konfiguration

Konfigurationsdateien: [linuxcnc/configs/koppi-cnc](linuxcnc/configs/koppi-cnc)

## AXIS starten

```bash
$ linuxcnc ~/linuxcnc/configs/koppi-cnc/koppi-cnc.ini
MACHINEKIT - 0.1
Machine configuration directory is '/home/koppi/linuxcnc/configs/koppi-cnc'
Machine configuration file is 'koppi-cnc.ini'
Starting Machinekit...
io started
halcmd loadusr io started
task pid=24244
emcTaskInit: using builtin interpreter
```

LinuxCNC / Machinekit AXIS:

![LinuxCNC / Machinekit AXIS](pics/20150515-002.png)

Desktop-Shortcut einrichten:

```bash
$ ln -s ~/linuxcnc/configs/koppi-cnc/koppi-cnc.desktop ~/Desktop/koppi-cnc.desktop 
```

AXIS icons:

Umstellung auf [Font Awesome icons](http://fortawesome.github.io/Font-Awesome/icons/): siehe [#3](https://github.com/koppi/mk/issues/3).

TODO - ```cnc-info.sh```:

![cnc-info.sh](pics/20150514-002.gif)

## Links / Sonstiges

Machinekit

* http://www.machinekit.io/
* https://groups.google.com/forum/#!forum/machinekit
* https://github.com/machinekit/machinekit/issues

LinuxCNC

* http://linuxcnc.org/
* http://linuxcnc.org/index.php/english/forum/index
* http://linuxcnc.org/index.php/english/news
* http://linuxcnc.org/index.php/english/documentation

Xenomai Kalibrierung

* Estimate Clock Latency

  http://jbohren.com/articles/xenomai-precise/
  
  http://wiki.linuxcnc.org/cgi-bin/wiki.pl?XenomaiKernel
  
  http://www.xenomai.org/pipermail/xenomai/2014-July/031217.html

EtherCAT

* LinuxCNC EtherCAT

  http://wiki.linuxcnc.org/cgi-bin/wiki.pl?EtherCatDriver
  
  http://www.linuxcnc.org/index.php/german/forum/24-hal-components/22346-ethercat-hal-driver

* Dr. Andreas Schiffler - CNC Retrofit

  https://www.youtube.com/user/drschiffler
  
  http://walter.roschi.eu/cnc-retrofit/
  
  Using BoschRexroth Drives with LinuxCNC
  
  http://www.linuxcnc.org/index.php/english/forum/27-driver-boards/27129-using-boschrexroth-drives-with-linuxcnc

* Sascha Ittner - Machinekit + EtherCAT on BeagleBone Black

  https://www.youtube.com/watch?v=M1LxQBjttWg
  
  https://github.com/sittner/linuxcnc-ethercat

* 陳伯綸 - LinuxCNC+IgH EtherCAT Master+FR-1000+beckhoff I/O DEMO

  https://www.youtube.com/watch?v=e6lXfIGkCH8

EtherCAT slave

* Software / User Space Slave

  http://comments.gmane.org/gmane.network.etherlab.user/1715
  
  git clone git://git.code.sf.net/p/ecslave/code ecslave

* ethercat operating system. A boot-able i386 linux based distribution running etherLAB

  http://sourceforge.net/projects/ecatos/ 

* etherlab domain manager

  This is a QT based pdo domain manager. It is a gui tool used to create a domain and slaves code based on xml provided by etherlab utility.

  http://sourceforge.net/projects/elabdomainmng/

* https://github.com/OpenEtherCATsociety

  * SOEM - Simple Open Source EtherCAT Master
  * SOES - Simple Open Source EtherCAT Slave
  
EtherCAT SOCs

* [QNX Evaluation Kit phyBOARD-Wega-AM335x](http://www.ibv-augsburg.net/media/pdf/QNX_Evaluation_Kit_phyBOARD-Wega_Product_Sheet.pdf)

  http://www.ibv-augsburg.net/

* BeagleBone variant called BotBone with two NICs suited for EtherCAT master/slave

  https://docs.google.com/document/d/1X9RrbkUpiTQ-S6Acken-5fv7yYq2DTr_1zOjf6zabn0/edit#heading=h.fxx7nvltcl7x

  https://plus.google.com/109948108631535499425/posts/jLJbwwJrLgP

  http://www.mapacode.tw/

Deutsche Foren:

* Peter's CNC-Ecke

  http://www.cncecke.de/

* SPS Forum

  http://www.sps-forum.de/

Nützliche Debian-Pakete

```bash
vim vim-scripts screen wicd-curses
```

## Machinekit HACKING

Mitmachen

  * http://www.machinekit.io/docs/contributing/

Machinekit Debian/Wheezy: Pakete für die Entwicklungsumgebung installieren:

```bash
sudo apt-get install libczmq-dev python-zmq libjansson-dev \
    libwebsockets-dev libxenomai-dev python-pyftpdlib
```

```bash
sudo sh -c \
    "echo 'deb http://ftp.de.debian.org/debian wheezy-backports main' > \
	     /etc/apt/sources.list.d/wheezy-backports.list"
		 sudo apt-get update
		 sudo apt-get install -t wheezy-backports cython
```

### Machinekit coding style (WIP)

* Please use the settings for C++ (put in your .emacs):

  https://github.com/machinekit/machinekit/issues/391#issuecomment-72355100
  
* strahlex / coding_style.el

  https://github.com/machinekit/machinekit/pull/625#issuecomment-100625726

### git / GitHub fork, clone, branch, commit, push, rebase, merge

TODO

### Tools

perf

```bash
$ sudo apt-get -y install linux-base inux-tools-3.8
```

lttng

```bash
TODO
```

libbacktrace

```bash
TODO
```

### Installation Xenomai (2.6.4)

* Neueres Xenomai bauen, siehe

  https://xenomai.org/2014/06/building-debian-packages

## Konfiguration TODO

* Tool length probe switch

  http://softsolder.com/2010/04/17/ugliest-tool-length-probe-switch-repeatability/
