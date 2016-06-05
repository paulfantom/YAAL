from serial import Serial

END_BYTE = b'\xFF'

class AmbilightSerial(Serial):
  def __init__(self, leds=1, *args, **kwargs):
    Serial.__init__(self, *args, **kwargs)

  def sync(self):
    Serial.write(self,END_BYTE)

  def write(self,data):
    if type(data[0]) is int:
      #return self.writeBytes(bytes(bytearray(data)))
      return self.writeBytes(bytearray(data))
    #elif type(data[0]) is str:
    #  print data
    else:
      for rgb in data:
        return self.write(rgb)

  def writeBytes(self,data):
    #for i in range(len(data)):
    #  if data[i] == ord(END_BYTE):
    #    print(data[i])
    #    data[i] = 254
    return Serial.write(self,data.replace(END_BYTE,'\xFE'))
    #return Serial.write(self,data)
