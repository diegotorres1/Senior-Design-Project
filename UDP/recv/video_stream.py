#!/usr/bin/env python
# Author : Diego Torres
# Description : Server for control system called by App
# Date of Modification : 3/2/2018

# Libraries
from socket import *
import numpy as np
import cv2
import time
import sys
import os

sys.path.insert(0, '../../Bluetooth/')
from bluetooth_computer_test import bluetooth_computer_test
sys.path.insert(0, '../../Object_Detection/')
from stop_light_detector import stop_light_detector

class video_stream():
    def __init__(self, server_ip, video_port):
        ## Server Params
        self.addr = (server_ip, video_port)
        self.fName = 'img.jpg'
        self.timeOut = 0.05
        self.buf = 1024

        # Image Processing Params
        lights_dict = {'r':'Stop Light Red', 'g':'Stop Light Green','y':'Stop Light Yellow'}
        self.output_string = ''
        sld = stop_light_detector()
        bc = bluetooth_computer_test()

        try:
            #reconnection while loop
            while True:
                s = socket(AF_INET, SOCK_DGRAM)
                s.bind(self.addr)
                data, address = s.recvfrom(self.buf)
                try:
                    f = open(data, 'wb')
                except:
                    continue

                data, address = s.recvfrom(self.buf)

                #video while loop
                try:
                    while(data):
                        f.write(data)
                        s.settimeout(self.timeOut)
                        data, address = s.recvfrom(self.buf)
                except self.timeout:
                    f.close()
                    s.close()

                # Image Read
                image = cv2.imread(self.fName)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image = cv2.resize(image,(int(1280/6),int(720/6)))

                # Image Processing
                start_time = time.time()
                temp_time = time.time()
                [image,dimension] = sld.detect_stop(image)
                print('Stop Detection Time: ' + str(time.time() - temp_time))
                temp_time = time.time()
                [image,light_color] = sld.detect_stoplight(image)
                print('Stop Light Time: ' + str(time.time() - temp_time))

                # Bluetooth transmission
                bc.send_bluetooth_message(light_color)
                if(dimension[0] is not None and dimension[0] != 0):
                    bc.send_bluetooth_message(b's')
                    self.output_string = 'stopsign'
                elif(light_color != '0'):
                    self.output_string = lights_dict[light_color]
                else:
                    self.output_string = ''
                print('Bluetooth Time : ' + str(time.time() - temp_time))

                # Display Image
                image = cv2.resize(image,(int(1280/2),int(720/2)))
                cv2.imshow('stream',image)
                print('Total Image Process Timing : ' + str(time.time() - start_time))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print('Stream cancelled')
                    break

                #Cross Talk
                bool = True
                while(bool):
                    try:
                        with open('../Cross_Talk/receive_f.txt','w') as f:
                            data = f.write(self.output_string)
                        f.close()
                        bool = False
                    except:
                        print('recieve_f not available')
                        pass
                bool = True
                while(bool):
                    try:
                        with open('../Cross_Talk/transmit_f.txt','r') as f:
                            data = f.read()
                        bc.send_bluetooth_message(data)
                        f.close()
                        bool = False
                    except Exception as e:
                        print('transmit_f not available')
                        print(os.getcwd())
                        print(e)
                        pass

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, self.fname, exc_tb.tb_lineno)
