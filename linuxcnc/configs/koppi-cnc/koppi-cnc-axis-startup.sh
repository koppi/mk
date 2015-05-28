#!/usr/bin/env bash

sleep .2
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