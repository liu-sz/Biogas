#!/usr/bin/env python3.7
#-*- coding: utf-8 -*-

from picamera import PiCamera
import time
import os

camera = PiCamera()
camera.resolution = (1000, 1000)
# 500x500: 212 kB 
# 750x750: 396 kB
# 1000x1000: 724 kB
# 1250x1250: 720 kB
# File size depends on environment (light levels, etc)

def getTime():
    curr_time = time.localtime()
    timestamp = ''
    for i in range(5):
        timestamp += ('_' + str(curr_time[i]))
    print(timestamp)
    return timestamp

def getImage():
    file_name = ''
    #camera.start_preview()
    time.sleep(5)
    print(time.localtime())
    file_name = '/home/pi/Desktop/image%s.jpg' % getTime()
    camera.capture(file_name)
    #camera.stop_preview()
    cmd = 'scp ' + file_name + ' biogas@image_server:/home/biogas/images'
    #scp image2022721617.jpg biogas@image_server:/home/biogas/images
    os.system(cmd)
    camera.close() # Prevent port error

getImage()