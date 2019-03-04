#!/usr/bin/env python
# Author : Diego Torres
# Description : Server for control system called by App
# Date of Modification : 3/2/2018

# Libraries
from socket import *
import numpy as np
import cv2
from video_stream import video_stream
from sensor_stream import sensor_stream
import threading

class server():
    def __init__(self,server_ip, video_port, sensor_port):
        print('server')
        #video and sensor thread
        s_thread = threading.Thread(target=self.sensor_stream, args=(server_ip,sensor_port))
        s_thread.daemon = True
        s_thread.start()

        v_thread = threading.Thread(target=self.video_stream, args=(server_ip,video_port))
        v_thread.daemon = True
        v_thread.start()

    def video_stream(self,server_ip,video_port):
        vs = video_stream(server_ip,video_port)
        print('video_stream thread')


    def sensor_stream(self,server_ip,sensor_port):
        ss = sensor_stream(server_ip,sensor_port)
        print('sensor_stream thread')
