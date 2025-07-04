# LinuxCNC / EtherCAT Notes and Configurations

This repository contains notes, configurations, and scripts for running a CNC machine with LinuxCNC and EtherCAT. It also includes setup guides for Machinekit on various hardware platforms.

[![Gitter](https://badges.gitter.im/koppi/mk.svg)](https://gitter.im/koppi/mk?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Contents

### LinuxCNC Configurations

This repository includes configurations for a CNC machine controlled by LinuxCNC. The main configuration is `koppi-cnc`, which has evolved over time. A newer version, `koppi-cnc-210`, is also available for LinuxCNC 2.10.

These configurations include:
- HAL (Hardware Abstraction Layer) files for I/O, spindle control, and axis movement.
- INI files for machine parameters.
- Custom Python scripts for additional functionality.
- Panel configurations for the AXIS GUI.

### Hardware Setup Guides

The repository contains detailed guides for setting up Machinekit on different hardware:

- **[Machinekit on a Beckhoff CX9020](Machinekit-Beckhoff-CX9020.md)**
- **[Machinekit on a Raspberry Pi with RT-Preempt](Machinekit-RT-Preempt-RPI.md)**
- **[Machinekit on a Thinkpad X200 with Xenomai](Machinekit-Xenomai-Thinkpad-X200.md)**

### USB Stick Build Scripts

There are scripts available to build a bootable USB stick with LinuxCNC. These scripts automate the process of setting up a live environment for running the CNC machine.

## Usage

To use the configurations in this repository, you will need a working installation of LinuxCNC. You can then clone this repository and link the configuration files to your LinuxCNC configuration directory.

```bash
git clone https://github.com/koppi/mk.git
cd mk
# Follow the instructions in the specific configuration's README
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.