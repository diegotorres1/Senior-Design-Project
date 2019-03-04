# Author : Diego Torres
# Description : App for control system called by Main
# Date of Modification : 3/2/2018

# Libraries
import bluetooth
import sys
import os

# Importing the GPIO library to use the GPIO pins of Raspberry pi

import RPi.GPIO as GPIO
class bluetooth_test():
    def __init__(self):
        self.red_led_pin = 4	# Initializing pin 40 for led
        self.yellow_led_pin = 17
        self.green_led_pin = 27
        self.speed = 13
        GPIO.setmode(GPIO.BCM)	# Using BCM numbering
        GPIO.setup(self.red_led_pin, GPIO.OUT)	# Declaring the pin 40 as output pin
        GPIO.setup(self.yellow_led_pin, GPIO.OUT)
        GPIO.setup(self.green_led_pin, GPIO.OUT)
        GPIO.setup(self.speed, GPIO.OUT)
        self.p = GPIO.PWM(self.speed, 20)
        self.p.start(0)

        host = ""
        port = 1	# Raspberry Pi uses port 1 for Bluetooth Communication
        # Creaitng Socket Bluetooth RFCOMM communication
        self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('Bluetooth Socket Created')
        try:
            self.server.bind((host, port))
            print("Bluetooth Binding Completed")
        except:
            print("Bluetooth Binding Failed")
        self.server.listen(1) # One connection at a time
        # Server accepts the clients request and assigns a mac address.
        self.client, self.address = self.server.accept()
        print("Connected To", self.address)
        print("Client:", self.client)


    def bluetooth_stream(self):
        count = 0
        try:
            while True:
                send_data = ''
                # Receivng the data.
                data = self.client.recv(1024) # 1024 is the buffer size.
                print('Bluetooth Data : ' + str(data))
                data = str(data)
                lines = data.split('\n')
                for item in lines:
                    pair = item.split(' ')
                    if(pair[0] == 'speed_command'):
                        self.p.ChangeDutyCycle(float(pair[1]))
                        send_data = str(pair[1])
                    elif(pair[0] == 'angle_command'):
                        send_data = (str(pair[1]))
                #~ if (data == b'r' or data == b's'):
                    #~ GPIO.output(self.red_led_pin, True)
                    #~ send_data = "Red light is on"
                    #~ print(send_data)
                #~ elif(data == b'y'):
                    #~ count = 10
                    #~ GPIO.output(self.yellow_led_pin, True)
                    #~ send_data = 'Yellow light is on'
                #~ elif(data == b'g'):
                    #~ count = 10
                    #~ GPIO.output(self.green_led_pin, True)
                    #~ send_data = "Green light is on"
                #~ elif (data == b'0' and count < 0):
                    #~ GPIO.output(self.red_led_pin, False)
                    #~ GPIO.output(self.yellow_led_pin, False)
                    #~ GPIO.output(self.green_led_pin, False)
                    #~ send_data = "Light Off "
                #~ else:
                    #~ send_data = "waiting for stoplight"
                    #~ GPIO.output(red_led_pin, False)
                    #~ GPIO.output(yellow_led_pin, False)
                    #~ GPIO.output(green_led_pin, False)
                    #~ send_data = "Light Off "
                #~ # Sending the data.a
                self.client.send(send_data)
                count-=1
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            # Making all the output pins LOW
            GPIO.cleanup()
            # Closing the client and server connection
            self.client.close()
            self.server.close()
    print('End of Bluetooth')
