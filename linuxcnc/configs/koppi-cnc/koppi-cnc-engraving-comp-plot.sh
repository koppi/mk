#!/usr/bin/env bash

gnuplot <<- EOF
  set term png size 800,700 font arial 14
  set output "koppi-cnc-engraving-comp.png"

  set noborder
  set key off

  set xrange [-10.5:220]
  set yrange [-10.25:220.5]

  set xtics 50
  set ytics 50
  set cbtics 0.1
  set format cb "%3.1f"

  set title "Z-Achsen Korrektur"

  set view map
  set size ratio 1
  set object 1 rect from graph 0, graph 0 to graph 1, graph 1 back
  set object 1 rect fc rgb "black" fillstyle solid 1.0
  set palette rgbformulae 22,13,-31

  splot 'koppi-cnc-engraving-comp.txt' using 1:2:3 with points pointtype 5 pointsize 1 palette linewidth 30
EOF
