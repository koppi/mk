#!/usr/bin/env python

# sudo apt-get install mosquitto mosquitto-clients python-mosquitt
# sudo pip install paho-mqtt

########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######
########################### EXPERIMENTAL / DON'T USE IN PRODUCTION ######

import sys
import logging

import hal, time
import paho.mqtt.client as mqtt

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

work_thread = 0.05

h = hal.component("esp-01-mqtt")

old_gp0 = False
old_gp2 = False

    
def on_connect(client, userdata, rc):
    client.subscribe("esp-01/status")
    client.subscribe("esp-01/gp0")
    client.subscribe("esp-01/gp2")
    
def on_message(client, userdata, msg):
    global old_gp0, old_gp2
    
    logging.debug("on_message: " + msg.topic + ' : ' + str(msg.payload))

    if msg.topic == "esp-01/gp0":
        if str(msg.payload) == "0":
            h["gp0"] = False
            old_gp0  = False
        elif str(msg.payload) == "1":
            h["gp0"] = True
            old_gp0  = True

    if msg.topic == "esp-01/gp2":
        if str(msg.payload) == "0":
            h["gp2"] = False
            old_gp2  = False
        elif str(msg.payload) == "1":
            h["gp2"] = True
            old_gp2  = True

def on_publish(client, packet, msd):
    logging.debug("on_publish: " +  msg.topic + ' : ' + str(msg.payload))

logging.debug("init")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set(userID, password)
client.connect("localhost", 1883, 60)
    
def run() :
    global old_gp0, old_gp2
    logging.debug("run")
    
    h.newpin("gp0", hal.HAL_BIT, hal.HAL_IN)
    h.newpin("gp2", hal.HAL_BIT, hal.HAL_IN)
    logging.debug("ready")
    h.ready()

    try:
        while True:
            time.sleep(work_thread)
            client.loop()

            gp0 = h["gp0"]
            gp2 = h["gp2"]

            if gp0 != old_gp0:
                if gp0:
                    client.publish("esp-01/gp0", "1")
                else:
                    client.publish("esp-01/gp0", "0")
                
            if gp2 != old_gp2:
                if gp2:
                    client.publish("esp-01/gp2", "1")
                else:
                    client.publish("esp-01/gp2", "0")                    
            
            old_gp0 = gp0
            old_gp2 = gp2

    except KeyboardInterrupt :
        raise SystemExit

run()
