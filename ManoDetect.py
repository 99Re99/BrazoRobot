import cv2
import numpy as np
import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
import PoseModule as pm
import socket

cap = cv2.VideoCapture(0)
#cap=cv2.VideoCapture(1)
#cap = cv2.VideoCapture('Pose.mp4')

success, img3 = cap.read()
h, w, _ = img3.shape
detector3 = HandDetector(detectionCon=0.8, maxHands=2)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)


detector2 = cvzone.HandDetector(maxHands=1, detectionCon=0.7)
mySerial = cvzone.SerialObject("COM3", 9600, 1)
output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (640, 480))
while True:
        #identifica mano derecha e izquierda
    # Get image frame
    success, img3 = cap.read()
    # Find the hand and its landmarks
    hands, img3 = detector3.findHands(img3)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    data = []

    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), serverAddressPort)
    success, img = cap.read()
    #img = cv2.resize(img, (1280, 720))



    success,img2 = cap.read()  # success agregar?
    detector2.findHands(img2)
    lmList2, bbox = detector2.findPosition(img2)
#detecta la posicion de los dedos
    if lmList2:
        fingers = detector2.fingersUp()
        print(fingers)
        mySerial.sendData(fingers)
        output.write(img2)
        time.sleep(0.1)
    cv2.imshow("Imagen2", img2)

#Detecta el angulo del brazo
    # print(lmList)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.waitKey(1)
