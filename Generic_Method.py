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

# STYLE VARIABLES
font = cv2.FONT_HERSHEY_COMPLEX

# Abrir video
capture = cv2.VideoCapture('../Registros_FlexCam/27_12_2023/DSC_0094.MOV')

if not capture.isOpened():
  print("Cannot open camera")
  exit()
  
while (capture.isOpened()):
    # Capture frame-by-frame
    val_returned, frame = capture.read()
    if val_returned==True:
        frame = cv2.resize(frame,(LENGTH_PX,WIDTH_PX))
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame_umbral = cv2.adaptiveThreshold(frame_gray,150,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2) 
        
        
        cv2.imshow("Video",frame_umbral)
        
        tecla = cv2.waitKey(1)
        if tecla == ord('q'):
            break
    else: break

capture.release()
cv2.destroyAllWindows()