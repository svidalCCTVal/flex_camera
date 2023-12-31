# -*- coding: utf-8 -*-
"""
- COMPRESION CAM -

Código realizado para medir la variación del tamaño de madera expuesta a presión sobre esta causando una compresión del material.
El código basa su funcionamiento en base a la detección del objeto oscuro con mayor área y verificar la variación de la arista inicial. 

Estado: Validado con video real grabado en laboratorio DIM. Sincronización del final del video logrado en base a movimiento contrario a compresión sostenido. 
Pendientes: 
    - Lograr sincronización del inicio del video.

Input: 
    - pixel_mm_ratio: Valor obtenido del codigo "calibration_measurement.py"
    - max_pixel_change: Cantidad de pixeles sostenidos en aumento para considerar que la posición de la madera cambió en posición. En caso de que se haga un ensayo
    rápido podría considerarse hacer este valor más pequeño, para obtener mayor precisión.
    - max_conteo_disminucion: Cantidad de pixeles sostenidos en contra de la compresión para detectar fin del experimento. En caso de que sea muy rápido el
    decrecimiento podría hacerse este número menor. 
    
Output: 
    - nombre_archivo_excel: Columna de variacion de pixeles con su conversión a milímetros se exporta en formato '.xlsx' en la carpeta del código.    
    
Created on Mon Dec  4 14:16:47 2023
@author: CCTVal - SVL
"""

import cv2
import time
import numpy as np
from sys import exit
import pandas as pd

font = cv2.FONT_HERSHEY_COMPLEX

second_init = time.time()

first_frame = True
pixel_mm_ratio = 0.08460236886632826
y_initial = 0
x_initial = 0
max_pixel_change = 35
pixel_change_count_up = 0
pixel_change_count_down = 0 
pixel_deformation = 0
pixel_deformation_list = []
conteo_disminucion = 0
max_conteo_disminucion = 10

# Abrir video
cap = cv2.VideoCapture('../Videos_Flexion_Cam/Ensayo_Compresion_1.MOV')

if not cap.isOpened():
  print("Cannot open camera")
  exit() 

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret==True:
        
        # Re dimenzionar imagenes a tamaño 1280 o el que se requiera
        imagen_inicial = cv2.resize(frame, (1280, 720))
        
        # Aplicar filtro gaussiano para difuminar bordes
        #imagen_inicial_blured = cv2.medianBlur(imagen_inicial, 5)
        imagen_inicial_blured = imagen_inicial

        # Convertir a escala de grises
        gris_inicial = cv2.cvtColor(imagen_inicial_blured, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral para posteriormente detectar contornos con facilidad
        umbral_inicial = cv2.threshold(gris_inicial, 130, 255, cv2.THRESH_BINARY_INV)[1]
        
        # Encontrar contornos de imagen
        contornos_inicial, _ = cv2.findContours(umbral_inicial, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Seleccionar contorno que abarca mayor área en cada frame
        max_area_contour_inicial = max(contornos_inicial, key=cv2.contourArea)
        
        # Obtener los vertices donde están las esquinas del contorno. Variar parámetro de escalamiento en caso de querer distintas respuestas.
        approx_inicial = cv2.approxPolyDP(max_area_contour_inicial, 0.009 * cv2.arcLength(max_area_contour_inicial, True), True)
        
        cv2.drawContours(imagen_inicial, [approx_inicial], -1, (0, 0, 255), 2)
        
        # Hay que obtener el valor X de la coordenada con Y más alto, para poner el dibujo la imagen
        x_array_inicial =  approx_inicial[:, :, 0].ravel()
        y_array_inicial = approx_inicial[:, :, 1].ravel()
        
        ###  SE OBTIENE POSICIÓN DE (X,Y) PARA GUARDAR ESTADO INICIAL  
        x_ordenado_inicial = np.sort(x_array_inicial)[::-1] 
        y_ordenado_inicial = np.sort(y_array_inicial)[::-1]

        # Tomar los valores de y de las esquinas superiores del rectangulo detectado - Estos valores nos sirven para todos los frames
        y_o1 = y_ordenado_inicial[3]
        y_o2 = y_ordenado_inicial[2]
        
        y_mean_actual = round((y_o1+y_o2)/2) 
        
        if first_frame:
            y_mean = round((y_o1+y_o2)/2)
            y_initial = y_mean
            first_frame = False
        else:
            if y_mean_actual < y_mean :
                conteo_disminucion += 1
            else: 
                conteo_disminucion=0
            
            if conteo_disminucion >= max_conteo_disminucion:
                print("¡Disminución rápida detectada! Deteniendo la lectura del video luego de ",max_conteo_disminucion,"frames.")
                break

            if y_mean_actual>y_mean:
                pixel_change_count_up += 1 
            else: 
                pixel_change_count_up = 0
                
            if pixel_change_count_up >= max_pixel_change:
                pixel_change_count_up=0
                y_mean = round((y_o1+y_o2)/2)
                
            pixel_deformation = y_mean - y_initial
            
        pixel_deformation_list.append(pixel_deformation*pixel_mm_ratio)
        print("y_mean:", y_mean, "pixel_deformation:",pixel_deformation,"(y_o1+y_o2)/2:",y_mean_actual)
        cv2.imshow("Video", imagen_inicial)
        
        tecla = cv2.waitKey(1)
        if tecla == ord('q'):
                break
    
    else: break

second_end = time.time()

cap.release()
cv2.destroyAllWindows()

while_duration = second_end-second_init

print("while_duration:", while_duration)
print('Deformación Final=', pixel_deformation*pixel_mm_ratio)

#Exportar deformaciones a excel
data = {'Columna': pixel_deformation_list}
df = pd.DataFrame(data)

# Exportar a un archivo Excel
nombre_archivo_excel = 'Compresion.xlsx'
df.to_excel(nombre_archivo_excel, index=False)








#%% RUTINA POR DOS FOTOS

"""
Código de prueba en base a fotos para probar detección y algoritmo de compresion.

"""

import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX

#Relación pixel-milimetro
relacion_pixel_mm = 0.1736111111111111

# Cargar imágenes
imagen_inicial = cv2.imread('Imagenes_Traccion/madera_inicial.JPG')
imagen_final = cv2.imread('Imagenes_Traccion/madera_final.jpg')

# Re dimenzionar imagenes a tamaño 1280 o el que se requiera
imagen_inicial = cv2.resize(imagen_inicial, (1280, 720))
imagen_final = cv2.resize(imagen_final, (1280, 720))

# Aplicar filtro gaussiano para difuminar bordes
imagen_inicial_blured = cv2.medianBlur(imagen_inicial, 9)
imagen_final_blured = cv2.medianBlur(imagen_final, 9)

# Convertir a escala de grises
gris_inicial = cv2.cvtColor(imagen_inicial_blured, cv2.COLOR_BGR2GRAY)
gris_final = cv2.cvtColor(imagen_final_blured, cv2.COLOR_BGR2GRAY)

# Aplicar umbral para posteriormente detectar contornos con facilidad
umbral_inicial = cv2.threshold(gris_inicial, 150, 255, cv2.THRESH_BINARY_INV)[1]
umbral_final = cv2.threshold(gris_final, 150, 255, cv2.THRESH_BINARY_INV)[1]

# Encontrar contornos de imagen inicial y final
contornos_inicial, _ = cv2.findContours(umbral_inicial, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornos_final, _ = cv2.findContours(umbral_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Seleccionar contorno que abarca mayor área en cada imagen 
max_area_contour_inicial = max(contornos_inicial, key=cv2.contourArea)
max_area_contour_final = max(contornos_final, key=cv2.contourArea)

# -
# - 
# - Adaptación de 1 cliclo For de esta página: 
# - https://www.geeksforgeeks.org/find-co-ordinates-of-contours-using-opencv-python/
# -
# -

# Obtener los vertices donde están las esquinas del contorno. Variar parámetro de escalamiento en caso de querer distintas respuestas.
approx_inicial = cv2.approxPolyDP(max_area_contour_inicial, 0.011 * cv2.arcLength(max_area_contour_inicial, True), True)
approx_final = cv2.approxPolyDP(max_area_contour_final, 0.011 * cv2.arcLength(max_area_contour_final, True), True)

# Hay que obtener el valor X de la coordenada con Y más alto, para poner el dibujo la imagen
x_array_inicial =  approx_inicial[:, :, 0].ravel() 
x_array_final = approx_final[:, :, 0].ravel() 

y_array_inicial = approx_inicial[:, :, 1].ravel()
y_array_final = approx_final[:, :, 1].ravel()

print("x_array_inicial:", x_array_inicial)
print("y_array_inicial:", y_array_inicial)
print("x_array_final:", x_array_final)
print("y_array_final:", y_array_final)

x_ordenado_inicial = np.sort(x_array_inicial)[::-1]
y_ordenado_inicial = np.sort(y_array_inicial)[::-1]

y_o1 = y_ordenado_inicial[3]
y_o2 = y_ordenado_inicial[2]

# y inicial media
y_o = round((y_o1+y_o2)/2)

# x inicial 1
x_o1=x_array_inicial[np.where(y_array_inicial==y_o1)][0]

# x inicial 2 
x_o2=x_array_inicial[np.where(y_array_inicial==y_o2)][0]

x_o=round((x_o1+x_o2)/2)

x_ordenado_final = np.sort(x_array_final)[::-1]
y_ordenado_final = np.sort(y_array_final)[::-1]

print("[INICIAL] Coordenadas de Y ordenadas ",y_ordenado_inicial)
print("[FINAL] Coordenadas de Y ordenadas ",y_ordenado_final)

y_f1 = y_ordenado_final[3]
y_f2 = y_ordenado_final[2]

# y final media
y_f = round((y_f1+y_f2)/2)

print("x_o1, y_o1:", x_o1, y_o1)
print("x_o2, y_o2:", x_o2, y_o2)
print("y_f1:", y_f1)
print("y_f2:", y_f2)

deformacion_final = abs(y_f - y_o)*0.1736111111111111


pos_inicial_y = y_ordenado_inicial[0]
pos_final_y = y_ordenado_final[0] # corresponde al max value de las posiciones Y

print(" \n \n DEFORMACIÓN FINAL:   ", deformacion_final, "[mm]")

# ACÁ EN ADELANTE SON CONFIGURACIONES DE VISUALIZACIÓN


# A CONTINUACIÓN SE USA SOLO PARA PONER TEXTOS EN LAS ESQUINAS DETECTADAS

# Transformar la matrix anterior a vector de una dimensión
approx_matrix_final_flat = approx_final.ravel()
approx_matrix_inicial_flat = approx_inicial.ravel()

# Contador de elementos en arreglo approx_matrix_flat
i=0

for j in approx_matrix_final_flat : 
        if(i % 2 == 0): 
            x = approx_matrix_final_flat[i] 
            y = approx_matrix_final_flat[i + 1] 
  
            # String containing the co-ordinates. 
            string = str(x) + " " + str(y)  
  
            if(i == 0): 
                # text on topmost co-ordinate. 
                #cv2.putText(imagen_inicial, string, (x, y), font, 0.5, (0, 255, 0))  
                cv2.putText(imagen_final, string, (x, y), font, 0.5, (0, 255, 0))
                
            else: 
                # text on remaining co-ordinates. 
                #cv2.putText(imagen_inicial, string, (x, y), font, 0.5, (0, 255, 0))
                cv2.putText(imagen_final, string, (x, y), font, 0.5, (0, 255, 0))  
        i = i + 1

i=0
for j in approx_matrix_inicial_flat : 
        if(i % 2 == 0): 
            x = approx_matrix_inicial_flat[i] 
            y = approx_matrix_inicial_flat[i + 1] 
  
            # String containing the co-ordinates. 
            string = str(x) + " " + str(y)  
  
            if(i == 0): 
                # text on topmost co-ordinate. 
                cv2.putText(imagen_inicial, string, (x, y), font, 0.5, (0, 255, 0))                  
            else: 
                # text on remaining co-ordinates. 
                cv2.putText(imagen_inicial, string, (x, y), font, 0.5, (0, 255, 0))
        i = i + 1

# Dibujar contornos (opcional, solo para visualización)
#cv2.drawContours(imagen_inicial, contornos_inicial, -1, (0, 255, 0), 2)
cv2.drawContours(imagen_inicial, [approx_inicial], -1, (0, 255, 0), 2)
cv2.drawContours(imagen_final, [approx_final], -1, (0, 255, 0), 2)

# Dibujar lina de y minimos
#cv2.line(imagen_inicial,(0,y_ordenado_inicial[0]),(1280,y_ordenado_inicial[1]),(255,0,0),4)
cv2.line(imagen_final,(x_o,y_o),(x_o,y_f),(255,0,0),4)

# Mostrar imágenes (opcional)
cv2.imshow('Imagen Inicial', imagen_inicial)
#cv2.imshow('Escala de grises Final', umbral_final)
cv2.imshow('Imagen Final', imagen_final)
cv2.waitKey(0)
cv2.destroyAllWindows()

