#include <DigiCDC.h>
#include <Adafruit_NeoPixel.h>

static const int LED_COUNT = 30;
static const int LED_PIN = 1;
static int IDX = 0;
static int pos = 0;

Adafruit_NeoPixel LEDS = Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  LEDS.begin();
  SerialUSB.begin();

  // set all to low red light
  for (int i = 0; i < LED_COUNT; i++) {
    LEDS.setPixelColor(i, LEDS.Color(30,0,0));
    LEDS.show();
  }
}

void loop() {
  int bytes = SerialUSB.available();
  if (!bytes) {
    return;
  }

  parseBytes(bytes);
}

void parseBytes(int numBytes) {
  uint8_t red = 0;
  uint8_t grn = 0;
  uint8_t blu = 0;
  while (numBytes--) {
    byte val = SerialUSB.read();
    if (val == 0xFF) {
      IDX = 0;
      pos = 0;
      LEDS.show();
    }
    else {
      switch(pos++) {
        case 0:
        red = val;
        break;
        case 1:
        grn = val;
        break;
        case 2:
        blu = val;
        pos = 0;
        LEDS.setPixelColor(IDX++, LEDS.Color(red,grn,blu));
        break;
      }
    }
  }
}

