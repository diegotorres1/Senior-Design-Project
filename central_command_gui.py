# Author : Diego Torres
# Description : App for control system called by Main
# Date of Modification : 3/2/2018

# Libraries
from tkinter import *
import time
import threading
import sys
sys.path.append("UDP/recv/")
from server import server
import os

class App:
    #NEED TO edit the thread worker
    def UDP_server_worker(self):
        time.sleep(2)
        server_ip = '192.168.0.13'
        # server_ip = '169.234.47.26'
        sensor_port = 8005
        video_port = 8006
        s = server(server_ip, video_port, sensor_port)

        while(True):
            try:
                with open('Cross_Talk/transmit_f.txt','w') as f:
                    f.write(
                    'speed_command' + ' ' + str(self.speed) + '\n'
                    'angle_command' + ' ' + str(self.angle)
                    )
                f.close()
                time.sleep(.01)
            except Exception as e:
                print(e)
                print(os.getcwd())
                print('transmit_f can not find')
                pass
            ##object detection
            try:
                with open('Cross_Talk/receive_f.txt','r') as f:
                    data = f.read()
                f.close()
                self.detected_label.config(text=data)
                time.sleep(.01)
            except:
                # print('receive_f can not find')
                pass
            #sensed values
            try:
                with open('Cross_Talk/receive_s.txt','r') as f:
                    data = f.read()
                f.close()
                measured_dict = {}
                ##split into individual lines
                lines = data.split('\n')
                ##split into variable and value
                for item in lines:
                    pair = item.split(',')
                    measured_dict[pair[0]] = pair[1]


                if 'speed_measure' in measured_dict:
                    self.angle_actual_label.config(text=measured_dict['speed_measure'])
                if 'angle_measure' in measured_dict:
                    self.speed_actual_label.config(text = measured_dict['angle_measure'])
                time.sleep(.01)
            except:
                # print('data_transfer_files')
                pass





    def __init__(self, master):
        #thread
        t = threading.Thread(target = self.UDP_server_worker)
        t.daemon = True
        t.start()



        self.object_str  = 'NaN'
        self.speed = 0
        self.speed_actual = 0
        self.angle = 0
        self.angle_actual = 0

        #main
        self.main_frame = Frame(master)
        self.main_frame.pack()

        #speed
        self.speed_frame = Frame(self.main_frame)
        self.speed_frame.pack(side = BOTTOM)
        self.speed_value_frame = Frame(self.speed_frame)
        self.speed_value_frame.pack(side = BOTTOM)

        #angle
        self.angle_frame = Frame(self.main_frame)
        self.angle_frame.pack(side = BOTTOM)
        self.angle_value_frame = Frame(self.angle_frame)
        self.angle_value_frame.pack(side = BOTTOM)

        #traffic signs detected
        self.detection_frame = Frame(self.main_frame)
        self.detection_frame.pack(side = TOP)



        #MAIN
        self.button = Button(self.main_frame,text="SHUTDOWN", fg="red",command=self.main_frame.quit)
        self.button.pack(side=LEFT)



        #SPEED CONTROL
        self.speed_label = Label(self.speed_frame, text="Speed Controls")
        self.speed_label.pack(side=TOP)

        self.speed_desired_label = Label(self.speed_value_frame, text=self.speed)
        self.speed_desired_label.pack(side=LEFT)
        self.speed_actual_label = Label(self.speed_value_frame, text=self.speed_actual)
        self.speed_actual_label.pack(side=RIGHT)


        self.increment_speed_button = Button(self.speed_frame,text="+",command=self.increment_speed)
        self.increment_speed_button.pack(side=LEFT)
        self.decrement_speed_button = Button(self.speed_frame,text="-",command=self.decrement_speed)
        self.decrement_speed_button.pack(side=LEFT)
        self.speed_entry = Entry(self.speed_frame, width=50)
        self.speed_entry.pack(side=RIGHT)
        self.submit_speed_button = Button(self.speed_frame,text="submit",command=self.submit_speed)
        self.submit_speed_button.pack(side=RIGHT)

        #STEERING CONTROL
        self.angle_label = Label(self.angle_frame, text="Steering Controls")
        self.angle_label.pack(side=TOP)

        self.angle_desired_label = Label(self.angle_value_frame, text=self.angle)
        self.angle_desired_label.pack(side=LEFT)
        self.angle_actual_label = Label(self.angle_value_frame, text=self.angle_actual)
        self.angle_actual_label.pack(side=RIGHT)

        self.increment_angle_button = Button(self.angle_frame,text="+",command=self.increment_angle)
        self.increment_angle_button.pack(side=LEFT)
        self.decrement_angle_button = Button(self.angle_frame,text="-",command=self.decrement_angle)
        self.decrement_angle_button.pack(side=LEFT)
        self.angle_entry = Entry(self.angle_frame, width=50)
        self.angle_entry.pack(side=RIGHT)
        self.submit_speed_button = Button(self.angle_frame,text="submit",command=self.submit_angle)
        self.submit_speed_button.pack(side=RIGHT)

        #Objects

        self.detection_label = Label(self.detection_frame,text = "Objects Detected")
        self.detection_label.pack(side = TOP)
        self.detected_label = Label(self.detection_frame,text = self.object_str)
        self.detected_label.pack(side = BOTTOM)



    ############################################################################
    # Control Functions : Start
    ############################################################################
    #Speed Control
    def increment_speed(self):
        self.speed += 1
        self.speed_desired_label.config(text=self.speed)

        print('speed : \t' + str(self.speed))
    def decrement_speed(self):
        self.speed -= 1
        self.speed_desired_label.config(text=self.speed)
        print('speed : \t' + str(self.speed))
    def submit_speed(self):
        try:
            self.speed = int(self.speed_entry.get())
            self.speed_desired_label.config(text=self.speed)
        except Exception as e:
            print(e)
            print('Invalid input is attempting to be submitted. Value must be an integer')
        print('speed : \t' + str(self.speed))


    #Angle Control
    def increment_angle(self):
        self.angle += 1
        self.angle_desired_label.config(text = self.angle)
        print('angle :\t' + str(self.angle))
    def decrement_angle(self):
        self.angle -= 1
        self.angle_desired_label.config(text = self.angle)
        print('angle : \t' + str(self.angle))
    def submit_angle(self):
        try:
            self.angle = int(self.angle_entry.get())
            self.angle_desired_label.config(text = self.angle)
        except Exception as e:
            print(e)
            print('Invalid input is attempting to be submitted. Value must be an integer')
        print('angle : \t' + str(self.angle))


    #Objects Detected

    ############################################################################
    # Control Functions : End
    ############################################################################
