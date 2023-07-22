import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
from math import sqrt

from pyfirmata import Arduino,SERVO,util
from time import sleep
 
from cvzone.HandTrackingModule import HandDetector


port = "com8"
pin = 10
board = Arduino(port)



cap = cv2.VideoCapture(0)

fw = 1280
fh = 720

cap.set(3, fw)
cap.set(4, fh)
detector = HandDetector(maxHands=1, detectionCon=0.8)

def highPin(pin):
    board.digital[pin].write(1)

def lowPin(pin):
    board.digital[pin].write(0)


def distance(cood1,cood2):
    return (((cood2[0]-cood1[0])**2)+((cood2[1]-cood1[1])**2))**0.5

def detechFinger(list):
    points = [8,12,16,5,17]    
    for p in points:
         cv2.circle(img, (list[p][0], list[p][1]),15, (255, 255, 255), cv2.FILLED)

    close_dist = distance(list[points[3]],list[points[4]])
    dist1 = distance(list[points[0]],list[points[1]])/close_dist
    dist2 = distance(list[points[1]],list[points[2]])/close_dist

    # print("distance 1  : ",dist1)
    # print("distance 2  : ",dist2)
    # print()

    if (1.34 < dist1 < 1.9) and (0.25 <dist2<0.54):
        print("one")
        highPin(13)
        lowPin(11)
        lowPin(9)
    elif (0.6 < dist1 < 1.07) and (1.34 <dist2<2.1):
        print("two")

        highPin(11)
        lowPin(13)
        lowPin(9)
    elif (0.43 < dist1 < 0.72) and (0.5 <dist2<0.76):
        print("three")

        highPin(9)
        lowPin(13)
        lowPin(11)
    else:
        print("Distance 1 : ",dist1)
        print("Distance 2 : ",dist2)
        print()



while True:
    # board.digital[11].write(1)
    # time.sleep(1)
    # board.digital[11].write(0)
    # time.sleep(1)
    
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hand,img = detector.findHands(img, draw=True)

    if hand:
        lmList = hand[0]["lmList"]
        detechFinger(lmList)




    cv2.imshow("Image", img)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break