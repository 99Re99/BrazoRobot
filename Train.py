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
#tipo de mano
success, img3 = cap.read()
h, w, _ = img3.shape
detector3 = HandDetector(detectionCon=0.8, maxHands=2)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
#brazo variables
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
#mano
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

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

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
    #cv2.imshow("Imagen", img2)

#Detecta el angulo del brazo
    # print(lmList)
    if len(lmList) != 0:

        angle = detector.findAngle(img, 12, 14, 16)

        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (220, 310), (650, 100))
        print(angle, per)

        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        #print(count)

        # Dibujo barra
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)

        # Contador
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 255), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                    (255, 255, 255), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 0, 0), 5)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #cv2.imshow("Image", img)
    cv2.waitKey(1)
