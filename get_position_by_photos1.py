#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:25:53 2023

@author: cctval
"""

import cv2
import numpy as np
# Cargar imágenes
imagen_inicial = cv2.imread('posinit.jpg')
imagen_final = cv2.imread('posfin.jpg')

#ancho_nuevo = 800
#alto_nuevo = int(imagen_inicial[0]*(ancho_nuevo/imagen_inicial.shape[1]))

#imagen_inicial_redim = cv2.resize(imagen_inicial, (1280, 720))
#imagen_final_redim = cv2.resize(imagen_final, (1280, 720))

# Convertir a escala de grises
#gris_inicial = cv2.cvtColor(imagen_inicial_redim, cv2.COLOR_BGR2GRAY)
#gris_final = cv2.cvtColor(imagen_final_redim, cv2.COLOR_BGR2GRAY)

gris_inicial = cv2.cvtColor(imagen_inicial, cv2.COLOR_BGR2GRAY)
gris_final = cv2.cvtColor(imagen_final, cv2.COLOR_BGR2GRAY)


# Aplicar umbral para resaltar la marca
_, umbral_inicial = cv2.threshold(gris_inicial, 250, 255, cv2.THRESH_BINARY_INV)
_, umbral_final = cv2.threshold(gris_final, 250, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos
contornos_inicial, _ = cv2.findContours(umbral_inicial, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornos_final, _ = cv2.findContours(umbral_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar contornos (opcional, solo para visualización)
cv2.drawContours(imagen_inicial, contornos_inicial, -1, (0, 255, 0), 2)
cv2.drawContours(imagen_final, contornos_final, -1, (0, 255, 0), 2)

# Calcular centroides de los contornos
centroide_inicial = np.mean(contornos_inicial[0], axis=0)[0]
centroide_final = np.mean(contornos_final[0], axis=0)[0]

# Calcular deformación
deformacion_x = centroide_final[0] - centroide_inicial[0]
deformacion_y = centroide_final[1] - centroide_inicial[1]

print(f"Deformación en el eje X: {deformacion_x}")
print(f"Deformación en el eje Y: {deformacion_y}")

# Mostrar imágenes (opcional)
cv2.imshow('Imagen Inicial', imagen_inicial)
cv2.imshow('Imagen Final', imagen_final)
cv2.waitKey(0)
cv2.destroyAllWindows()


# %% Prueba 2
    
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('posinit.jpg', cv.IMREAD_GRAYSCALE)
# Initiate ORB detector
orb = cv.ORB_create()
# find the keypoints with ORB
kp = orb.detect(img,None)
# compute the descriptors with ORB
kp, des = orb.compute(img, kp)
# draw only keypoints location,not size and orientation
img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
plt.imshow(img2), plt.show()







