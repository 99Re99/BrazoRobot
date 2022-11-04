import cvzone
import cv2
import time
import PoseModule as pm


cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.poseDetector()
cap = cv2.VideoCapture(0)
detectorM = cvzone.HandDetector(maxHands=1, detectionCon=0.7)
mySerial = cvzone.SerialObject("COM3", 9600, 1)
output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (640, 480))

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    detectorM.findHands(img)
    lmList2, bbox = detectorM.findPosition(img)
    if lmList2:
        fingers = detectorM.fingersUp()
        print(fingers) #Revisado
        mySerial.sendData(fingers)
        output.write(img)
        time.sleep(0.1)

    if len(lmList) != 0:
        print(lmList[14])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Imagen", img)
    cv2.waitKey(1)