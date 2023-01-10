import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import time
from PIL import Image, ImageTk

#APP
root = tk.Tk()
#root.geometry('850x650')
root.title('Digital Image Correlation - IAMEND')
marco1 = tk.LabelFrame(root,text='Previsualización',height=25,width=50)
marco1.pack(side=tk.LEFT)
mens = tk.Label(marco1,text='Sin señal de video')
mens.pack()
label_widget = tk.Label(marco1)
label_widget.pack()
root.bind('<Escape>', lambda e: root.quit())

pts=np.zeros((4,2),np.int)
count=0


def get_mouse(event,x,y,flags,params):
    global count
    if event == cv2.EVENT_LBUTTONDOWN:
        pts[count]=x,y
        count+=1


def initcam():
    vid = cv2.VideoCapture(int(camID.get()))
    width, height = 800, 600
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def open_camera():
        if vid.isOpened():
            rval, frame = vid.read()
            mens.config(text='Camara iniciada en el puerto '+ camID.get())
            mens.pack()
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)
            photo_image = ImageTk.PhotoImage(image=captured_image)
            label_widget.photo_image = photo_image
            label_widget.configure(image=photo_image)
        else:
            mens.config(text='No se encontro una camara en ese puerto')
            mens.pack()
        label_widget.after(10, open_camera)

    open_camera()

marco2 = tk.LabelFrame(root,text='Puerto de entrada')
marco2.pack(side=tk.RIGHT)

camID = ttk.Entry(marco2,width=1)
camID.pack(side=tk.LEFT)
camID.insert(0,"0")

button1 = tk.Button(marco2, text="Iniciar Camara", command=initcam)
button1.pack(side=tk.RIGHT)

root.mainloop()