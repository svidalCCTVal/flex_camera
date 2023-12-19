# -*- coding: utf-8 -*-
"""
- CALIBRATION MEASUREMENT - 

Código para realizar calibración de la medición de pixeles en base a un cuadrado aruco de medidas conocidas. 

Input: 
    - imagen: Poner ruta de la foto de calibración.
    - tamano_objeto_mm: Medida del lado del cuadrado en milimetros

Output: 
    - relacion_pixel_mm: En consola se printea tamaño de 1 pixel en milímetros

Created on Wed Nov 29 16:40:41 2023
@author: CCTVAL
"""

import cv2
import numpy as np

# Abrir imagen del cuadrado aruco de calibración
imagen = cv2.imread('../Videos_Flexion_Cam/Calibracion_Ensayo_Compresion_1.JPG')

# Medida del lado del cuadrado aruco medida previamente, en milímetros
tamaño_objeto_mm = 50 

# Se desea escalar la foto tomada a un ancho de 1280 px
nuevo_ancho = 1280

# Calcular el factor de escala para mantener las proporciones
escala = nuevo_ancho / imagen.shape[1]
nuevo_alto = int(imagen.shape[0] * escala)

# Redimensionar la imagen
imagen_redimensionada = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen_redimensionada, cv2.COLOR_BGR2GRAY)

# Aplicar la binarización (umbralización) para obtener una imagen binaria
_, umbral = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos en la imagen binaria
contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Encontrar el contorno de área más grande más grande
contorno_mas_grande = max(contornos, key=cv2.contourArea)

# Calcular el rectángulo delimitador para el contorno más grande
x, y, ancho, alto = cv2.boundingRect(contorno_mas_grande)

print('x:', x)
print('y:', y)
print('ancho:', ancho)
print('alto:', alto)

# Calcular la relación de píxeles a milímetros que el ancho se mida bien 
relacion_pixel_mm = tamaño_objeto_mm / ancho  # ancho del objeto en píxeles

# Calcular el tamaño del objeto en milímetros
tamaño_objeto_real_mm = ancho * relacion_pixel_mm, alto * relacion_pixel_mm

# Dibujar el rectángulo delimitador en la imagen original
cv2.rectangle(imagen_redimensionada, (x, y), (x + ancho, y + alto), (0, 255, 0), 2)

print("Medidas calculadas con programa:", tamaño_objeto_mm)
print('Relacion pixel milimetro:', relacion_pixel_mm)

# Mostrar la imagen con el rectángulo delimitador
cv2.imshow('Objeto con rectángulo delimitador', imagen_redimensionada)
cv2.waitKey(0)
cv2.destroyAllWindows()





