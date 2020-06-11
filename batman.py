import cv2
import numpy as np
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
from PyQt5 import QtCore
from bloodPressure import bloodPressure
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
#from PyQt4 import QtTest
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
#import pyqtgraph as pg
import sys
import time
from apscheduler.triggers.interval import IntervalTrigger
import datetime
from process import Process
from webcam import Webcam
from video import Video
# from interface import waitKey, plotXY
def myfunc():
    global arr_sy
    global arr_dy
    global arr_hr
    global maximum_sy
    global maximum_dy
    global maximum_hr
    global minimum_sy
    global minimum_dy
    global minimum_hr
    global average_sy
    global average_dy
    global average_hr
    global len_me
    global sio
    if(average_hr == 0):
        maximum_sy = round(max(arr_sy), 3)
        minimum_sy = round(min(arr_sy), 3)
        average_sy = round(sum(arr_sy)/len(arr_sy), 3)
        maximum_dy = round(max(arr_dy), 3)
        minimum_dy = round(min(arr_dy), 3)
        average_dy = round(sum(arr_dy)/len(arr_dy), 3)
        maximum_hr = round(max(arr_hr), 3)
        minimum_hr = round(min(arr_hr), 3)
        average_hr = round(sum(arr_hr)/len(arr_hr), 3)
    else:
        arr_sy.append(maximum_sy)
        maximum_sy = round(max(arr_sy), 3)
        arr_sy.pop()
        arr_sy.append(minimum_sy)
        minimum_sy = round(min(arr_sy), 3)
        arr_sy.pop()
        average_sy = round(((average_sy*len_me)+sum(arr_sy))/(len(arr_sy)+len_me), 3)

        arr_dy.append(maximum_dy)
        maximum_dy = round(max(arr_dy), 3)
        arr_dy.pop()
        arr_dy.append(minimum_dy)
        minimum_dy = round(min(arr_dy), 3)
        arr_dy.pop()
        average_dy = round(((average_dy*len_me)+sum(arr_dy))/(len(arr_dy)+len_me), 3)

        arr_hr.append(maximum_hr)
        maximum_hr = round(max(arr_hr), 3)
        arr_hr.pop()
        arr_hr.append(minimum_hr)
        minimum_hr = round(min(arr_hr), 3)
        arr_hr.pop()
        average_hr = round(((average_hr*len_me)+sum(arr_hr))/(len(arr_hr)+len_me), 3)


    len_me = len(arr_hr) + len_me
    arr_hr = []
    arr_dy = []
    arr_hr = []
    sio.emit("heart.store", data={'jwt': str(jwt_me), "values": { 'avg': average_hr, "min": minimum_hr ,"max": maximum_hr}})
    sio.emit("blood.store", data={'jwt': str(jwt_me), "values": { 'avg': average_sy, "min": minimum_sy ,"max": maximum_sy, 'avg1': average_dy, "min1": minimum_dy ,"max1": maximum_dy}})
    #print(maximum_me, minimum_me, average_me)

#class for setting up all the functionality
class GUI:
    def __init__(self, vs, jwt, values):
        super(GUI,self).__init__()
        #self.initUI()
        self.webcam = vs
        self.values = values
        self.jwt = jwt
        self.sio = sio
        # self.video = Video()
        self.input = 0
        #self.dirname = ""
        print("Input: webcam")
        #self.statusBar.showMessage("Input: webcam",5000)
        #self.btnOpen.setEnabled(False)
        self.process = Process()
        #self.status = False
        self.frame = np.zeros((10,10,3),np.uint8)
        #self.plot = np.zeros((10,10,3),np.uint8)
        self.bpm = 0
#main thread for heart rate measurement
def main(gui):
    frame = gui.webcam.read()[1]
    gui.process.frame_in = frame
    gui.process.run()
    gui.frame = gui.process.frame_out #get the frame to show in GUI
    gui.bpm = gui.process.bpm #get the bpm change over the time
#TODO : Add code to upload bpm to the cloud
    gui.frame = cv2.cvtColor(gui.frame, cv2.COLOR_RGB2BGR)

    print("Freq: " + str(float("{:.2f}".format(gui.bpm))))
    if gui.process.bpms.__len__() >50:
        if(max(gui.process.bpms-np.mean(gui.process.bpms))<5): #show HR if it is stable -the change is not over 5 bpm- for 3s
            hr = float("{:.2f}".format(np.mean(gui.process.bpms)))
            print("Heart rate: " + str(hr) + " bpm")
            sio.emit('heart.ping', data={"jwt": str(gui.jwt), "value": str(hr)})
            bp = bloodPressure(hr,gui.values['age'],gui.values['sex'],gui.values['weight'],gui.values['height'])
            sio.emit('blood.ping', data={"jwt": str(gui.jwt), "value": (bp)})
            arr_sy.append(bp[0])
            arr_dy.append(bp[1])
            arr_hr.append(hr)
# start function
import time

# standard Python

def iAmBatman(videoservice, jwt0, values, sio1):
    global flag
    global sio
    global average_sy
    global average_hr
    global average_dy
    global len_me
    global arr_sy
    global arr_dy
    global arr_hr
    arr_sy = []
    arr_dy = []
    arr_hr = []
    flag = 0
    global jwt_me
    sio = sio1
    jwt_me = jwt0
    average_sy = 0
    average_dy = 0
    average_hr = 0
    len_me = 0
    trigger = IntervalTrigger(minutes=1)
    job = sched.add_job(myfunc, trigger)
    sched.start()
    #print(values)
    print("starting program")
    while(1):
        flag = 1
        if(flag):
            gui = GUI(videoservice, jwt0, values)
            while(1):
                try:
                    main(gui)
                except:
                    print("--------- Heart Rate detector could not find Region of interest ---------")
                    print("--------------- Readjust the Camera to include you FACE ------------")
                    print("-------------- Restarting Heart Rate detector --------------")
                    gui = GUI(videoservice, jwt0, values)
