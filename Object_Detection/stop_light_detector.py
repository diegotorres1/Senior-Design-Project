import cv2 as cv2
import sys
import numpy as np
import imutils
import os
class stop_light_detector():
    def __init__(self):
        if(__debug__):
            print('stop_light_detector created')

        self.stop_light_cascade = cv2.CascadeClassifier('TrafficLight_HAAR_16Stages.xml')
        self.stop_sign_cascade = cv2.CascadeClassifier('Stopsign_HAAR_19Stages.xml')
        # self.stop_light_cascade = cv2.CascadeClassifier('../object_detect/TrafficLight_HAAR_16Stages.xml')
        # self.stop_sign_cascade = cv2.CascadeClassifier('../object_detect/Stopsign_HAAR_19Stages.xml')


    def detect_stop(self,image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            w = 0
            h = 0
            stop_sign = self.stop_sign_cascade.detectMultiScale(gray, 1.03, 5)
            # print('stop_sign_check : ' + str(stop_sign))
            for (x,y,w,h) in stop_sign:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),4)
            return [image,(w,h)]
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return [image,(None,None)]

    def detect_stoplight(self, image):
        try:
            #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)# XXX:
            c = None
            stop_light = self.stop_light_cascade.detectMultiScale(image, 1.005, 5)
            # print(stop_light)
            c = '0'
            for (x,y,w,h) in stop_light:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),4)
                [image,c] = self.detect_stoplight_color(image,x,y,w,h)
            return [image,c]
        except Exception as e:
            print(e)
            return [image, '0']


    def detect_stoplight_color(self,image,x,y,w,h):
        try:
            height, width, channels = image.shape
            blurred = cv2.GaussianBlur(image, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

            ##draw rectangle binary

            # cv2.rectangle(hsv,(0,0),(x,height),(0,0,0),-1)
            # cv2.rectangle(hsv,(0,0),(width,y),(0,0,0),-1)
            # cv2.rectangle(hsv,(x+w,0),(width,height),(0,0,0),-1)
            # cv2.rectangle(hsv,(0,height),(width,height-y),(0,0,0),-1)


            lower_red = np.array([166, 84, 141])
            upper_red = np.array([186,255,255])

            lower_green = np.array([66, 122, 129])
            upper_green = np.array([86,255,255])

            lower_yellow = np.array([23, 59, 119])
            upper_yellow = np.array([54,255,255])


            #obtain masks
            red_mask = cv2.inRange(hsv, lower_red, upper_red)
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            #erode and dilate masks
            red_mask = cv2.erode(red_mask, None, iterations=2)
            red_mask = cv2.dilate(red_mask, None, iterations=2)

            green_mask = cv2.erode(green_mask, None, iterations=2)
            green_mask = cv2.dilate(green_mask, None, iterations=2)

            yellow_mask = cv2.erode(yellow_mask, None, iterations=2)
            yellow_mask = cv2.dilate(yellow_mask, None, iterations=2)

            red_cnts = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            red_cnts = imutils.grab_contours(red_cnts)

            green_cnts = cv2.findContours(green_mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            green_cnts = imutils.grab_contours(green_cnts)

            yellow_cnts = cv2.findContours(yellow_mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            yellow_cnts = imutils.grab_contours(yellow_cnts)
            light = '0'
            c = None
            try:
                r = max(red_cnts, key=cv2.contourArea)
                ((x1, y1), radius) = cv2.minEnclosingCircle(r)
                if(x1 < x and x1 > (x + w) and y1 < y and y1 > (y+h)):
                    r = None
            except:
                print('not r')
                r = None

            try:
                g = max(green_cnts, key=cv2.contourArea)
                ((x1, y1), radius) = cv2.minEnclosingCircle(g)
                if(x1 < x and x1 > (x + w) and y1 < y and y1 > (y+h)):
                    g = None
            except:
                print('not g')
                g = None
            try:
                y = max(yellow_cnts, key=cv2.contourArea)
                ((x1, y1), radius) = cv2.minEnclosingCircle(y)
                if(x1 < x and x1 > (x + w) and y1 < y and y1 > (y+h)):
                    y = None
            except:
                y = None
                print('not y')




            if(r is not None):
                c = r
                light = 'r'
            elif(g is not None):
                light = 'g'
                c = g
            elif(y is not None):
                light = 'y'
                c = y
            elif(r is not None and g is not None and y is not None):
                #light decision tree
                light = ''
                #red light
                if(r.countourArea > g.contourArea and r.countourArea > y.contourArea):
                    light = 'r'
                    c = r
                #green light
                elif(g.countourArea > r.contourArea and g.countourArea > y.contourArea):
                    light = 'g'
                    c = g
                #yellow light
                elif(y.countourArea > r.contourArea and y.countourArea > g.contourArea):
                    light = 'y'
                    c = y

            #draw the circle around the stoplight
            if(c is not None):
                print(light)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                if radius > 5:
                    cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            return [image,light]
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return [image,'0']
