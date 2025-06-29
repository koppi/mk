## build a LinuxCNC Debian/GNU Linux bookworm 8GB image

```bash
sudo apt -y install grml-debootstrap apt-cacher
```
```bash
sudo vi /etc/apt-cacher/apt-cacher.conf
```
uncomment
```
#allowed_hosts = *
```
and restart apt-cacher
```bash
sudo /etc/init.d/apt-cacher restart
```
next, build and run machinekit-bookworm.img:
```bash
$ time sh x &> machinekit-bookworm.log
$ sh y # run in QEMU
```
