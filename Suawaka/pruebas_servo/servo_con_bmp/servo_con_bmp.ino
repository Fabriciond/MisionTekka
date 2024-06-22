#include <Servo.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;
Servo servo;

float presion, altitud, presion_inicial;
bool servoHaSidoActivado = false;

void setup() {
  Serial.begin(9600);
  
  servo.attach(9);
  bmp.begin(0x76);

  presion_inicial = bmp.readPressure() / 100.0;
}

void loop() {
  altitud = bmp.readAltitude(presion_inicial);

  Serial.println(String(altitud));
  
  if (altitud >= 1 && !servoHaSidoActivado) {
    servoHaSidoActivado = true;
    servo.write(0);
    Serial.println("Servo 0");
    delay(2000);

    servo.write(90);
    Serial.println("Servo 90");
    delay(1000);

//    servo.write(0);
//    Serial.println("Servo 0");
//    delay(1000);

  }

  delay(1000);
}
