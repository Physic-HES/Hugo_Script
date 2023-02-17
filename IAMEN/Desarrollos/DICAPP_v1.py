import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import time
from PIL import Image, ImageTk

#APP
root = tk.Tk()
root.title('Digital Image Correlation - IAMEND')
marco1 = tk.LabelFrame(root,text='Previsualización')
marco1.pack(side=tk.LEFT)
canvas = tk.Canvas(marco1)
canvas.pack(anchor='nw',fill='both',expand=1)
mens = tk.Label(marco1,text='Sin señal de video')
mens.pack()
root.bind('<Escape>', lambda e: root.quit())

photo_image=None
line1,line2,line3,line4=None,None,None,None
count=0
pts=np.zeros((4,2),np.int64)

def get_x_and_y(event):
    global count
    if count<=3:
        pts[count] = event.x, event.y
        count+=1

def lines(count):
    line1 = canvas.create_line((pts[0][0], pts[0][1], pts[0][0], pts[0][1]),
                               fill='red',
                               width=2)
    line2 = canvas.create_line((pts[0][0], pts[0][1], pts[0][0], pts[0][1]),
                               fill='red',
                               width=2)
    line3 = canvas.create_line((pts[0][0], pts[0][1], pts[0][0], pts[0][1]),
                               fill='red',
                               width=2)
    line4 = canvas.create_line((pts[0][0], pts[0][1], pts[0][0], pts[0][1]),
                               fill='red',
                               width=2)
    if count == 2:
        canvas.coords(line1, pts[0][0], pts[0][1], pts[1][0], pts[0][1])
        canvas.coords(line2, pts[0][0], pts[0][1], pts[1][0], pts[0][1])
        canvas.coords(line3, pts[0][0], pts[0][1], pts[1][0], pts[0][1])
        canvas.coords(line4, pts[0][0], pts[0][1], pts[1][0], pts[0][1])
    if count >= 3:
        canvas.coords(line1, pts[0][0], pts[0][1], pts[1][0], pts[0][1])
        canvas.coords(line2, pts[0][0], pts[2][1], pts[1][0], pts[2][1])
        canvas.coords(line3, pts[0][0], pts[0][1], pts[0][0], pts[2][1])
        canvas.coords(line4, pts[1][0], pts[0][1], pts[1][0], pts[2][1])

def initcam():
    vid = cv2.VideoCapture(int(camID.get()))
    width, height = 800, 600
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def open_camera():
        global photo_image, line1, line2, line3, line4
        if vid.isOpened():
            rval, frame = vid.read()
            mens.config(text='Camara iniciada en el puerto '+ camID.get())
            mens.pack()
            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            captured_image = Image.fromarray(opencv_image)
            photo_image = ImageTk.PhotoImage(image=captured_image)
            canvas.config(height=photo_image.height(), width=photo_image.width())
            canvas.create_image(0, 0, image=photo_image, anchor='nw')
            lines(count)
        else:
            mens.config(text='No se encontro una camara en ese puerto')
            mens.pack()
        canvas.after(1,open_camera)

    open_camera()


marco2 = tk.LabelFrame(root,text='Configuración')
marco2.pack(side=tk.RIGHT)

puerto= tk.Label(marco2,text='Puerto de entrada: ')
puerto.grid(row=0,column=0)
camID = ttk.Entry(marco2,width=1)
camID.insert(0,'0')
camID.grid(row=0,column=1)

canvas.bind('<Button-1>',get_x_and_y)


step= tk.Label(marco2,text='Discretización: ')
step.grid(row=1,column=0)
step_N = ttk.Entry(marco2,width=2)
step_N.insert(0,'32')
step_N.grid(row=1,column=1)

mask= tk.Label(marco2,text='Tamaño de Mascara: ')
mask.grid(row=2,column=0)
mask_N = ttk.Entry(marco2,width=2)
mask_N.insert(0,'16')
mask_N.grid(row=2,column=1)

button1 = tk.Button(marco2, text="Iniciar Camara", command=initcam)
button1.grid(row=3,column=0)
button2 = tk.Button(marco2, text="DIC", command=initcam)
button2.grid(row=3,column=1)


root.mainloop()