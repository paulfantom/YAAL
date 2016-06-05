import math

def HSItoRGB(H=0,S=0.5,I=0.5):
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

if __name__ == '__main__':
  import sys
  print(HSItoRGB(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3])))
