Yet Another Ambient Lighting
============================

About
-----
Probably the cheapest ambient lighting your monitor can get.

Requirements
------------
- WS2812b LED strip
- Digistump
- python2
- python2-pyserial
- python2-pyqt5 [optional]

Setup
-----
1. Install your WS2812b LED strip with Digistump as a controller.
  - Position LED strip to start from **bottom left** corner of your screen.
2. Modify `LEDS_ARRAY` variable in `main.py` file.
  - 'L' is LED
  - '.' is nothing  
  `LEDS_ARRAY` **must represent positioning of your LEDs behind the monitor if you want to use this program as Ambilight replacement.** Otherwise you can write only L's for LEDs, ex. `LLLLL` for 5 LEDs.
3. Find name of your display.
  - on linux use command `xrandr | grep " connected" | awk '{print $1}'` to find connected displays, ex. `DP1-1`
4. Modify `SCREEN` variable in `main.py` to previously found name of screen. _This is not needed if you are not using Ambilight function_
5. Copy `50-ambilight.rules` to `/etc/udev/rules.d/` or change `DEVICE` variable in `main.py` to serial port on which program will communicate with Digistump
6. Connect Digistump, wait couple of seconds, and run `main.py`

Callibration
------------
Use variables `MIN_RGB` and `MAX_RGB` in `main.py` to set minimum and maximum values for each color.

Usage
-----
Run: `python2 main.py COMMAND` where `COMMAND` is one of the following:
```
off                                    - disable all LEDs
color/colour/rgb [red] [green] [blue]  - set color
white [brightness]                     - light all leds with white color
led POS [red] [green] [blue]           - light one led at POSition
avg/mean                               - screen average color
edge/movie                             - screen edge color (ambilight)
fade                                   - smoothly fade between colors
rainbow/spectrum [circular/hasselhoff] - show rainbow
kit/knight/hasselhoff                  - K.I.T. from 'Knight Rider'
countdown SECONDS [red] [green] [blue] - fancy countdown
```
Values written in UPPERCASE are required. Values in brackets are optional.

Other
-----
Package `python2-pyqt5` is needed to quickly grab screenshots.  
Code was tested on linux with KDE5 and may not work on other platforms.  
Max frame rate is around 25-30fps due to the limitations of the DigistumpCDC library. However, it is enough.
