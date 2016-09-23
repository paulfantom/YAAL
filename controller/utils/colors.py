import math

def HSLtoRGB(H=0,S=0.5,I=0.5):
  H = float(H)
  S = float(S)
  I = float(I) 
  H = math.fmod(H,360)
  H = 3.14159*H/float(180)
  if S > 1: S = 1
  elif S < 0: S = 0
  if I > 1: I = 1
  elif I < 0: I = 0
  if H < 2.09439:
    r = 255*I/3*(1+S*math.cos(H)/math.cos(1.047196667-H))
    g = 255*I/3*(1+S*(1-math.cos(H)/math.cos(1.047196667-H)))
    b = 255*I/3*(1-S)
  elif H < 4.188787:
    H = H - 2.09439
    g = 255*I/3*(1+S*math.cos(H)/math.cos(1.047196667-H))
    b = 255*I/3*(1+S*(1-math.cos(H)/math.cos(1.047196667-H)))
    r = 255*I/3*(1-S)
  else:
    H = H - 4.188787
    b = 255*I/3*(1+S*math.cos(H)/math.cos(1.047196667-H))
    r = 255*I/3*(1+S*(1-math.cos(H)/math.cos(1.047196667-H)))
    g = 255*I/3*(1-S)
  return (int(r),int(g),int(b))

def HSItoRGB(H=0,S=0.5,I=0.5):
  # normalize input
  H = float(H)
  S = float(S)
  I = float(I) 
  if S > 1: S = 1
  elif S < 0: S = 0
  if I > 1: I = 1
  elif I < 0: I = 0
  
  C = ( 1 - abs(2*I - 1)) * S
  h = H / 60
  X = C * ( 1 - abs(math.fmod(h,2) - 1))
  r = 0
  g = 0
  b = 0
 
  if h>=0 and h<1:
    r = C
    g = X
  elif h>=1 and h<2:
    r = X
    g = C
  elif h>=2 and h<3:
    g = C
    b = X
  elif h>=3 and h<4:
    g = X
    b = C
  elif h>=4 and h<5:
    r = X
    b = C
  else:
    r = C
    b = X
  m = I - C/2
  r += m
  g += m
  b += m

  r = int(r*255.0)
  g = int(g*255.0)
  b = int(b*255.0)

  return (r,g,b)

if __name__ == '__main__':
  import sys
  print(HSItoRGB(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])))
