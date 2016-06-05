#include <WS2812.h>
#include <DigiCDC.h>

static const int LED_COUNT = 30;
static const int LED_PIN = 1;
static int IDX = 0;
static int pos = 0;

WS2812 LEDS(LED_COUNT);
cRGB value;

void setup() {
  SerialUSB.begin();
  LEDS.setOutput(LED_PIN);

  // set all to very light white
  value.b = 0; value.g = 20; value.r = 0;
  for (int i = 0; i < LED_COUNT; i++) {
    LEDS.set_crgb_at(i, value);
    LEDS.sync();
  }
  value.b = 20; value.g = 0; value.r = 0;
  LEDS.set_crgb_at(IDX, value);
}

void loop() {
  int bytes = SerialUSB.available();
  if (!bytes) {
    return;
  }

  parseBytes(bytes);
}

void parseBytes(int numBytes) {
  while (numBytes--) {
    byte val = SerialUSB.read();
    if (val == 0xFF) {
      IDX = 0;
      pos = 0;
      LEDS.sync();
    }
    else {
      switch(pos++) {
        case 0:
        value.r = val;
        break;
        case 1:
        value.g = val;
        break;
        case 2:
        value.b = val;
        pos = 0;
        LEDS.set_crgb_at(IDX++, value);
        break;
      }
    }
  }
}

