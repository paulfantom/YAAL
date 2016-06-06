#!/usr/bin/env python2
import sys
from utils.ambilight import Ambilight
from utils.colors import HSItoRGB

LED_ARRAY=[
  ".LLLLLLLLLLLLLLLL.",
  "L................L",
  "L................L",
  "L................L",
  "L................L",
  "L................L",
  "L................L",
  "L................L"
]
SCREEN='DP1-1'
DEVICE="/dev/ambilight"

MIN_RGB=(4,4,4)
##MAX_RGB=(254,254,140)  #Belinea "<F11>low blue light -60%"
MAX_RGB=(254,254,254)

def input3(d1=0,d2=0,d3=0,start=2,normalize=int):
  ret = [d1,d2,d3]
  for i in range(3):
    try:
      ret[i] = normalize(sys.argv[start+i])
    except IndexError:
      pass
  return ret

if __name__ == '__main__':
  ambilight = Ambilight(LED_ARRAY,DEVICE)
  try:
    sel = sys.argv[1].lower()
  except IndexError:
    sel = 'white'
  if sel == 'off':
    ambilight.off()
  elif sel == 'color' or sel == 'colour' or sel == 'rgb':
    rgb = input3()
    rgb = ( int(rgb[0]), int(rgb[1]), int(rgb[2]) )
    ambilight.allColor(rgb)
  elif sel == 'white' or sel == 'full':
    try:
      brightness = int(sys.argv[2])
    except IndexError:
      brightness = 254
    ambilight.allColor((brightness,brightness,brightness))
  elif sel == 'hsi' or sel == 'hsv' or sel == 'hsl':
    ambilight.allColor(HSItoRGB(*(input3(300,1,1,normalize=float))))
  elif sel == 'fade':
    while True:
      for H in range(360):
        ambilight.allColor(HSItoRGB(H,1,1))
  elif sel == 'led':
    ambilight.oneLED(int(sys.argv[2]),input3(254,0,0,start=3))
  elif sel == 'kit' or sel == 'knight' or sel == 'hasselhoff':
    ambilight.kit(input3(254))
  elif sel == 'countdown':
    try:
      sec = float(sys.argv[2])
    except IndexError:
      print("Seconds not spocified")
      sys.exit(1)
    ambilight.countdown(sec,input3(255,0,0,start=3))
  elif sel == 'rainbow' or sel == 'spectrum':
    try:
      if sys.argv[2].lower() == 'circular':
        ambilight.move_rainbow(True)
      elif sys.argv[2].lower() == 'hasselhoff':
        ambilight.move_rainbow(False)
      else:
        ambilight.rainbow()
    except IndexError:
      ambilight.rainbow()
  elif sel == 'avg' or sel == 'mean':
    ambilight.setMinMax(MIN_RGB,MAX_RGB)
    ambilight.screenSmoothFlow(SCREEN)
  elif sel == 'edge' or sel == 'movie':
    ambilight.setMinMax(MIN_RGB,MAX_RGB)
    ambilight.edgeScreen(SCREEN)
  elif sel == 'speedtest':
    import time
    i = 0
    t1 = time.time()
    t2 = time.time()
    while (t2 - t1) < 60:
      ambilight.allColor((((20*i)%254),0,0))
      i += 1
      t2 = time.time()
    print("FPS: "+str(round(i/60.0,2)))
  else:
    print("Following options are available:")
    print("  off                                    - disable all LEDs")
    print("  color/colour/rgb [red] [green [blue]   - set color")
    print("  white [brightness]                     - light all leds with white color")
    print("  led POS [red] [green] [blue]           - light one led at POSition")
    print("  avg/mean                               - screen average color")
    print("  edge/movie                             - screen edge color (ambilight)")
    print("  fade                                   - smoothly fade between colors")
    print("  rainbow/spectrum [circular/hasselhoff] - show rainbow")
    print("  kit/knight/hasselhoff                  - K.I.T. from 'Knight Rider'")
    print("  countdown SECONDS [red] [green] [blue] - fancy countdown")
#    print("  speedtest                              - test connection speed")

