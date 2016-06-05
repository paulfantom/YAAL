Yet Another Ambient Lighting
============================

Requirements
------------
- python2
- python2-pyserial
- python2-pyqt5 [optional]

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
Values written in UPPERCASE are required.
Values written in [] brackets are optional

