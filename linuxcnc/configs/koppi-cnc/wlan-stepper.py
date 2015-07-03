#!/usr/bin/env python

# sudo apt-get install mosquitto mosquitto-clients python-mosquitto
# sudo pip install paho-mqtt

import sys
import time
import logging
from logging import StreamHandler, Formatter
import datetime as dt

#from machinekit import hal
import hal
import paho.mqtt.client as mqtt

class MsecFormatter(logging.Formatter):
    converter=dt.datetime.fromtimestamp
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s,%03d" % (t, record.msecs)
        return s
        
logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logger = logging.getLogger('msec_logger')
logger.propagate = False

h = logging.StreamHandler()
h.setFormatter(MsecFormatter('[%(asctime)s]:%(message)s', datefmt='%s.%f'))
logger.addHandler(h)

work_thread = 0.001

h = hal.component("wlan-stepper")

def on_connect(client, userdata, rc):
    client.subscribe("pos-0-fb")
    
def on_message(client, userdata, msg):
    logger.debug("on_message: " + msg.topic + ': ' + str(msg.payload))

    if msg.topic == "pos-0-fb":
        h["pos-0-fb"] = long(msg.payload.strip('\0'))

def on_publish(client, packet, msd):
    logger.debug("on_publish: " +  msg.topic + ': ' + str(msg.payload))

logger.debug("init")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set(userID, password)
client.connect("localhost", 1883, 60)
    
def run() :
    logger.debug("run")
    
    h.newpin("pos-0-cmd", hal.HAL_FLOAT, hal.HAL_IN)
    h.newpin("pos-0-fb", hal.HAL_FLOAT, hal.HAL_OUT)
    logger.debug("ready")
    h.ready()

    pos_0_cmd_old = 0

    try:
        while True:
            time.sleep(work_thread)
            client.loop()

            pos_0_cmd = h["pos-0-cmd"]

            if pos_0_cmd_old != pos_0_cmd:
                client.publish("pos-0-cmd", pos_0_cmd)
                pos_0_cmd_old = pos_0_cmd
                
    except KeyboardInterrupt :
        raise SystemExit

run()
