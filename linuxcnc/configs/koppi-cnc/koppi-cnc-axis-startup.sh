#!/usr/bin/env bash

echo "koppi-cnc-axis-startup.sh"

sleep 1
halcmd setp halui.machine.on 0
sleep .2
halcmd setp halui.estop.reset 1
sleep .2
halcmd setp halui.estop.reset 0
sleep .2
halcmd setp halui.machine.on 1
sleep .2

# turn on Z axis compensation
halcmd sets comp-toggle 1
sleep .2
halcmd sets comp-toggle 0

# clear notifications
halcmd setp axisui.notifications-clear 1
sleep .100 ;# requires a sleep that does <1
halcmd setp axisui.notifications-clear 0
