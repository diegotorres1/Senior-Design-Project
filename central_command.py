# Author : Diego Torres
# Description : Main for control system
# Date of Modification : 3/2/2018

# Libraries
from tkinter import *
import cv2
import threading
from central_command_gui import App
import time

# app_worker call worker for gui
def app_worker():
    root = Tk()
    app = App(root)
    root.mainloop()

def main():
    app_worker()

if __name__ == '__main__':
    main()
    print('Autonomous Vehicle Test')
