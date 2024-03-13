# -*- coding: utf-8 -*-
"""
- FLEXION CAM 2 - 

La idea de este código es identificar un 'punto' negro en una madera y seguir su recorrido. Se piensa utilizar seguimiento en torno a su centro de masa.

Created on Tue Dec 19 09:58:06 2023
@author: CCTVal - SVL
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
capture = cv2.VideoCapture('../Registros_FlexCam/27_12_2023/DSC_0100.MOV') #poner nombre video

if not capture.isOpened():
  print("Cannot open camera")
  exit()
  
while (capture.isOpened()):
    # Capture frame-by-frame
    val_returned, frame = capture.read()
    if val_returned==True:
        resized_frame = cv2.resize(frame,(LENGTH_PX,WIDTH_PX))
        
        ventana_recortada = resized_frame[100:720, 200:1280] # estos valores de recorte son al ojo según el tipo de video, Hay que ver como establecer algo parametrizado completo
        
        frame_gray = cv2.cvtColor(ventana_recortada, cv2.COLOR_BGR2GRAY)
        
        frame_umbral = cv2.threshold(frame_gray, 100, 255, cv2.THRESH_BINARY_INV)[1]
        
        # Encontrar contornos 
        frame_contours, _ = cv2.findContours(frame_umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Seleccionar contorno que abarca mayor área en cada imagen 
        max_area_frame_contours = max(frame_contours, key=cv2.contourArea)
        
        # Crea imagen en blanco ára dibujar contorno
        imagen_contorno = np.zeros((620, 1080), dtype=np.uint8)
        
        # Dibujar contornos y lineas en frame actual 
        cv2.drawContours(imagen_contorno, frame_contours, -1, 255, thickness=cv2.FILLED)

        # Calcular los momentos de la imagen
        momentos = cv2.moments(imagen_contorno)
        
        # Calcular el centro de masa
        cx = int(momentos['m10'] / momentos['m00'])
        cy = int(momentos['m01'] / momentos['m00'])
        
        # Imprimir el centro de masa
        print(f"Centro de Masa: ({cx}, {cy})")
        
        # Dibujar el centro de masa en la imagen original
        imagen_original = cv2.imread('ruta_de_la_imagen.jpg')
        cv2.circle(ventana_recortada, (cx, cy), 5, (0, 255, 0), -1)  # Dibujar un círculo en el centro de masa
        
        text = f'Cy: {cy}'
        cv2.putText(ventana_recortada, text, (cx+10, cy-10), font, 0.5, (0,255,0), 1, cv2.LINE_AA)
        
        cv2.imshow("Video",ventana_recortada)
        tecla = cv2.waitKey(1)
        if tecla == ord('q'):
            break
    else: break

capture.release()
cv2.destroyAllWindows()

