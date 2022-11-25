#!/usr/bin/env bash

function drive_info() {
  local P="$1"
  echo "Device $i                 "
  echo "  Device name:      $(ethercat -p $P upload --type string 0x1008 0x0)"
  echo "  Hardware Version: $(ethercat -p $P upload --type string 0x1009 0x0)"
  echo "  Software Version: $(ethercat -p $P upload --type string 0x100A 0x00)"
  echo "  Product Code:     $(ethercat -p $P upload --type uint32 0x1018 0x02)"
  echo "  Revision:         $(ethercat -p $P upload --type uint32 0x1018 0x03)"
  echo "  Serial Number:    $(ethercat -p $P upload --type uint32 0x1018 0x04)"

  echo "  Internal Temp.:   $(ethercat -p $P upload --type int8   0xF900 0x02) deg"
  echo "  Motor Supply:     $(ethercat -p $P upload --type uint16 0xF900 0x05) mV"
  echo "  Maximum Current:  $(ethercat -p $P upload --type uint16 0x8010 0x01) mV"
  echo "  Cycle time:       $(ethercat -p $P upload --type uint16 0xF900 0x06)"

  echo "  Actual op. mode:  $(ethercat -p $P upload --type uint8 0xA010 0x11)"
  echo ""
  echo "  Ready to enable:  $(ethercat -p $P upload --type bool 0x6010 0x01)"
  echo "  Ready:            $(ethercat -p $P upload --type bool 0x6010 0x02)"
  echo "  Warning:          $(ethercat -p $P upload --type bool 0x6010 0x03)"
  echo "  Error:            $(ethercat -p $P upload --type bool 0x6010 0x04)"
  echo "  Sync Error:       $(ethercat -p $P upload --type bool 0x6010 0x0E)"
  echo "  Ready to enable:  $(ethercat -p $P upload --type bool 0x6010 0x01)"
  echo " Errors:                  "
#echo "  Saturated:         $(ethercat -p $P upload --type bool 0xA010 0x01)"
  echo "  Over Temperature: $(ethercat -p $P upload --type bool 0xA010 0x02)"
#echo "  Torque Temp:       $(ethercat -p $P upload --type bool 0xA010 0x03)"
  echo "  Under Voltage:    $(ethercat -p $P upload --type bool 0xA010 0x04)"
  echo "  Over Voltage:     $(ethercat -p $P upload --type bool 0xA010 0x05)"
#echo "  Short Circuit A:   $(ethercat -p $P upload --type bool 0xA010 0x06)"
#echo "  Short Circuit B:   $(ethercat -p $P upload --type bool 0xA010 0x07)"
  echo "  No Control Power: $(ethercat -p $P upload --type bool 0xA010 0x08)"
  echo "  Misc Error:       $(ethercat -p $P upload --type bool 0xA010 0x09)"
  echo "  Open load A:      $(ethercat -p $P upload --type bool 0xA010 0x0A)"
  echo "  Open load B:      $(ethercat -p $P upload --type bool 0xA010 0x0B)"
  echo "  Over current A:   $(ethercat -p $P upload --type bool 0xA010 0x0C)"
  echo "  Over current B:   $(ethercat -p $P upload --type bool 0xA010 0x0D)"
}

D=/run/shm/cnc_info_

for i in 1 2 3; do
  drive_info $i > $D$i
done

paste $D* | pr -t -e21

rm -f $D*
