
import cv2
import numpy as np
from dataclasses import dataclass

@dataclass
class Geometria():
    objEsquina: int
    imgCanny: np.ndarray
    x: int
    y: int
    w: int
    h: int

    def __post_init__(self):
        if self.objEsquina == 3:
            self.objectType = "Triangulo"
        elif self.objEsquina == 4:
            aspecto = self.w / float(self.h)
            if aspecto > 0.95 and aspecto < 1.05:
                self.objectType = "cuadrado"
            else:
                self.objectType = "Rectangulo"
        elif self.objEsquina > 4:
            self.objectType = "Circulo"
        else:
            self.objectType = "Nada"

def obContorno(img):
    contorno, jerarquia = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contorno:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:
            cv2.drawContours(frame, cnt, -1, (0, 0, 255), 3)
            perimetro = cv2.arcLength(cnt, True)
            print(perimetro)
            aprrox = cv2.approxPolyDP(cnt, 0.02 * perimetro, True)
            print(len(aprrox))
            objEsquina = len(aprrox)
            x, y, w, h = cv2.boundingRect(aprrox)
            geometria = Geometria(objEsquina, imgCanny, x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, str(geometria.objectType), (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 0, 0), 2)

print("\nSelecciona una opción: \nA) VideoFigs.mp4\nB) Camara")
opcion = input("Seleccione la opción A/B: ")
if opcion == 'A':
    cap = cv2.VideoCapture("videoFigs.mp4")
elif opcion == 'B':
    cap = cv2.VideoCapture(0)
else:
    print("No existe esa opción")
while cap.isOpened():
    ret, frame = cap.read()
    imgCanny = frame.copy()
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    obContorno(imgCanny)
    cv2.imshow("Figuras geometricas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
