#include <Wire.h>
#include <ArduinoJson.h>
#include <I2Cdev.h>
#include <DHT.h>
#include <SoftwareSerial.h>
#include <Adafruit_BMP280.h>
#include <MQ135.h>

// Definicion de los pines para los sensores
#define PIN_DHT 4
#define PIN_MQ A0
#define PIN_UV A1

#define TYPE_DHT DHT11

// Inicializacion de los objetos para los sensores
DHT dht(PIN_DHT, TYPE_DHT);
Adafruit_BMP280 bmp;
MQ135 mq(PIN_MQ);

// Inicializacion de las variables de medicion
float P0;
double humedad;
double temperaturaDHT;
double temperaturaBMP;
double co2;
float presion;
double altitud;
float indiceUV;

// Inicializacion de los componentes necesarios para la comunicacion por XBee
SoftwareSerial xbee(2, 3); // rx(2) tx(3)
bool xbee_bootloader = true;
unsigned long tiempo = 0;
DynamicJsonDocument json(1024);

void setup() {
  xbee.begin(9600);
  Serial.begin(230400);
  xbee.println("B");
  delay(1000);

  dht.begin();
  bmp.begin(0x76);
  P0 = bmp.readPressure() / 100;
}

void loop() {
  humedad = dht.readHumidity();
  temperaturaDHT = dht.readTemperature();
  temperaturaBMP = bmp.readTemperature();
  co2 = mq.getCorrectedPPM(temperaturaDHT, humedad);
  presion = bmp.readPressure() / 100.0F;
  altitud = bmp.readAltitude(P0);
  indiceUV = obtenerIndiceUV(analogRead(PIN_UV));

  generarJson();

  if (configuracionBaud()) {
    // LA B MAGICA para configurar el modulo en ByPass
    xbee.println("B");
  } else {
    serializeJson(json, xbee);
    xbee.println();
  }
  
  serializeJson(json, xbee);
  
  delay(100);
}

void generarJson() {
  json["carga"] = "ili";
  json["tiempo"] = millis() / 1000;
  json["humedad"] = humedad;
  json["temperaturaDHT"] = temperaturaDHT;
  json["temperaturaBMP"] = temperaturaBMP;
  json["co2"] = co2;
  json["presion"] = presion;
  json["altitud"] = altitud;
  json["indiceUV"] = indiceUV;
}

bool configuracionBaud() {
  tiempo = millis();
  // Validaciones para configurar la cantidad de baudios (tiempo mayor a 2 segundos y que la B magica aun se este mostrando)
  if (tiempo >= 2000 && xbee_bootloader) {
    // Declaramos xbee_bootloader en false despues de haber accedido al bootloader y 
    // configurar el modulo en modo Transparente en la funcion loop para dar paso al mensaje que queremos enviar
    xbee_bootloader = false;
    // Declaramos la comunicacion del xbee a 230400 para poder transmitir datos
   // xbee.begin(230400);
    Serial.println("Baudios configurados a 230400");
  }
  return xbee_bootloader;
}

float obtenerIndiceUV(float lecturaAnalogica) {
  float voltaje = lecturaAnalogica * (5.0 / 1023.0);

  if (voltaje < 227) {
    return 0;
  } else if (voltaje >= 227 && voltaje <= 317) {
    return 1;
  } else if (voltaje >= 318 && voltaje <= 407) {
    return 2;
  } else if (voltaje >= 408 && voltaje <= 502) {
    return 3;
  } else if (voltaje >= 503 && voltaje <= 605) {
    return 4;
  } else if (voltaje >= 606 && voltaje <= 695) {
    return 5;
  } else if (voltaje >= 696 && voltaje <= 794) {
    return 6;
  } else if (voltaje >= 795 && voltaje <= 880) {
    return 7;
  } else if (voltaje >= 881 && voltaje <= 975) {
    return 8;
  } else if (voltaje >= 976 && voltaje <= 1078) {
    return 9;
  } else if (voltaje >= 1079 && voltaje <= 1171) {
    return 10;
  } else {
    return 11;
  }
}
