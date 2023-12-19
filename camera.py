# -*- coding: utf-8 -*-
"""
- CAMERA - 
Código para probar cámaras conectadas a PC, o reproducir video a partir de archivos.

Created on Fri Nov 24 10:46:16 2023
@author: CCTVal - SVL
"""

import cv2 as cv 
from sys import exit


#cap = cv.VideoCapture(1)
cap = cv.VideoCapture('Video_Flexion1.MOV')

if not cap.isOpened():
  print("Cannot open camera")
  exit()
  
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret==True:
        resized = frame.copy()
        del frame
        cv.imshow("color",resized)
        tecla = cv.waitKey(1)
        if tecla == ord('q'):
            break
    else: break


cap.release()
cv.destroyAllWindows()
