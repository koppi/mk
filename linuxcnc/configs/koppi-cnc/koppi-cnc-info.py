#!/usr/bin/env python

import sys
import time
import hal
import logging
import subprocess

work_thread = 2.0 # work_thread means how often pins will be updated (sec)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def ec_upload(p, t, addr, value):
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

class Info :
        def __init__(self) :
                logging.info("koppi-cnc-info.py init")
                self.h = hal.component("koppi-cnc-info")
                logging.info("koppi-cnc-info.py ok")

                for i in range(0,3):
                        self.h.newpin("motor-supply-%d" % (i), hal.HAL_FLOAT, hal.HAL_OUT)
                        self.h.newpin("max-current-%d"  % (i), hal.HAL_FLOAT, hal.HAL_OUT)
                        self.h.newpin("temp-%i" % (i), hal.HAL_S32, hal.HAL_OUT)
                self.h.ready()

        def run(self) :
                offset = 4

                while 1:
                        try:
                                for i in range(0,3):
                                        self.h['motor-supply-%d' % (i)] = ec_upload(i+offset, "uint16", 0xF900, 0x05) / 1000.0
                                        self.h['max-current-%d'  % (i)] = ec_upload(i+offset, "uint16", 0x8010, 0x01) / 1000.0
                                        self.h['temp-%d' % (i)]         = ec_upload(i+offset, "int8",   0xF900, 0x02)
                                time.sleep(work_thread)
                        except KeyboardInterrupt :
                                raise SystemExit
                        except Exception,e:
                                print str(e)

i = Info()
i.run()
