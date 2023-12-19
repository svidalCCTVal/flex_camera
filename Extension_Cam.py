# -*- coding: utf-8 -*-
"""
- EXTENSION CAM - 

Código para realizar medición de extensión de maderas. Este código es en experimentos donde se afirma una probeta de madera y se 'estira' hacia arriba. 
Para probar el código es necesario tener un video real de los experimentos, pero se deja avanzado el diagrama de código a continuación.

El código se basa en determinar la disminución de posición del pixel medio entre los vertices de la arista superior de la madera expuesta al experimento.  

Estado: Incompleto.
Pendientes: 
    - Grabar video de prueba real y echar a andar el código.  

Input: 
    - Video de experimento
    - Relación pixel mm ratio

Output: 
    - Archivo xlsx con deformación/estiramiento de la probeta de madera

Created on Tue Dec 19 09:58:20 2023
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
conteo_aumento = 0
max_conteo_aumento = 10

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
        
        # Se podría aplicar filtro gaussiano para difuminar bordes. Depende del video y de las condiciones de luz al momento de grabar
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
        
        # Dibujar contornos en la imagen qye luego se mostrará
        cv2.drawContours(imagen_inicial, [approx_inicial], -1, (0, 0, 255), 2)
        
        # Hay que obtener el valor X de la coordenada con Y más alto, para poner el dibujo la imagen
        x_array_inicial =  approx_inicial[:, :, 0].ravel()
        y_array_inicial = approx_inicial[:, :, 1].ravel()
        
        # SE OBTIENE POSICIÓN DE (X,Y) PARA GUARDAR ESTADO INICIAL  
        x_ordenado_inicial = np.sort(x_array_inicial)[::-1] 
        y_ordenado_inicial = np.sort(y_array_inicial)[::-1]

        # Tomar los valores de Y de las esquinas superiores del rectangulo detectado - Estos valores nos sirven para todos los frames
        y_o1 = y_ordenado_inicial[3]
        y_o2 = y_ordenado_inicial[2]
        
        # Obtener posición de pixel que se analiza para determinar deformación
        y_mean_actual = round((y_o1+y_o2)/2) 
        
        # Si se está analizando el primer frame se guarda la posición inicial para comparar posición próximos frames
        if first_frame:
            y_mean = round((y_o1+y_o2)/2)
            y_initial = y_mean
            first_frame = False
        else:
            # Si no estamos en el primer frame, se compara el pixel medido versus el del pixel medio del frame anterior. 
            # Si el pixel y_mean_actual es mayor, entonces la madera se 'contrajo' luego de ser estiarada.
            # Se hace un conteo de cuantas veces seguidas ocurre esta 'contracción'.
            if y_mean_actual > y_mean :
                conteo_aumento += 1
            else: 
                conteo_aumento=0
            
            # Si la contracción es mayor o igual a max_conteo_disminucion significa que hubo una contracción sostenida por lo que se asume que el experimento acabó.
            if conteo_aumento >= max_conteo_aumento:
                print("¡Disminución rápida detectada! Deteniendo la lectura del video luego de ", max_conteo_aumento," frames.")
                break
            
            # Si el pixel medio medido es menor, entonces significa que la madera se está 'Estirando'. 
            # Mientras esto ocurre se cuenta cuantos frames consecutivos se 'Estira' la madera.
            if y_mean_actual<y_mean:
                pixel_change_count_down += 1 
            else: 
                pixel_change_count_down = 0
            
            # Si la cantidad de frames que se 'estiró' consecutivamente es mayor o igual a max_pixel_change, se considera que hubo un estiramiento real y se actualiza
            # el valor de y_mean. 
            if pixel_change_count_down >= max_pixel_change:
                pixel_change_count_up=0
                y_mean = round((y_o1+y_o2)/2)
            
            # Con el valor de y_mean se calcula la deformación en pixeles.     
            pixel_deformation = y_mean - y_initial
        
        # Se añade la deformación a pixel_deformation_list, escalando por el pixel_mm_ratio para que se calcule la deformación en milimetros    
        pixel_deformation_list.append(pixel_deformation*pixel_mm_ratio)
        print("y_mean:", y_mean, "pixel_deformation:",pixel_deformation,"(y_o1+y_o2)/2:",y_mean_actual)
        cv2.imshow("Video", imagen_inicial)
        
        tecla = cv2.waitKey(1)
        if tecla == ord('q'):
                break
    
    else: break

cap.release()
cv2.destroyAllWindows()

# Calcular tiempo de procesamiento
second_end = time.time()
while_duration = second_end-second_init

print("while_duration:", while_duration)
print('Deformación Final=', pixel_deformation*pixel_mm_ratio)

#Exportar deformaciones a excel
data = {'Deformación': pixel_deformation_list}
df = pd.DataFrame(data)
nombre_archivo_excel = 'Output_Extension_Cam.xlsx'
df.to_excel(nombre_archivo_excel, index=False)