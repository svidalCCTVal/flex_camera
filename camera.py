# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:46:16 2023

@author: CCTVAL
"""

import cv2 as cv 
from sys import exit


cap = cv.VideoCapture('/dev/video0')

if not cap.isOpened():
  print("Cannot open camera")
  exit()
  
while True:
  # Capture frame-by-frame
  ret, frame = cap.read()
  if not ret:
    continue
  h,w,_ = frame.shape
  h2,w2 = (int)(h/2),(int)(w/2)+55
  cuty,cutx = 112,112
  ymin,ymax,xmin,xmax = h2-cuty,h2+cuty,w2-cutx,w2+cutx
  img = frame[ymin:ymax, xmin:xmax ,:].copy()
  img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  
  cv.rectangle(frame, pt1=(xmin,ymin), pt2=(xmax,ymax), color=(255,0,0), thickness=10)
  resized = cv.resize(frame.copy(), (800,600))
  del frame
  cv.imshow("color",resized)
  tecla = cv.waitKey(1)
  if tecla == ord('q'):
    break

cap.release()
cv.destroyAllWindows()
