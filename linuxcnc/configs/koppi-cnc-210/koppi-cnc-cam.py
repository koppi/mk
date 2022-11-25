#!/usr/bin/env python

import cv

capture = cv.CaptureFromCAM(0)
cv.WaitKey(200)

frame = cv.QueryFrame(capture)
font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1, 1, 0, 2, 8)

while True:
       frame = cv.QueryFrame(capture)

#       cv.PutText(frame, "ShapeOko CAM", (10,460), font, cv.RGB(17, 110, 255))
       cv.Line(frame, (320,0), (320,480) , 255)
       cv.Line(frame, (0,240), (640,240) , 255)
       cv.Circle(frame, (320,240), 100, 255)
       
       cv.ShowImage("Window",frame)
       c = (cv.WaitKey(16) & 255)
       
       if c==27: #Break if user enters 'Esc'.
           break
