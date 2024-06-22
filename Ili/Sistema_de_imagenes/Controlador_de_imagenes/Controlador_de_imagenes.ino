#include "esp_camera.h"
#include "Arduino.h"
#include "FS.h"
#include "SD_MMC.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "driver/rtc_io.h"
#include <EEPROM.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>

#define EEPROM_SIZE 1

#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27

#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

int numero_de_foto = 0;
int xbee_bootloader = false;
int tiempo = 0;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  Serial.begin(230400);
  delay(1000);

  camera_config_t configuracion_camara;
  configuracion_camara.ledc_channel = LEDC_CHANNEL_0;
  configuracion_camara.ledc_timer = LEDC_TIMER_0;
  configuracion_camara.pin_d0 = Y2_GPIO_NUM;
  configuracion_camara.pin_d1 = Y3_GPIO_NUM;
  configuracion_camara.pin_d2 = Y4_GPIO_NUM;
  configuracion_camara.pin_d3 = Y5_GPIO_NUM;
  configuracion_camara.pin_d4 = Y6_GPIO_NUM;
  configuracion_camara.pin_d5 = Y7_GPIO_NUM;
  configuracion_camara.pin_d6 = Y8_GPIO_NUM;
  configuracion_camara.pin_d7 = Y9_GPIO_NUM;
  configuracion_camara.pin_xclk = XCLK_GPIO_NUM;
  configuracion_camara.pin_pclk = PCLK_GPIO_NUM;
  configuracion_camara.pin_vsync = VSYNC_GPIO_NUM;
  configuracion_camara.pin_href = HREF_GPIO_NUM;
  configuracion_camara.pin_sscb_sda = SIOD_GPIO_NUM;
  configuracion_camara.pin_sscb_scl = SIOC_GPIO_NUM;
  configuracion_camara.pin_pwdn = PWDN_GPIO_NUM;
  configuracion_camara.pin_reset = RESET_GPIO_NUM;
  configuracion_camara.xclk_freq_hz = 2000000;
  configuracion_camara.pixel_format = PIXFORMAT_JPEG;
  configuracion_camara.frame_size = FRAMESIZE_QVGA;  // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
  configuracion_camara.jpeg_quality = 6;
  configuracion_camara.fb_count = 2;

  esp_err_t err = esp_camera_init(&configuracion_camara);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  if (!SD_MMC.begin()) {
    Serial.println("SD Card Mount Failed");
    return;
  }

  uint8_t cardType = SD_MMC.cardType();
  if (cardType == CARD_NONE) {
    Serial.println("No SD Card attached");
    return;
  }
}

void loop() {
  camera_fb_t *fb = NULL;

  fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }
  // initialize EEPROM with predefined size
  EEPROM.begin(EEPROM_SIZE);
  numero_de_foto = EEPROM.read(0) + 1;

  // Path where new picture will be saved in SD Card
  String path = "/picture" + String(numero_de_foto) + ".jpg";

  fs::FS &fs = SD_MMC;
  Serial.printf("Picture file name: %s\n", path.c_str());

  File file = fs.open(path.c_str(), FILE_WRITE);
  if (!file) {
    Serial.println("Failed to open file in writing mode");
  } else {
    file.write(fb->buf, fb->len);  // payload (image), payload length
    Serial.printf("Saved file to path: %s\n", path.c_str());
    EEPROM.write(0, numero_de_foto);
    EEPROM.commit();
  }
  file.close();

  File file2 = SD_MMC.open("/numeritos" + String(numero_de_foto) + ".txt", FILE_WRITE);

  if (file2) {
    for (int i = 0; i < fb->len; i++) {
      String numero = String(fb->buf[i]);
      file2.print(numero);
      file2.print(",");
      if (configuracionBaud()) {
        // LA B MAGICA para configurar el modulo en ByPass
        Serial.println("B");

      } else {
        Serial.print(numero);
        Serial.print(",");
        delay(20);
        
      }
    }
    file2.close();
  }


  esp_camera_fb_return(fb);

  // Turns off the ESP32-CAM white on-board LED (flash) connected to GPIO 4
  pinMode(4, OUTPUT);
  digitalWrite(4, LOW);
  rtc_gpio_hold_en(GPIO_NUM_4);

  delay(5000);
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
