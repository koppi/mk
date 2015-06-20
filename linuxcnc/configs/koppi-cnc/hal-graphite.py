#!/usr/bin/env python
# -*- coding: utf-8 -*-

# sudo apt-get -y install graphite-carbon

import sys
import re
import time
import hal
import logging

from machinekit import hal

import subprocess
from shlex import split

work_thread = 5.0 # update pins every [sec]

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
#logging.basicConfig(stream=sys.stderr, level=logging.INFO)

def carbon(name, value, t):
        cmd = "echo '%s %f %d'" % (name, value, t)
        p1 = subprocess.Popen(split(cmd),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        p2 = subprocess.Popen(split("nc -q0 127.0.0.1 2003"), stdin=p1.stdout)
#        retval = p2.wait()
#        if (retval == 0):
#                logging.debug(cmd)
#        else:
#                raise Exception('Error: statsd: %s' % (cmd))

class Info :
        def __init__(self) :
                logging.debug("ready")
        
        def run(self) :
                while 1:
                        try:
                                t = int(time.time())
                                for sig in hal.signals():
                                        s = hal.Signal(sig)
                                        for pin in s.pins():
                                                carbon('hal.' + pin.name, float(pin.get()), t)
                                
                                time.sleep(work_thread)
                        except KeyboardInterrupt :
                                raise SystemExit
                        except Exception,e:
                                print str(e)

i = Info()
i.run()
