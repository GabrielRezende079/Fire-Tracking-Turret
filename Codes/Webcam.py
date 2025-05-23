import cv2
import numpy as np
import serial
import time
from ultralytics import YOLO

arduinoData = serial.Serial('COM3', 9600)
model = YOLO("C:/Users/Pichau/Documents/MeusProj/Fire-Tracking-Turret/Codes/runs/detect/train3/weights/best.pt")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Controle da bomba
tempo_jato = 1  # segundos entre ON/OFF
espera_para_ligar = 2  # segundos antes de começar a jatear
inicio_fogo = None
ultimo_jato = 0
estado_bomba = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    results = model(frame)

    fogo_detectado = False
    tempo_atual = time.time()

    for r in results:
        boxes = r.boxes.xyxy
        if len(boxes) > 0:
            fogo_detectado = True

            if inicio_fogo is None:
                inicio_fogo = tempo_atual

            box = boxes[0]
            x1, y1, x2, y2 = map(int, box)
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            cy_invertido = h - cy

            coordinates = f"{cx},{cy_invertido}\r"
            arduinoData.write(coordinates.encode())
            print(f"Enviado: X{cx} Y{cy_invertido}")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
            cv2.putText(frame, f"{cx},{cy}", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    if fogo_detectado:
        if tempo_atual - inicio_fogo >= espera_para_ligar:
            if tempo_atual - ultimo_jato >= tempo_jato:
                if estado_bomba:
                    arduinoData.write("OFF\r".encode())
                    print("Bomba DESLIGADA (intermitente)")
                else:
                    arduinoData.write("ON\r".encode())
                    print("Bomba LIGADA (intermitente)")
                estado_bomba = not estado_bomba
                ultimo_jato = tempo_atual
    else:
        if estado_bomba:
            arduinoData.write("OFF\r".encode())
            print("Bomba DESLIGADA (fim da detecção)")
        inicio_fogo = None
        estado_bomba = False

    cv2.imshow("Fire Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduinoData.close()
cv2.destroyAllWindows()
