from base import startMeUp
import cv2
from threading import Thread
capture_target=0

import time
import socketio
import time
from batman import iAmBatman, GUI
import cv2
from queue import Queue
from threading import Thread

#worker thread for heart rate
def thread_work(videostream, jwt, values):
    #print("start analysis:")
    iAmBatman(videostream, jwt, values, sio)

# standard Python
sio = socketio.Client()

@sio.event
def connect():
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
        # print(jwt)
        # sio.disconnect()

    else:
        print("Incorrect Credentials")
        sio.disconnect()

try:
    sio.disconnect()
except:
    pass

import cv2

cap1 = cv2.VideoCapture(0)
while(True):
	ret, frame = cap1.read()
	cv2.imshow('Press Q after adjusting the camera', frame) 
	if (cv2.waitKey(1) & 0xFF == ord('q')): 
		break

# cap1.release() 

cv2.destroyAllWindows() 

print("connected")
while(flag):
    sio.connect('http://ec2-100-26-9-144.compute-1.amazonaws.com:5000/')
    email = str(input("Email:"))
    password = str(input("Password:"))
    sio.emit('user.login', data={"email":str(email), "password":str(password)}, callback=call)
    sio.sleep(3)

#print("THROUGH")
#cap1 = cv2.VideoCapture(capture_target)
worker1 = Thread(target=startMeUp, args=(cap1, jwt, sio))
worker1.setDaemon(True)
worker1.start()

worker2 = Thread(target=thread_work, args=(cap1, jwt, values,))
worker2.setDaemon(True)
worker2.start()

worker1.join()
worker2.join()

# while(1):
#     # if((not(worker1.is_alive()))):
#     #     print("--------- Respiratory detector could not find Region of interest ---------")
#     #     print("--------------- Readjust the Camera to include you CHEST AREA ------------")
#     #     print("------------Restarting Respiratory detector --------------")
#     #     worker1 = Thread(target=startMeUp, args=(cap1, jwt, ))
#     #     worker1.setDaemon(True)
#     #     worker1.start()
#     #     time.sleep(3)
#
#     if((not(worker2.is_alive()))):
#         print("--------- Heart Rate detector could not find Region of interest ---------")
#         print("--------------- Readjust the Camera to include you FACE clearly ------------")
#         print("------------Restarting Heart Rate detector --------------")
#         worker2 = Thread(target=thread_work, args=(cap1, jwt, values,))
#         worker2.setDaemon(True)
#         worker2.start()
