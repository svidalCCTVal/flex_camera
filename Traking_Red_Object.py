# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:11:38 2024

Se intenterá experimentar con modelos de treshgold adaptativo y con videos que no tengan buena visión en general a ver qué ocurre.
En este método la idea es tener un circulo que esté pintado o pegado a la madera a deformar. 

Estado: Probando y jugando con treshold adapativo

@author: SVL
"""

import cv2
import numpy as np
# import time
# import pandas as pd

# GLOBAL VARIABLES 
LENGTH_PX = 1280 
WIDTH_PX = 720 

# Cambiar nombres a estas variables
redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([8, 255, 255], np.uint8)

redBajo2=np.array([175, 100, 20], np.uint8)
redAlto2=np.array([179, 255, 255], np.uint8)

# STYLE VARIABLES
font = cv2.FONT_HERSHEY_COMPLEX

# Abrir video
capture = cv2.VideoCapture('../Registros_FlexCam/25_03_2024/DSC_0102.MOV')

if not capture.isOpened():
  print("Cannot open camera")
  exit()
  
while (capture.isOpened()):
    # Capture frame-by-frame
    val_returned, frame = capture.read()
    if val_returned==True:
        frame = cv2.resize(frame,(LENGTH_PX,WIDTH_PX))
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        frame_umbral = cv2.threshold(frame_gray,35,255,cv2.THRESH_BINARY)[1] 

        maskRed1 = cv2.inRange(frame_hsv, redBajo1, redAlto1)
        maskRed2 = cv2.inRange(frame_hsv, redBajo2, redAlto2)
        #maskRed = cv2.add(maskRed1, maskRed2)
        maskRedvis = cv2.bitwise_and(frame, frame, mask= maskRed1)  
        
        cv2.imshow("Video B&N",maskRedvis)
        cv2.imshow("Video Original", frame)
        
        tecla = cv2.waitKey(1)
        if tecla == ord('q'):
            break
    else: break

capture.release()
cv2.destroyAllWindows()