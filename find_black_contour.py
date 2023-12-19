# -*- coding: utf-8 -*-
"""
- FIND BLACK CONTOUR - 

Código de pruebas para identificar contornos de objetos obscuros. No se utiliza en los experimentos.

Created on Mon Nov 27 14:31:11 2023
@author: CCTVal - SVL
"""

import cv2 
import numpy as np 

## PARTE DE PROCESO DE IMAGENES

# Let's load a simple image with 3 black squares 
image = cv2.imread('madera_rota5.jpg') 
cv2.waitKey(0) 

image = cv2.resize(image, (1280, 720))

# Grayscale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

#gaussianBlur
#image_blured = cv2.GaussianBlur(gray,(5,5),0)

#medianBlur
image_blured = cv2.medianBlur(gray, 9)

# Find Canny edges 
edged = cv2.Canny(image_blured, 150, 255) 
cv2.waitKey(0) 


# Finding Contours 
# Use a copy of the image e.g. edged.copy() 
# since findContours alters the image 
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

cv2.imshow('Canny Edges After Contouring', edged) 
cv2.waitKey(0) 

print("Number of Contours found = " + str(len(contours))) 

# Find the contour with the largest area
max_area_contour = max(contours, key=cv2.contourArea)

# Draw the contour with the largest area in red
cv2.drawContours(image, [max_area_contour], 0, (0, 0, 255), 3)

# Draw all contours 
# -1 signifies drawing all contours 
#cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 

cv2.imshow('Contours', image) 
cv2.waitKey(0)
cv2.destroyAllWindows() 