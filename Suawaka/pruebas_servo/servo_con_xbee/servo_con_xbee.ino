#include <SoftwareSerial.h>
#include <Adafruit_BMP280.h>
#include <Servo.h>

Adafruit_BMP280 bmp;
SoftwareSerial xbee(2, 3);// rx(2)/tx(3)
Servo servo;

unsigned long tiempo = 0;//Declaracion de la variable del tiempo
bool magicB = true; //Booleano para controlar la entrada y salida del bootloader

float presion, altitud, presion_inicial;
bool servoHaSidoActivado = false;

void setup() {
  xbee.begin(9600); //En un principio el xbee se configura en 9600 baudios para poder comunicarse con el bootloader
  Serial.begin(230400);
  xbee.println("B");
  delay(1000);

  bmp.begin(0x76);
  presion_inicial = bmp.readPressure() / 100.0;
  
}

void loop() {
  altitud = bmp.readAltitude(presion_inicial);
  
  if (configuracionBaud()) {
    xbee.println("B");  //LA B MAGICA para configurar el modulo en ByPass
  } else {
    xbee.println(String(altitud));    
  }

  if (altitud >= 1 && !servoHaSidoActivado) {
    servo.attach(9);
    servoHaSidoActivado = true;
    servo.write(0);
    Serial.println("Servo 0");
    delay(2000);

    servo.write(90);
    Serial.println("Servo 90");
    delay(1000);

    servo.detach();
  }

  delay(200);
}


bool configuracionBaud() {
  tiempo = millis();                      //Variable para medir el tiempo transcurrido
  if (tiempo > 1000 && magicB == true) {  //Validaciones para configurar la cantidad de baudios (tiempo mayor a 1000 milisegundo y que la B magica aun se este mostrando )
    magicB = false;                       //Declaramos magicB en false despues de haber accedido al bootloader y configurar el modulo en modo Transparente en la funcion loop para dar paso al mensaje que queremos enviar
    xbee.begin(230400);                   //Declaramos la comunicacion del xbee a 230400 para poder transmitir datos
    Serial.println("Baudios configurados a 230400");
  }
  return magicB;
}
