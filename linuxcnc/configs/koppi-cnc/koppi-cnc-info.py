#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import time
import hal
import logging
import subprocess

work_thread = 1.0 # update pins every [sec]

#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def sensors(value):
        cmd = "sensors"
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
#        for line in p.stdout.readlines():
#                print "1 %s" % line

        retval = p.wait()
        if (retval == 0):
                v = filter(lambda x:re.search(r'%s'%(value), x), p.stdout.readlines())
                return v[0]
        else:
                raise Exception('Error: ec_upload: %s' % (cmd))

class Info :
        def __init__(self) :
#                logging.info("koppi-cnc-info.py init")
                self.h = hal.component("koppi-cnc-info")
#                logging.info("koppi-cnc-info.py ok")

                for i in range(0,3):
                        self.h.newpin("motor-supply-%d" % (i), hal.HAL_FLOAT, hal.HAL_OUT)
                        self.h.newpin("max-current-%d"  % (i), hal.HAL_FLOAT, hal.HAL_OUT)
                        self.h.newpin("temp-%i" % (i), hal.HAL_S32, hal.HAL_OUT)
                self.h.newpin("fan1-rpm", hal.HAL_S32, hal.HAL_OUT)
                self.h.newpin("temp1",    hal.HAL_FLOAT, hal.HAL_OUT)
                self.h.newpin("link-up",  hal.HAL_BIT, hal.HAL_IN)
                self.h.ready()

        def ec_upload(self, p, t, addr, value):
                if not self.h['link-up']:
                        return 0
                
                cmd = "ethercat -p %d upload --type %s %d %d" % (p, t, addr, value)
                p = subprocess.Popen(cmd, shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
#        for line in p.stdout.readlines():
#                print "1 %s" % line

                retval = p.wait()
                if (retval == 0):
                        v = p.stdout.readlines()[0].split()[1]
#                print v
                        return int(v)
                else:
                        raise Exception('Error: ec_upload: %s' % (cmd))

        def run(self) :
                offset = 4

                while 1:
                        try:
                                for i in range(0,3):
                                        self.h['motor-supply-%d' % (i)] = self.ec_upload(i+offset, "uint16", 0xF900, 0x05) / 1000.0
                                        self.h['max-current-%d'  % (i)] = self.ec_upload(i+offset, "uint16", 0x8010, 0x01) / 1000.0
                                        self.h['temp-%d' % (i)]         = self.ec_upload(i+offset, "int8",   0xF900, 0x02)
                                self.h['fan1-rpm'] = int(sensors("fan1").split(":")[1].replace("RPM", ""))
                                self.h['temp1'] = float(sensors("temp1").split(":")[1].replace("°C", "").replace("+", ""))

                                time.sleep(work_thread)
                        except KeyboardInterrupt :
                                raise SystemExit
                        except Exception,e:
                                print str(e)

i = Info()
i.run()
