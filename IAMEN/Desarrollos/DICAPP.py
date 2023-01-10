import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
import time
from PIL import Image, ImageTk

#APP
root = tk.Tk()
label_widget = tk.Label(root)
label_widget.pack()
root.bind('<Escape>', lambda e: root.quit())

#DIC
camID=0
cam = cv2.VideoCapture(camID)
w = int(cam.get(3))
h = int(cam.get(4))
zona=63 #tamaño de zonas donde se correlaciona una porcion interior
div=zona/3
campo=80 #Cantidad de discretizaciones (discrt)
print(f'Tamaño de camara: {w}x{h}')
raw_in = 60
col_in = 170
discrt = 4
rgy=range(int(raw_in+zona/2),int(raw_in+zona/2+campo*discrt),int(discrt))
rgx=range(int(col_in+zona/2),int(col_in+zona/2+campo*discrt),int(discrt))
map_def_x = np.zeros((len(rgy), len(rgx)))
map_def_y = np.zeros((len(rgy), len(rgx)))
map_def = np.zeros((len(rgy), len(rgx)))
image_stres = np.zeros((h, w))
def ciclo():
    rval, frame_ = cam.read()
    frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
    time.sleep(0.1)
    rval, frame2_ = cam.read()
    b,g,r=cv2.split(frame2_)
    frame2_RGB=cv2.merge((b,g,r))
    frame2 = cv2.cvtColor(frame2_, cv2.COLOR_BGR2GRAY)
    nn,kk=0,0
    for n in rgy:
        for k in rgx:
            sub_frame_0 = frame[int(n-zona/2):int(n+zona/2),int(k-zona/2):int(k+zona/2)]
            sub_frame_1 = frame2[int(n-zona/2):int(n+zona/2),int(k-zona/2):int(k+zona/2)]
            sub_frame = sub_frame_0[int(div):int(2*div), int(div):int(2*div)]
            a,b,c,sub_int_def=cv2.minMaxLoc(cv2.matchTemplate(sub_frame_1,sub_frame,cv2.TM_CCOEFF_NORMED))
            map_def_x[nn, kk]+=sub_int_def[0]-div
            map_def_y[nn, kk]+=sub_int_def[1]-div
            map_def[nn,kk]=np.sqrt(map_def_x[nn, kk]**2+map_def_y[nn, kk]**2)
            kk+=1
        nn+=1
        kk=0
    if discrt>1:
        mapa=cv2.resize(map_def,(int(campo*discrt),int(campo*discrt)), interpolation =cv2.INTER_AREA)
    else:
        mapa=map_def
    stress_x = (mapa[:-int(discrt),int(discrt):]-mapa[:-int(discrt),:-int(discrt)])/(2*discrt)
    stress_y = (mapa[int(discrt):,:-int(discrt)]-mapa[:-int(discrt),:-int(discrt)])/(2*discrt)
    stress=np.sqrt(stress_x**2+stress_y**2)
    image_stres[int(raw_in+zona/3+discrt/2):int(raw_in+zona/3+(campo-1)*discrt+discrt/2),
                    int(col_in+zona/3+discrt/2):int(col_in+zona/3+(campo-1)*discrt+discrt/2)]=5*mapa[:-int(discrt),:-int(discrt)]
    stress_color=cv2.applyColorMap(image_stres.astype('uint8'), cv2.COLORMAP_INFERNO)
    merge=cv2.add(frame2_RGB,stress_color)
    opencv_image = cv2.cvtColor(merge, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image)
    photo_image = ImageTk.PhotoImage(image=captured_image)
    #Update frame in APP
    label_widget.photo_image = photo_image
    label_widget.configure(image=photo_image)
    label_widget.after(10, ciclo)

button1 = tk.Button(root, text="Preview DIC", command=ciclo)
button1.pack()
root.mainloop()

