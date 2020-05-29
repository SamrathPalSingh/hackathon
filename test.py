import cv2
webcam = cv2.VideoCapture(0)
print("Start camera")
while(1):
    #print("put frame")
    x=webcam.read()[1]
    cv2.imshow("Processed", x)
