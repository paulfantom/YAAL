import sys
from PyQt5.QtGui import QPixmap, QImage, QScreen, QColor
from PyQt5.QtWidgets import QApplication
from time import time

class Screen():
  __lastGrab = 0
  
  # name   - screen name ex. 'DP1-1'
  # matrix - how to cut screen ex. (2,2) cuts screen in 2x2 matrix
  # blocks - select which matrix blocks are interesting (left,up,right,down)
  # fps    - frames per second
  def __init__(self, name, matrix=(1,1), leds=(1,1,1,1), leds_offset=(0,0,0,0)):
    self.app = QApplication(sys.argv)
    self.screen = self.__findScreen(name)
    self.screenGeo = ( self.screen.availableGeometry().x(), self.screen.availableGeometry().y(), self.screen.availableGeometry().width(), self.screen.availableGeometry().height() )

    self.blockDim = ( self.screen.availableGeometry().width() // matrix[0], self.screen.availableGeometry().height() // matrix[1] )
    self.blocksGeo = self.__computeBlocksGeo(matrix,leds,leds_offset)
    self.scaleCount = self.__findScalerCount()
    #TODO check if all blocks are in matrix

  def __findScaler(self,curr,expected):
    eq = float(expected)/float(curr)
    scaler = 1
    while (0.5)**scaler > eq:
      scaler+=1
    return scaler
  
  def __findScalerCount(self):
    x = self.__findScaler(self.blockDim[0],1) - 1
    y = self.__findScaler(self.blockDim[1],1) - 1
    if x > y: return y
    else: return x
   
  def __findScreen(self,name):
  #  app = QApplication(sys.argv)
    if name == "all":
      print("Not implemented yet")
      sys.exit(1)
    screens = QApplication.screens()
    for scr in screens:
      if scr.name() == name:
        return scr

  def __computeBlocksGeo(self,matrix,blocks,offset):
    # check if all blocks are inside matrix
    for i in range(4):
      if matrix[i%2] < (blocks[(i+1)%4]+offset[(i+1)%4]):
        print("Matrix too small. Exiting...")
        sys.exit(1)
    
    # count
    coordinates = []
    for i in range(matrix[1]):
      for j in range(matrix[0]):
#        coordinates.append((x + self.blockDim[0] * j, y + self.blockDim[1] * i ))
        coordinates.append((self.blockDim[0] * j, self.blockDim[1] * i ))
    
    c = []
    for i in self.__chooseBlocks(matrix,blocks,offset):
      c.append(coordinates[i])
    return c

  def __chooseBlocks(self,matrix,blocks,offset):
    # create frame
    frame = []
    left =   [matrix[0]*(i+offset[0])             for i in range(blocks[0])]
    top =    [offset[1]+i                         for i in range(blocks[1])]
    right =  [matrix[0]-1+matrix[0]*(i+offset[2]) for i in range(blocks[2])]
    bottom = [offset[3]+matrix[0]*(matrix[1]-1)+i for i in range(blocks[3])]
    frame.extend(reversed(left))
    frame.extend(top)
    frame.extend(right)
    frame.extend(reversed(bottom))
    #remove duplicates and preserve order
    seen = set()
    seen_add = seen.add
    return [x for x in frame if not (x in seen or seen_add(x))]

  def grab(self):
    pix = self.screen.grabWindow(QApplication.desktop().winId(),*self.screenGeo)
    #pix.scaled(screen.availableGeometry().width() // 4,screen.availableGeometry().height() // 4)
    return pix.toImage()

  def pixelize(self,image):
    for i in range(self.scaleCount):
      image = image.scaled(image.width() // 2, image.height() // 2, transformMode=1) 
    return QColor(image.pixel(0,0)).getRgb()[:-1] 

  def compute(self):
    arr = []
    image = self.grab()
    for x,y in self.blocksGeo:
      img = image.copy(x,y,self.blockDim[0],self.blockDim[1])
      arr.append(self.pixelize(img))
    return arr
