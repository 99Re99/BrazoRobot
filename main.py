from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img3 = cap.read()
h, w, _ = img3.shape
detector3 = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:

    success, img3 = cap.read()

    hands, img3 = detector3.findHands(img3)
    # hands = detector.findHands(img, draw=False)
    data = []


    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), serverAddressPort)
        print(data)
    # Display
    cv2.imshow("Image", img3)
    cv2.waitKey(1)