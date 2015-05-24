#!/usr/bin/env bash

gnuplot <<- EOF
  set term png
  set output "koppi-cnc-engraving-comp.png"
  set key off

  set view map
  set size ratio 1
  set object 1 rect from graph 0, graph 0 to graph 1, graph 1 back
  set object 1 rect fc rgb "black" fillstyle solid 1.0

  splot 'koppi-cnc-engraving-comp.txt' using 1:2:3 with points pointtype 5 pointsize 1 palette linewidth 30
EOF
