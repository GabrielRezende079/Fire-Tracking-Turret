#include <Servo.h>
String inputString = "";
bool stringComplete = false;

Servo left_right;
Servo up_down;

const int bombaPin = 11;  // Pino da bomba

void setup() {
  left_right.attach(10);
  up_down.attach(9);
  pinMode(bombaPin, OUTPUT);
  digitalWrite(bombaPin, LOW);  // Bomba desligada inicialmente
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
    // Comando especial para ligar/desligar a bomba
    if (inputString == "ON") {
      digitalWrite(bombaPin, HIGH);  // Liga a bomba
    } else if (inputString == "OFF") {
      digitalWrite(bombaPin, LOW);   // Desliga a bomba
    } else {
      // Movimento da torre
      int commaIndex = inputString.indexOf(',');
      if (commaIndex != -1) {
        int x_axis = inputString.substring(0, commaIndex).toInt();
        int y_axis = inputString.substring(commaIndex + 1).toInt();

        int y = map(y_axis, 0, 1080, 180, 0);
        int x = map(x_axis, 0, 1920, 180, 0);

        left_right.write(x);
        up_down.write(y);
      }
    }

    inputString = "";
    stringComplete = false;
  }

  delay(10);
}
