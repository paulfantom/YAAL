#!/usr/bin/env python2
import sys
import time
from utils.colors import HSItoRGB
from utils.ambilightserial import AmbilightSerial
try:
  from utils.screen import Screen
  NO_QT=False
except ImportError:
  NO_QT=True

class Ambilight(object):
  serial = None
  leds = 1
  ledMatrix = (1,1)
  ledArray  = (1,1,1,1)
  ledOffset = (0,0,0,0)

  def __init__(self,leds_array=[1],port='/dev/ambilight'):
    self.__parseLedsArray(leds_array)
    for i in range(60):
      try:
        #self.serial = AmbilightSerial(leds=self.leds, port=port, baudrate=115200, write_timeout=1)
        self.serial = AmbilightSerial(leds=self.leds, port=port, baudrate=115200)
        break
      except OSError:
        if i == 0:
          print("Waiting for "+port+" to become available.")
        time.sleep(1)
    if self.serial == None:
      print("Couldn't access "+port)
      sys.exit(1)
    self.serial.sync()
#    self.off()

  def __parseLedsArray(self,leds_array):
    count = 0
    for row in leds_array:
      for i in row:
        if i == 'L': count+=1
    self.leds =  count
    self.ledMatrix = (len(leds_array[0]),len(leds_array))
    array  = [0,0,0,0]
    offset = [0,0,0,0]

    # top & bottom
    for i in range(4):
      led = 0
      if i < 2: side = 0
      else: side = -1
      
      if i == 1 or i == 3:
        # left & right
        while led < len(leds_array[0]):
          if leds_array[side][led] == '.': offset[i] += 1
          else: break
          led += 1
        while led < len(leds_array[0]):
          if leds_array[side][led] == 'L': array[i] += 1
          else: break
          led += 1
      else:
        # top & bottom
        while led < len(leds_array):
          if leds_array[led][side] == '.': offset[i] += 1
          else: break
          led += 1
        while led < len(leds_array):
          if leds_array[led][side] == 'L': array[i] += 1
          else: break 
          led += 1

    self.ledArray=tuple(array)
    self.ledOffset=tuple(offset)

  def allColor(self,rgb):
    for i in range(self.leds):
      self.serial.write(rgb)
    self.serial.sync()

  def off(self):
    self.allColor((0,0,0))

  def oneLED(self,pos,color):
    pos %= self.leds
    for i in range(self.leds):
      if pos == i:
        self.serial.write(color)
      else:
        self.serial.write((0,0,0))
    self.serial.sync()      
  
  def one_by_one(self,color,direction=True,start=0):
    pos = start
    for i in range(self.leds):
      self.oneLED(pos,color)
      if direction:
        pos+=1
      else:
        pos-=1
  
  def kit(self,color):
    while True:
      self.one_by_one(color)
      self.one_by_one(color,False,self.leds-1)

  def countdown(self,seconds,color):
    steps = self.leds // 2
    interval = seconds / steps
    pos = 0
    for step in range(steps):
      for i in range(self.leds):
        if pos == i or pos == self.leds-i-1:
          self.serial.write(color)
        else:
          self.serial.write((0,0,0))
      self.serial.sync()
      pos+=1
      time.sleep(interval)
    self.allColor(color)
  
  def rainbow(self):
    H = 0
    self.serial.sync()
    for led in range(self.leds):
      c = HSItoRGB(H,1,1)
      self.serial.write(c)
      H += 360 // self.leds
    self.serial.sync()
  
  def move_rainbow(self,circular=False):
    arr = []
    H = 0 
    for led in range(self.leds):
      arr.append(HSItoRGB(H,1,1))
      H += 360 // self.leds
  
    direction = True
    i = 0
    while True:
      for val in arr:
        self.serial.write(val)
      self.serial.sync()
      if direction:
        tmp = arr.pop(0)
        arr.append(tmp)
      else:
        tmp = [arr.pop()]
        tmp.extend(arr)
        arr = tmp
      if i > self.leds and not circular:
        direction = not direction
        i = 0
      i+=1
  
  def screenSmoothFlow(self,screen_name):
    if NO_QT:
      print("Cannot find PyQT5. Exiting...")
      sys.exit(1)
    scr = Screen(screen_name)
    count = 4
    nextC = None
    c = [0,0,0]
    steps = [0,0,0]
    while True:
      nextC = scr.compute()
      for i in range(3):
        steps[i] = (int(nextC[0][i]) - c[i]) // count
      
      for i in range(count):
        for j in range(3):
          c[j] += steps[j]
        self.allColor(c)
  
  def edgeScreen(self,screen_name,fps=60):
    if NO_QT:
      print("Cannot find PyQT5. Exiting...")
      sys.exit(1)
    interval = 1/float(fps)
#    scr = Screen(screen_name,grid)
    scr = Screen(screen_name,self.ledMatrix,self.ledArray,self.ledOffset)
    self.serial.sync()
    while True:
      tstart = time.time()
      scr.grab()
      arr = scr.compute()
      for rgb in arr:
        self.serial.write(rgb)
      self.serial.sync()
      tend = time.time()
      wait = interval - (tend - tstart)
      if wait > 0:
        time.sleep(wait)



