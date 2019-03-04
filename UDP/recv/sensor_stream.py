#!/usr/bin/env python
# Author : Diego Torres
# Description : Server for control system called by App
# Date of Modification : 3/2/2018

# Libraries
from socket import *
class sensor_stream():
    def __init__(self,server_ip, sensor_port):
        data = " "
        bufferSize  = 1024
        global sensor_data
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((server_ip, sensor_port))
        while True:
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            self.data = bytesAddressPair[0]
            bool = True
            while(bool):
                try:
                    with open('data_transfer_files/recieve_s.txt','w') as f:
                        data = f.write(self.data)
                    f.close()
                    bool = False
                except:
                    pass
