#include <ArduinoJson.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>
#include <Adafruit_BMP280.h>
#include <Servo.h>

Adafruit_MPU6050 mpu;
Adafruit_BMP280 bmp;
Servo servo;

double temperatura, presion, altitud, presion_inicial;
float aceleracion_x, aceleracion_y, aceleracion_z;
String cadena = "";

bool servoHaSidoActivado = false;

// Inicializacion de los componentes necesarios para la comunicacion por XBee
SoftwareSerial xbee(2, 3);  // rx(2) tx(3)
bool xbee_bootloader = true;
unsigned long tiempo = 0;
DynamicJsonDocument json(1024);

void setup() {
  xbee.begin(9600);
  Serial.begin(9600);
  xbee.println("B");
  delay(1000);
  bmp.begin(0x76);
  mpu.begin();
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  presion_inicial = bmp.readPressure() / 100;
  moverServo(0);
}

void loop() {
  sensors_event_t acelerometro, giroscopio, temp;
  mpu.getEvent(&acelerometro, &giroscopio, &temp);

  temperatura = bmp.readTemperature();
  presion = bmp.readPressure() / 100.0F;
  altitud = bmp.readAltitude(presion_inicial);

  aceleracion_x = acelerometro.acceleration.x;
  aceleracion_y = acelerometro.acceleration.y;
  aceleracion_z = acelerometro.acceleration.z;

  cadena = "t" + String(temperatura) + "," + "p" + String(presion) + "," + "a" + String(altitud) + "," + "x" + String(aceleracion_x) + "," + "y" + String(aceleracion_y) + "," + "z" + String(aceleracion_z);

  Serial.println(cadena);
  if (altitud >= 1 && !servoHaSidoActivado) {
    moverServo(90);
    servoHaSidoActivado = true;
  }

  if (configuracionBaud()) {
    // LA B MAGICA para configurar el modulo en ByPass
    xbee.println("B");
  } else {
    xbee.println(cadena);
  }

  if (xbee.available()) {
    String txt = xbee.readString();
    Serial.println(txt);
    if (txt == "paro_emergencia") {
      moverServo(90);
      Serial.print("se desplego");
    }
  }

  delay(200);
}

bool configuracionBaud() {
  tiempo = millis();
  // Validaciones para configurar la cantidad de baudios (tiempo mayor a 2 segundos y que la B magica aun se este mostrando)
  if (tiempo >= 6000 && xbee_bootloader) {
    // Declaramos xbee_bootloader en false despues de haber accedido al bootloader y
    // configurar el modulo en modo Transparente en la funcion loop para dar paso al mensaje que queremos enviar
    xbee_bootloader = false;
    // Declaramos la comunicacion del xbee a 230400 para poder transmitir datos
    //xbee.begin(230400);
    Serial.println("Baudios configurados a 230400");
  }
  return xbee_bootloader;
}
void moverServo(int grados) {
  servo.attach(9);
  delay(200);
  servo.write(grados);
  delay(200);
  servo.detach();
}