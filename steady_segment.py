# -*- coding: utf-8 -*-
"""
- STEADY SEGMENT - 

Código tomado del proyecto Double Target para sacar ideas de la utilización de OpenCV en la identificación de imagenes de referencia. 

Created on 'unkwowm'
@author: 'unknown'
"""

##distancia entre el sensor y un target 273[mm] dx = 160,dy = 210,thresholdGrey = 88,thresholdAreaMin = 30000,thresholdAreaMax = 60000
##distancia entre el sensor y un target 650[mm] dx = 45,dy = 50,thresholdGrey = 190,thresholdAreaMin = 1500,thresholdAreaMax = 2000
##distancia entre el sensor y un target 650[mm] dx = 190,dy = 200,thresholdGrey = 135,thresholdAreaMin = 40000,thresholdAreaMax = 60000


import os
import sys
import numpy as np
import cv2
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
from time import sleep


def draw_text(img, text,
          font=cv2.FONT_HERSHEY_SIMPLEX,
          pos=(10, 10),
          font_scale=0.5,
          font_thickness=2,
          text_color=(255, 255, 255),
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h - 1), font, font_scale, text_color, font_thickness)

    return text_size

color = {"primary":(56,106,255),
		"secondary":(224,208,158),
		"tertiary":(142,134,92),
		"quaternary":(63,72,25)}
# capture from web cam
cap = cv2.VideoCapture(1)
dx = 300
dy = 200
step = 5
thresholdGrey = 115
thresholdAreaMin = 40000
thresholdAreaMax = 60000
setCentroid = False
initialPos = None
initialSize = None
isMeasure = False
frameOut = 5


repeticiones_del_bucle = 1000000

rutina = [3]
vueltas = 0
paso_actual = 0
target = None
esperar = False

listaP = []
fig , axs = plt.subplots(1,1,figsize=(15,8))


while True:
	tecla = cv2.waitKey(1)
	if tecla == ord('q'):
		break
	if isMeasure:
		if not esperar:
			sleep(0.1)
			target = rutina[paso_actual%len(rutina)]

			#Caso especial target 0 o target 6: en estas posciones no hay target
			if target == 0 or target == 6:
				dataOutputFile = open(testFile, "a")
				dataOutputFile.write(f"{target}:{0:.2f}:{None}:{None}:{None}:{pd.Timestamp.now().strftime('%Y-%m-%d_%H_%M_%S')}\n")
				dataOutputFile.close()
				paso_actual += 1
				vueltas += 1 if paso_actual%len(rutina) == 0 else 0
				if vueltas >= repeticiones_del_bucle:
					vueltas = 0
					isMeasure = False
					listaP = []
					paso_actual = 0
					target = None
					print("termino experimento")
				continue
	ret, cv_img = cap.read()
	if not ret:
		continue
	h,w,_ = cv_img.shape
	if tecla == ord('w'):
		dy += step if dy + step < h//2 else 0
	if tecla == ord('s'):
		dy -= step if dy - step > 0 else 0
	if tecla == ord('a'):
		dx += step if dx + step < w//2 else 0
	if tecla == ord('d'):
		dx -= step if dx - step > 0 else 0
	if tecla == ord('u'):
		thresholdGrey += 1 if thresholdGrey < 255 else 0
	if tecla == ord('j'):
		thresholdGrey -= 1 if thresholdGrey > 0 else 0
	if tecla == ord('y'):
		thresholdAreaMin += step if thresholdAreaMin + step < thresholdAreaMax - 100 else 0
	if tecla == ord('h'):
		thresholdAreaMin -= step if thresholdAreaMin - step > 100 else 0
	if tecla == ord('t'):
		thresholdAreaMax += step if thresholdAreaMax < 100000 else 0
	if tecla == ord('g'):
		thresholdAreaMax -= step if thresholdAreaMax - step > thresholdAreaMin + 100 else 0
	if tecla == ord('x'):
		setCentroid = True
		posicion_inicial = 0xCC7BA1#motor_movement.get_motor_position()
	# Opcion de iniciar un bucle de mediciones y dejarlo corriendo.
	if tecla == ord('c') and not isMeasure:
		testFile = f"test-{''.join(map(str,rutina))}-{pd.Timestamp.now().strftime('%Y-%m-%d_%H_%M')}.csv"
		isMeasure = True
		continue
	
	cv2.rectangle(cv_img, (w//2-dx,h//2-dy), (w//2+dx,h//2+dy), (255,0,0), 2)
	crop = cv_img[h//2-dy:h//2+dy,w//2-dx:w//2+dx,:].copy()
	gray_image = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray_image,thresholdGrey,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	contoursFilter = []
	
	#Detectar target y filtrara por area		
	for c in contours:
		area = cv2.contourArea(c)
		#print(area)
		if not (thresholdAreaMin < area < thresholdAreaMax):
			continue
		cdelta = c + np.array([[[w//2 - dx,h//2 - dy]]])
		contoursFilter.append(cdelta)
	contours = contoursFilter
	
	#frame out si no dectecta target por 5 frame se detiene la medicion
	if len(contours) <=0 and isMeasure:
		frameOut-=1
		if frameOut == 0:
			print("no se detectaron targets, abortando....")
			vueltas = 0
			paso_actual = 0
			listaP = []
			isMeasure = False
			target = None
		continue
	frameOut = 5
	
	for i,c in enumerate(contours):
		M = cv2.moments(c)
		if M["m00"] != 0:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
		else:
			continue
		
		ellipse = cv2.fitEllipse(c)
		(x,y),(a,b),_ = ellipse
		cv2.circle(cv_img, (cX, cY), 5, color["primary"], -1)
		cv2.circle(cv_img, (int(x), int(y)), 4, color["quaternary"], -1)
		a,b = (a,b) if a > b else (b,a)
		e = np.sqrt(a**2-b**2)/a
		sizePixel = c[:,:,1].max() - c[:,:,1].min() 
		cv2.drawContours(cv_img, [c], -1, color["primary"], 2)
		cv2.ellipse(cv_img,ellipse, color["quaternary"], 1)
		cv2.putText(cv_img, f"target {i+1} ({cX},{cY})", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, color["primary"], 2)
		
		if setCentroid and i+1==1:
			initialPos = (cX,cY)
			setCentroid = False
			initialSize = sizePixel
			print(f"res:{5e-3/initialSize}")

		if isMeasure and initialPos is not None and i+1==1:
			x0,y0 = initialPos
			deltaX = (cX-x0)*(5e-3/initialSize)*1e6
			deltaY = (cY-y0)*(5e-3/initialSize)*1e6
			errorCalculado = np.sqrt((deltaX)**2+(deltaY)**2)*(-1 if deltaX < 0 else 1)
			dataOutputFile = open(testFile, "a")
			dataOutputFile.write(f"{target}:{0:.2f}:{errorCalculado:.8f}:{deltaX:.8f}:{deltaY:.8f}:{pd.Timestamp.now().strftime('%Y-%m-%d_%H_%M_%S')}\n")
			dataOutputFile.close()
			if target == 3:
				listaP.append(errorCalculado)
				if len(listaP)>=3:
					axs.clear()
					bin_count = int(np.ceil(np.log2(len(listaP))) + 1)
					mu,sigma=np.mean(listaP),np.std(listaP)
					height,ranges,_ = axs.hist(listaP,bins=bin_count,density=True,edgecolor='black',lw=2,label=f"Error Histogram $3\sigma = {3*sigma:.2f}$")
					factor = (100*np.diff(ranges))
					middles = ranges[:-1]+np.diff(ranges)/2
					upper = height+np.sqrt(height*factor)/factor
					lower = height-np.sqrt(height*factor)/factor
					axs.vlines(middles,upper,lower,color="k",lw=2)
					axs.set_title(f"Error Distribution {len(listaP)} measurements",fontsize=20)
					xmin,xmax=axs.get_xlim()
					x = np.arange(xmin,xmax,.0001)
					plt.plot(x, norm.pdf(x, mu,sigma),label=f"$N(\mu={mu:.2f},\sigma²={sigma**(2):.2f})$")
					plt.xlabel("Distance [$\mu$m]",size=16)
					plt.ylabel("Frecuency",size=16)
					plt.legend(loc="best",fontsize=14)
					plt.grid()
					fig.canvas.draw()
					img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
					img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
					img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
					cv2.imshow("plot",img)
			if not esperar:
				paso_actual += 1
				vueltas += 1 if paso_actual%len(rutina) == 0 else 0
				if vueltas >= repeticiones_del_bucle:
					vueltas = 0
					isMeasure = False
					listaP = []
					paso_actual = 0
					target = None
					print("termino experimento")
	motor_pos = 0xCC7BA1#motor_movement.get_motor_position()
	draw_text(cv_img,f"Params = dx:{dx}, dy:{dy}, thG:{thresholdGrey}, thAMin:{thresholdAreaMin}, thAMax:{thresholdAreaMax}, MotorPos:{motor_pos}",pos=(cv_img.shape[0]//2,5))
	
	#take photo with data info
	if tecla == ord('z'):
		cv2.imwrite("photo.png", cv_img)
	cv2.imshow("camara",cv_img)
	#cv2.imshow("kmeans",segmented_frame)
	cv2.imshow("grey",gray_image)
	cv2.imshow("thresh",thresh)
	
# shut down capture system
cap.release()
cv2.destroyAllWindows()
