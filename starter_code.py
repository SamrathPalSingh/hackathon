from base import startMeUp
import cv2
from threading import Thread
capture_target=0


import socketio
import time
from batman import iAmBatman, GUI
import cv2
from queue import Queue
from threading import Thread

#worker thread for heart rate
def thread_work(videostream, jwt, values):
    #print("start analysis:")
    iAmBatman(videostream, jwt, values)

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("connected")
    pass


@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    pass


flag = 1
jwt = ""
def call(data):
    if(data['success'] == True):
        global jwt
        global flag
        global values
        flag = 0
        jwt = (data['token'])
        age = (data['user']['age'])
        weight = (data['user']['weight'])
        height = (data['user']['height'])
        sex = (data['user']['sex'])
        values = { 'sex' : sex , 'height' : height, 'weight' : weight, 'age' : age}
        sio.disconnect()
    else:
        print("Incorrect Credentials")
        sio.disconnect()



while(flag):
    sio.connect('http://deloitte-hack.herokuapp.com/')
    email = str(input("Email:"))
    password = str(input("Password:"))
    sio.emit('user.login', data={"email":str(email), "password":str(password)}, callback=call)
    sio.wait()


cap1 = cv2.VideoCapture(capture_target)
worker = Thread(target=startMeUp, args=(cap1, jwt, ))
worker.setDaemon(True)
worker.start()

worker = Thread(target=thread_work, args=(cap1, jwt, values, ))
worker.setDaemon(True)
worker.start()

worker.join()
