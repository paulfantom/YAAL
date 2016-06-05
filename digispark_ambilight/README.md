Digistump Ambilight
===================

Requirements:
-------------
- Arduino IDE
- Digistump Board package (https://github.com/digistump/DigistumpArduino)

Installation:
-------------
1a. Linux:
    Copy "49-micronucleus.rules" to /etc/udev/rules.d/
1b. Other platforms
    https://digistump.com/wiki/digispark/tutorials/connecting

2. Replace original DigisparkCDC library with my modified version DigisparkCDCFast
3. In Arduino IDE choose "Digispark (Default - 16.5 MHz)" as a platform board
    Tools -> Board -> Digispark (Default - 16.5 MHz)
4. Upload software (remember to connect board AFTER clicking "Upload")
