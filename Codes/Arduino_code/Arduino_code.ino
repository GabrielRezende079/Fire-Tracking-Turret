#include <Servo.h>
String inputString = "";
bool stringComplete = false;

Servo left_right;
Servo up_down;

void setup() {
  left_right.attach(10);
  up_down.attach(9);
  Serial.begin(9600);
}

void loop() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\r') {
      stringComplete = true;
      break;
    } else {
      inputString += inChar;
    }
  }

  if (stringComplete) {
    int commaIndex = inputString.indexOf(',');
    if (commaIndex != -1) {
      int x_axis = inputString.substring(0, commaIndex).toInt();
      int y_axis = inputString.substring(commaIndex + 1).toInt();

      int y = map(y_axis, 0, 1080, 180, 0); // inverte eixo Y
      int x = map(x_axis, 0, 1920, 180, 0);

      left_right.write(x);
      up_down.write(y);
    }

    inputString = "";
    stringComplete = false;
  }

  delay(10);
}
