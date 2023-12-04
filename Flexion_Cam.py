#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:25:53 2023

@author: cctval
"""

import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX

# ## APERTURA DE VIDEO
#cap = cv2.VideoCapture(1)
#
#if not cap.isOpened():
#  print("Cannot open camera")
#  exit()

#while True:
#  # Capture frame-by-frame
#  ret, frame = cap.read()
#  if not ret:
#    continue
#  resized = frame.copy()
#  del frame
#  
#  frame_to_show = cv2.medianBlur(resized, 9)
#  frame_to_show = cv2.cvtColor(frame_to_show, cv2.COLOR_BGR2GRAY)
#  umbral_frame = cv2.threshold(frame_to_show, 150, 255, cv2.THRESH_BINARY)[1]  
#  contornos_frame, _ = cv2.findContours(umbral_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#  
#  if  contornos_frame:
#      max_area_contour_frame = max(contornos_frame, key=cv2.contourArea)
#      approx = cv2.approxPolyDP(max_area_contour_frame, 0.005 * cv2.arcLength(max_area_contour_frame, True), True)
#      
#      n = approx.ravel()
#      i=0
#
#      for j in n : 
#              if(i % 2 == 0): 
#                  x = n[i] 
#                  y = n[i + 1] 
#        
#                  # String containing the co-ordinates. 
#                  string = str(x) + " " + str(y)  
#        
#                  if(i == 0): 
#                      # text on topmost co-ordinate. 
#                      cv2.putText(frame_to_show, "Arrow tip", (x, y), 
#                                      font, 0.5, (255, 0, 0))  
#                  else: 
#                      # text on remaining co-ordinates. 
#                      cv2.putText(frame_to_show, string, (x, y),  
#                                font, 0.5, (0, 255, 0))  
#              i = i + 1
#      
#      
#      
#      #cv2.drawContours(frame_to_show, [max_area_contour_frame], -1, (0, 255, 0), 2)
#      cv2.drawContours(frame_to_show, [approx], -1, (0, 255, 0), 2)
#  
#  cv2.imshow("MEDICION PIXELES",frame_to_show)
#  tecla = cv2.waitKey(1)
#    
#  if tecla == ord('q'):
#    break


#Relación pixel-milimetro
relacion_pixel_mm = 0.1736111111111111


# Cargar imágenes
imagen_inicial = cv2.imread('Imagenes/pintada_inicial.JPG')
imagen_final = cv2.imread('Imagenes/pintada_final.jpg')

# Re dimenzionar imagenes a tamaño 1280 o el que se requiera
imagen_inicial = cv2.resize(imagen_inicial, (1280, 720))
imagen_final = cv2.resize(imagen_final, (1280, 720))

# Aplicar filtro gaussiano para difuminar bordes
imagen_inicial_blured = cv2.medianBlur(imagen_inicial, 9)
imagen_final_blured = cv2.medianBlur(imagen_final, 9)

# Convertir a escala de grises
gris_inicial = cv2.cvtColor(imagen_inicial_blured, cv2.COLOR_BGR2GRAY)
gris_final = cv2.cvtColor(imagen_final_blured, cv2.COLOR_BGR2GRAY)


# Aplicar umbral para resaltar la marca
umbral_inicial = cv2.threshold(gris_inicial, 200, 255, cv2.THRESH_BINARY)[1]
umbral_final = cv2.threshold(gris_final, 180, 255, cv2.THRESH_BINARY)[1]

# Encontrar contornos
contornos_inicial, _ = cv2.findContours(umbral_inicial, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornos_final, _ = cv2.findContours(umbral_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Seleccionar contorno que abarca mayor área de imagen final
max_area_contour_inicial = max(contornos_inicial, key=cv2.contourArea)
max_area_contour_final = max(contornos_final, key=cv2.contourArea)


# LO QUE VIENE A CONTINUACIÓN ES UNA ADAPTACIÓN DE UN CICLO DE ESTA PÁGINA: https://www.geeksforgeeks.org/find-co-ordinates-of-contours-using-opencv-python/

# Obtener los vertices donde están las esquinas del contorno. Variar parámetro de escalamiento en caso de querer distintas respuestas.
approx_inicial = cv2.approxPolyDP(max_area_contour_inicial, 0.009 * cv2.arcLength(max_area_contour_inicial, True), True)
approx_final = cv2.approxPolyDP(max_area_contour_final, 0.009 * cv2.arcLength(max_area_contour_final, True), True)

# Hay que obtener el valor X de la coordenada con Y más alto, para poner el dibujo la imagen
x_array_final = approx_final[:, :, 0].ravel() #no está ordenado

print("Vertices de contorno: \n", approx_final)

y_array_inicial = approx_inicial[:, :, 1].ravel()
y_array_final = approx_final[:, :, 1].ravel()
print("y_array_final:", y_array_final)
print("x_array_final:", x_array_final)

max_y_index = np.argmax(y_array_final)
x_coordenate_y_max = x_array_final[max_y_index]

y_ordenado_inicial = np.sort(y_array_inicial)[::-1]
y_ordenado_final = np.sort(y_array_final)[::-1]

print("[INICIAL] Coordenadas de Y ordenadas ",y_ordenado_inicial)
print("[FINAL] Coordenadas de Y ordenadas ",y_ordenado_final)

pos_inicial_y = y_ordenado_inicial[0]
pos_final_y = y_ordenado_final[0] # corresponde al max value de las posiciones Y

deformacion_final = (pos_final_y - pos_inicial_y)*0.1736111111111111
print(" \n \n DEFORMACIÓN FINAL:   ", deformacion_final, "[mm]")

# ACÁ EN ADELANTE SON CONFIGURACIONES DE VISUALIZACIÓN


# A CONTINUACIÓN SE USA SOLO PARA PONER TEXTOS EN LAS ESQUINAS DETECTADAS
# Transformar la matrix anterior a vector de una dimensión
approx_matrix_flat = approx_final.ravel()

# Contador de elementos en arreglo approx_matrix_flat
i=0

for j in approx_matrix_flat : 
        if(i % 2 == 0): 
            x = approx_matrix_flat[i] 
            y = approx_matrix_flat[i + 1] 
  
            # String containing the co-ordinates. 
            string = str(x) + " " + str(y)  
  
            if(i == 0): 
                # text on topmost co-ordinate. 
                cv2.putText(imagen_final, "Arrow tip", (x, y), 
                                font, 0.5, (255, 0, 0))  
            else: 
                # text on remaining co-ordinates. 
                cv2.putText(imagen_final, string, (x, y),  
                          font, 0.5, (0, 255, 0))  
        i = i + 1

# Dibujar contornos (opcional, solo para visualización)
#cv2.drawContours(imagen_inicial, contornos_inicial, -1, (0, 255, 0), 2)
cv2.drawContours(imagen_inicial, [approx_inicial], -1, (0, 255, 0), 2)
cv2.drawContours(imagen_final, [approx_final], -1, (0, 255, 0), 2)

# Dibujar lina de y minimos
cv2.line(imagen_inicial,(0,y_ordenado_inicial[0]),(1280,y_ordenado_inicial[1]),(255,0,0),4)
cv2.line(imagen_final,(x_coordenate_y_max,pos_inicial_y),(x_coordenate_y_max,pos_final_y),(255,0,0),4)

# Mostrar imágenes (opcional)
cv2.imshow('Imagen Inicial', imagen_inicial)
#cv2.imshow('Escala de grises Final', umbral_final)
cv2.imshow('Imagen Final', imagen_final)
cv2.waitKey(0)
cv2.destroyAllWindows()


# %% Prueba 2
    
#import cv2 as cv
#from matplotlib import pyplot as plt
#
#img = cv.imread('posinit.jpg', cv.IMREAD_GRAYSCALE)
## Initiate ORB detector
#orb = cv.ORB_create()
## find the keypoints with ORB
#kp = orb.detect(img,None)
## compute the descriptors with ORB
#kp, des = orb.compute(img, kp)
## draw only keypoints location,not size and orientation
#img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
#plt.imshow(img2), plt.show()







