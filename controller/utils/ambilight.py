#!/usr/bin/env python2
import os
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

  def __init__(self,leds_array=[1],port='/dev/ambilight',minRGB=(0,0,0),maxRGB=(254,254,254)): 
    self.setMinMax(minRGB,maxRGB)
    self.__parseLedsArray(leds_array)
    for i in range(60):
      try:
        #self.serial = AmbilightSerial(leds=self.leds, port=port, write_timeout=1)
        self.serial = AmbilightSerial(leds=self.leds, port=port)
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

  def __normalize(self,rgb):
    return tuple([int( rgb[i]*self.thMult[i][0] + self.thMult[i][1] ) for i in range(3)])

  def setMinMax(self,minRGB=(0,0,0),maxRGB=(254,254,254)):
    self.thMult = [ ((maxRGB[i]-minRGB[i])/255.0, minRGB[i]) for i in range(3) ]

  def allColor(self,rgb,normalized=False):
    if normalized:
      rgb = self.__normalize(rgb)
    write = self.serial.write
    for i in range(self.leds):
      write(rgb)
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
    try:
      while True:
        self.one_by_one(color)
        self.one_by_one(color,False,self.leds-1)
    except KeyboardInterrupt:
      print("Exiting...")

  def countdown(self,seconds,color):
    steps = self.leds // 2
    interval = seconds / steps
    pos = 0
    try:
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
    except KeyboardInterrupt:
      print("Exiting...")

  def sun(self, hue=30, rise_time=30):
    hue = 30
    max_luminosity = 0.55

    steps = rise_time / 0.1
    step = max_luminosity / steps
    luminosity = 0
    while luminosity < max_luminosity:
      t1 = time.time()
      luminosity += step
      c = HSItoRGB(hue, 1, luminosity)
      self.allColor(c, True)
      time.sleep(0.1 - (time.time() - t1))

  def rainbow(self):
    H = 0
    self.serial.sync()
    for led in range(self.leds):
      c = HSItoRGB(H,1,0.5)
      self.serial.write(c)
      H += 360 // self.leds
    self.serial.sync()
  
  def move_rainbow(self,circular=False):
    arr = []
    H = 0 
    for led in range(self.leds):
      arr.append(HSItoRGB(H,1,0.5))
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
        self.allColor(self.__normalize(c))
  
  def edgeScreen(self,screen_name,app,fps=60):
    if NO_QT:
      print("Cannot find PyQT5. Exiting...")
      sys.exit(1)
   
    #get proc file
    if app is not None:
      try:
        from subprocess import check_output
        pid = int(check_output(["pidof","-s",app]))
        proc_file = '/proc/' + str(pid)
      except:
        proc_file = None
    else:
      proc_file = None
    interval = 1/float(fps)
#    scr = Screen(screen_name,grid)
    scr = Screen(screen_name,self.ledMatrix,self.ledArray,self.ledOffset)
    self.serial.sync()
    while True:
      tstart = time.time()
      scr.grab()
      arr = scr.compute()
      for rgb in arr:
        self.serial.write(self.__normalize(rgb))
      self.serial.sync()
      if proc_file is not None:
        if not os.path.exists(proc_file):
          break
      tend = time.time()
      wait = interval - (tend - tstart)
      if wait > 0:
        time.sleep(wait)



