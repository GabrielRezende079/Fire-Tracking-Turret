import cv2
import numpy as np
import serial
import time
from ultralytics import YOLO

arduinoData = serial.Serial('COM3', 9600)
model = YOLO("C:/Users/Pichau/Documents/MeusProj/Fire-Tracking-Turret/Codes/runs/detect/train3/weights/best.pt")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

bomba_ligada = False
ultimo_fogo_detectado = 0
tempo_espera = 3  # segundos antes de desligar a bomba

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    results = model(frame)

    fogo_detectado = False

    for r in results:
        boxes = r.boxes.xyxy
        if len(boxes) > 0:
            fogo_detectado = True
            ultimo_fogo_detectado = time.time()  # atualiza o tempo do último fogo detectado

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

    tempo_desde_ultimo_fogo = time.time() - ultimo_fogo_detectado

    if fogo_detectado and not bomba_ligada:
        arduinoData.write("ON\r".encode())
        bomba_ligada = True
        print("Bomba LIGADA")

    elif not fogo_detectado and bomba_ligada and tempo_desde_ultimo_fogo > tempo_espera:
        arduinoData.write("OFF\r".encode())
        bomba_ligada = False
        print("Bomba DESLIGADA")

    cv2.imshow("Fire Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduinoData.close()
cv2.destroyAllWindows()
