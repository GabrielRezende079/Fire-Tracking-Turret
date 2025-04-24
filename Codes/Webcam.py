import cv2
import numpy as np
import serial
from ultralytics import YOLO

# Conectar ao Arduino (ajuste conforme sua porta)
arduinoData = serial.Serial('COM3', 9600)

# Carregar o modelo YOLO treinado para fogo
model = YOLO("runs/detect/train3/weights/best.pt")

# Captura da webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape  # Altura e largura do frame

    # Realiza a detecção
    results = model(frame)

    for r in results:
        boxes = r.boxes.xyxy  # Coordenadas das detecções
        if len(boxes) > 0:
            # Pega a primeira detecção (você pode melhorar isso com a maior área, por exemplo)
            box = boxes[0]
            x1, y1, x2, y2 = map(int, box)
            cx = int((x1 + x2) / 2)  # Centro da caixa (x)
            cy = int((y1 + y2) / 2)  # Centro da caixa (y)

            # Inverter o eixo Y para servo (como discutido)
            cy_invertido = h - cy

            # Envia dados para Arduino
            coordinates = f"{cx},{cy_invertido}\r"
            arduinoData.write(coordinates.encode())
            print(f"Enviado: X{cx} Y{cy_invertido}")

            # Exibe a detecção e posição
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
            cv2.putText(frame, f"{cx},{cy}", (cx+10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Exibir frame
    cv2.imshow("Fire Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduinoData.close()
cv2.destroyAllWindows()
