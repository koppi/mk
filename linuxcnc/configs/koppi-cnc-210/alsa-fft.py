#!/usr/bin/env python2
#
# HAL component to output FFT spectrum of ALSA audio device
#
# sudo apt-get -y install python-alsaaudio
#
import sys
import logging
import alsaaudio as aa
from time import sleep
from struct import unpack
import numpy as np
import hal

rows = 8

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

work_thread = 0.01 # update pins every [sec]

def calculate_levels(data, chunk,sample_rate):
#   data    = unpack("%dh" % (len(data)), data)
   data    = np.fromstring(data, dtype='int16')
#   data    = np.array(data, dtype='h')
   fourier = np.fft.rfft(data)
   fourier = np.delete(fourier, len(fourier)-1)
   power   = np.log10(np.abs(fourier)+0.000001)**2
#   print (power)
   power   = np.reshape(power, (rows, chunk/rows/2))
   matrix  = np.average(power, axis=1)/4
   return matrix

logging.debug("init")

h = hal.component("alsa-fft")
h.newpin("min", hal.HAL_FLOAT, hal.HAL_OUT)
h.newpin("max", hal.HAL_FLOAT, hal.HAL_OUT)
for i in range(0, rows):
   h.newpin("fft-%d" % (i), hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()
logging.debug("ready")

sample_rate = 44100
chunk       = 1024 # Use a multiple of [rows]

logging.debug("aa.PCM begin")
audio = aa.PCM(type=aa.PCM_CAPTURE, mode=aa.PCM_NORMAL)
audio.setchannels(1)
audio.setrate(sample_rate)
audio.setformat(aa.PCM_FORMAT_S16_LE)
audio.setperiodsize(chunk)
logging.debug("aa.PCM end")

while True:
   l,data = audio.read()
   audio.pause(1)
   if l:
      matrix = calculate_levels(data, chunk, sample_rate)
      matrix_min = matrix.min()
      matrix_max = matrix.max()
      
      logging.debug("min %6.2f max %6.2f rows %s" % (matrix_min, matrix_max, ' '.join(("%2.0f" % (x) for x in matrix))))

      h["min"] = matrix_min
      h["max"] = matrix_max

      for i in range(0, rows):
         h["fft-%d" % (i)] = matrix[i]
      
   sleep(work_thread)
   audio.pause(0) # Resume capture
