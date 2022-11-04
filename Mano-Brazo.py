import cvzone
import cv2
import time

cap = cv2.VideoCapture(0)
detector2 = cvzone.HandDetector(maxHands=1, detectionCon=0.7)
mySerial = cvzone.SerialObject("COM3", 9600, 1)
output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (640, 480))

while True:
    success, img2 = cap.read()
    detector2.findHands(img2)
    lmList2, bbox = detector2.findPosition(img2)
    if lmList2:
        fingers = detector2.fingersUp()
        print(fingers)
        mySerial.sendData(fingers)
        output.write(img2)
        time.sleep(0.1)
    cv2.imshow("Imagen", img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()