"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import bluetooth
#f0:d5:bf:b2:6a:a5 address of my computer
#B8:27:EB:01:FB:F1 address of rpi
class bluetooth_computer_test():
    def __init__(self):
        self.serverMACAddress = 'B8:27:EB:01:FB:F1'
        self.port = 1
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.serverMACAddress, self.port))

    def send_bluetooth_message(self, input):
        self.s.send(input)
    def close_bluetooth_connection(self):
        self.s.close()
