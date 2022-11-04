import cvzone
import cv2
import time
import PoseEstimacion

cap = cv2.VideoCapture(0)
detectorM = cvzone.HandDetector(maxHands=1, detectionCon=0.7)
mySerial = cvzone.SerialObject("COM3", 9600, 1)
output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (640, 480))

while True:
    success, img = cap.read()
    detectorM.findHands(img)
    lmList2, bbox = detectorM.findPosition(img)
    if lmList2:
        fingers = detectorM.fingersUp()
        print(fingers) #Revisado
        mySerial.sendData(fingers)
        output.write(img)
        time.sleep(0.1)
    cv2.imshow("Imagen", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows(1)