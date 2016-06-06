Digistump Ambilight
===================

Requirements:
-------------
- Arduino IDE
- Digistump Board package (https://github.com/digistump/DigistumpArduino)

Installation:
-------------
1. On linux copy "49-micronucleus.rules" to /etc/udev/rules.d/. On other platforms check https://digistump.com/wiki/digispark/tutorials/connecting
2. Replace original DigiCDC.cpp file with included modified version
3. In Arduino IDE choose "Digispark (Default - 16.5 MHz)" as a platform board
    Tools -> Board -> Digispark (Default - 16.5 MHz)
4. Upload software (remember to connect board AFTER clicking "Upload")
