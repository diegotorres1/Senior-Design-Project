#!/usr/bin/env python
# Author : Diego Torres
# Description : App for control system called by Main
# Date of Modification : 3/2/2018

# Libraries
import numpy as np
from socket import *
from PIL import Image
import io
import picamera
import time
from bluetooth_test import bluetooth_test
import threading
class video_send():
    def __init__(self, server_ip, video_port):
        #server parameters
        self.ratio = 3
        self.host = server_ip
        self.port = video_port
        self.addr = (self.host, self.port)
        self.buf = 1024

        #bluetooth
        btt = bluetooth_test()
        threading.Thread(target=btt.bluetooth_stream).start()

    def sendFile(self,fName):
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto(bytes(fName, 'utf-8'), self.addr)
        f = open(fName, "rb")
        data = f.read(self.buf)
        while data:
            print(type(data))
            if(s.sendto(data, self.addr)):
                data = f.read(self.buf)
        f.close()
        s.close()

    def capture(self):
        print('Capture')
        count = 0
        with picamera.PiCamera() as cam:
            cam.resolution = (320,240)
            time.sleep(2)
            #create streams
            stream = io.BytesIO()
            for frame in cam.capture_continuous(stream,'jpeg',use_video_port = True):

                if frame is not None:
                    #~ cv2.imshow('frame', frame)
                    count = count + 1
                    if count == self.ratio:
                        # image = cv2.resize(frame,(int(1280/4),int(720/4)))
                        stream.seek(0)
                        image = Image.open(stream)

                        #~ image = Image.fromarray(frame)
                        # cv2.imwrite("img.jpg", image)
                        image.save('img.jpg')
                        self.sendFile("img.jpg")
                        count = 0
                        stream.seek(0)
                        stream.truncate() 
                else:
                    break
