#!/usr/bin/env python

"""Copyright (C) 2009 Nick Drobchenko, nick@cnc-club.ru

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
import sys
import logging

work_thread = 0.05 # update pins every [sec]

# koppi-cnc:
# probe "o<koppi_cnc_comp> call [0] [0] [220] [220] [10] [10] [100] [10] [1.5] [-3]"

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# prepare height map
class Compensation :
        def __init__(self) :
                logging.debug("init")
                self.comp = {}
                self.x_coords = []
                self.y_coords = []
                if len(sys.argv)<2:
                        logging.error("No input file name specified. Exiting.")
                        sys.exit()

                self.range_x,self.range_y, self.len_x,self.len_y = [],[], 0,0

                self.filename = sys.argv[1]
                logging.debug("filename = %s" % (self.filename))

                self.reset()
                logging.debug("get_comp(10,10) = %f" % (self.get_comp(10,10)))


        def reset(self) :
                logging.debug("reset")
                f = open(self.filename,"r")
                probe_lines = f.readlines()
                logging.debug("probe_lines = %d" % (len(probe_lines)))

                self.comp = {}
                self.x_coords = []
                self.y_coords = []
                for line in probe_lines :
                        coords = [float(i) for i in line.split()]
                        x,y,z = coords[0:3]
                        x,y = int(round(x,0)), int(round(y,0))
                        if x not in self.comp :  self.comp[x] = {}
                        self.comp[x][y] = z
                        if not x in self.x_coords : self.x_coords.append(x)
                        if not y in self.y_coords : self.y_coords.append(y)

                self.x_coords.sort()
                self.y_coords.sort()

                logging.debug("x_coords: %s" % (self.x_coords))
                logging.debug("y_coords: %s" % (self.y_coords))

                # check map integrity, map should be rectangular!
                for x in self.x_coords :
                        for y in self.y_coords :
                                if not x in self.comp or not y in self.comp[x] :
                                        logging.error("Map should be rectangular. Can't find point %s,%s"%(x,y))
                                        sys.exit()
                                else:
                                        logging.debug("%d,%d in self.comp" % (x,y))
                self.len_x = len(self.x_coords)
                self.range_x = range(self.len_x)
                self.len_y = len(self.y_coords)
                self.range_y = range(self.len_y)
                #print self.x_coords
                #for x in self.comp :
                #       print x, "     ",self.comp[x]
                #print self.len_x, self.len_y
                logging.debug("ok")
                self.error = True

        def get_comp(self,x,y) :
                        mx = x
                        my = y
                        x = max(self.x_coords[0],min(self.x_coords[-1],x))
                        y = max(self.y_coords[0],min(self.y_coords[-1],y))
                        i = 0
                        while i<self.len_x :
                                if self.x_coords[i]>x : break
                                i+=1

                        j = 0
                        while j<self.len_y :
                                if self.y_coords[j]>y : break
                                j+=1

                        if i==self.len_x : i -= 1
                        if j==self.len_y : j -= 1
                        x2=self.x_coords[i]
                        y2=self.y_coords[j]


                        if i<self.len_x:
                                x1 = self.x_coords[max(0,i-1)]
                        else:
                                x1 = x2

                        if j<self.len_y:
                                y1 = self.y_coords[max(0,j-1)]
                        else:
                                y1 = y2


                        # now make bilinear interpolation of the points
                        if x1 != x2 :
                                z1 = ((x2-x)*self.comp[x1][y1] + (x-x1)*self.comp[x2][y1])/(x2-x1)
                                z2 = ((x2-x)*self.comp[x1][y2] + (x-x1)*self.comp[x2][y2])/(x2-x1)
                        else:
                                z1 = self.comp[x1][y1]
                                z2 = self.comp[x1][y2]
                        if y1 != y2 :
                                z1 = ((y2-y)*z1 + (y-y1)*z2)/(y2-y1)

                        logging.debug("%4.2f,%4.2f %4.2f,%4.2f %4.2f" % (mx,my,x,y,z1))
                        return z1


        def run(self) :
                import hal, time

                h = hal.component("compensation")
                h.newpin("out", hal.HAL_FLOAT, hal.HAL_OUT)
                h.newpin("enable", hal.HAL_BIT, hal.HAL_IN)
                h.newpin("x-map", hal.HAL_FLOAT, hal.HAL_IN)
                h.newpin("y-map", hal.HAL_FLOAT, hal.HAL_IN)
                h.newpin("reset", hal.HAL_BIT, hal.HAL_IN)
                h.newpin("error", hal.HAL_BIT, hal.HAL_OUT)
                # ok, lets we are ready, lets go
                h.ready()
                last_reset = h["reset"]
                try:
                        while 1:
                                try:
                                        time.sleep(work_thread)
                                        if h["enable"] :
                                                x=h['x-map']
                                                y=h['y-map']
                                                h["out"]=self.get_comp(x,y)
                                        else :
                                                h["out"]=0
                                        if h["reset"]  and not last_reset:
                                                        self.reset()
                                        last_reset = h["reset"]
                                except KeyboardInterrupt :
                                        raise SystemExit
                                except :
                                        h["error"] = False
                                else :
                                        h["error"] = True

                except KeyboardInterrupt:
                  raise SystemExit

comp = Compensation()
comp.run()
