# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:04:32 2024

@author: CCTVAL
"""

# ---------------------------------------
# ------------- Tkinter -----------------
# ---------------------------------------


from tkinter import * 
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils

global video_path
global cap

def cerrar_ventana(event):
    if event.char == 'q' or event.keysym == 'Escape':
        root.destroy()

def elegir_video_a_visualizar():
    video_path=filedialog.askopenfilename(filetypes=[
        ("all video format",".mp4"),
        ("all video format",".avi"),
        ("all video format",".MOV")
    ])
    if len(video_path) > 0: 
        labelInfoVideoPath.configure(text=video_path)
        return video_path
    else: 
        labelInfoVideoPath.configure(text="Aun no se ha seleccionado nada")
        return ""

def visualizar_video():
    video_path = elegir_video_a_visualizar()
    if(len(video_path)>0): 
        cap=cv2.VideoCapture(video_path)
        while (cap.isOpened()):
            ret,frame=cap.read()
            if ret == True:
                frame = cv2.resize(frame,(1280,720))    

                # Convertir el frame de OpenCV a un objeto PhotoImage de Tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir BGR a RGB
                img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

                # Actualizar el Label con la nueva imagen
                labelVideo.configure(image=img_tk)
                labelVideo.image = img_tk

                # Esperar un breve tiempo para que se vea el video frame a frame
                root.update_idletasks()
                root.update()
            else:
                labelVideo.image = ""
                break
        cap.release()



root = Tk()
btnVisualizar = Button(root, text="Elegir y visualizar video", command=visualizar_video)
btnVisualizar.grid(column=0, row=0, padx=5, pady=5, columnspan=2)

LabelInfo1 = Label(root, text="Video de entrada")
LabelInfo1.grid(column=0, row=1)

labelInfoVideoPath = Label(root, text="Aun no se ha seleccionado nada")
labelInfoVideoPath.grid(column=1, row=1)

labelVideo = Label(root)
labelVideo.grid(column=0,row=2,columnspan=2)


# Asociar el evento de teclado a la función cerrar_ventana
root.bind('<Key>', cerrar_ventana)
root.mainloop()






