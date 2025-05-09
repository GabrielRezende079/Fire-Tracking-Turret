# 🔥 Fogo Tracker com Arduino + YOLO + OpenCV

Este projeto é uma torreta rastreadora que segue **chamas de fogo** utilizando uma webcam, **Arduino com servo motores** e **visão computacional** com OpenCV e YOLO.

O sistema detecta e rastreia o objeto (chama) na tela e movimenta os servos da torreta para segui-lo em tempo real.

> ✅ Baseado no excelente vídeo do [Owen O'Brien](https://youtu.be/a_UiYOO-Sdw?si=6ceBJHbI4weYNGXD). Adaptei o código para funcionar com **fogo**, usando um modelo YOLO treinado para isso.

---

## 🛠 Tecnologias utilizadas

- Python 3.12
- OpenCV
- Ultralytics YOLO
- Arduino (Servo motor)
- Comunicação Serial (pySerial)

---

## 🔩 Hardware necessário

- Arduino Uno (ou similar)
- 2 servos motores
- Webcam (interna ou externa)
- Suporte tipo pan-tilt ou torreta
- Cabo USB para comunicação com o PC

---

## 🧠 Como funciona

1. O Python detecta chama usando OpenCV ou YOLO.
2. As coordenadas da detecção são enviadas via porta serial para o Arduino.
3. O Arduino converte as coordenadas em ângulos e move os servos da torreta para mirar no alvo.

---
### Instalando as bibliotecas:

```bash
pip install ultralytics opencv-python pyserial numpy
```

## 📂 Estrutura do Projeto
```
├── face_tracker.py          # Rastreador de rosto usando OpenCV
├── fire_tracker.py          # Rastreador de fogo usando YOLO
├── Arduino_FaceFire_Tracker.ino  # Código Arduino
```
