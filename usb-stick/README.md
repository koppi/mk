# Build a Debian/GNU Linux Bookworm Image for LinuxCNC

This project provides a set of scripts to build a customized Debian/GNU Linux (Bookworm) image that includes LinuxCNC. The resulting image is approximately 8GB.

## Prerequisites

Before you begin, you need to install the following packages:

```bash
sudo apt-get update
sudo apt-get install -y grml-debootstrap apt-cacher
```

## Configuration

The build process uses `apt-cacher` to cache downloaded packages, which can significantly speed up subsequent builds. You need to configure it to allow access from the build environment.

1.  Edit the `apt-cacher.conf` file:

    ```bash
    sudo vi /etc/apt-cacher/apt-cacher.conf
    ```

2.  Uncomment the following line to allow hosts to connect:

    ```
    allowed_hosts = *
    ```

3.  Restart the `apt-cacher` service for the changes to take effect:

    ```bash
    sudo systemctl restart apt-cacher.service
    ```

## Building the Image

To build the image, run the main build script. It's recommended to redirect the output to a log file to monitor the process and for debugging purposes.

```bash
time sudo sh x &> linuxcnc-bookworm.log
```

## Running the Image

Once the build is complete, you can run the generated `linuxcnc-bookworm.img` file in QEMU using the following command:

```bash
sh y
```

## Demo

For a demonstration of the build process and the resulting image in action, please watch this video:

[https://youtu.be/p2XF-iWrrYM](https://youtu.be/p2XF-iWrrYM)