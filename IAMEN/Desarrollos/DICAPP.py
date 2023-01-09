import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
import numpy as np
import time
from PIL import Image, ImageTk

root = tk.Tk()

#DIC
camID=0
#figure1 = plt.Figure(figsize=(6, 5), dpi=100)
#ax1 = figure1.add_subplot(111)
#bar1 = FigureCanvasTkAgg(figure1, root)
#bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
label_widget = tk.Label(root)
label_widget.pack()
root.bind('<Escape>', lambda e: root.quit())
cam = cv2.VideoCapture(camID)
#cam.set(cv2.CAP_PROP_EXPOSURE, -4) #-4 es 80ms
w = int(cam.get(3))
h = int(cam.get(4))
zona=63 #tamaño de zonas donde se correlaciona una porcion interior
div=zona/3
campo=80 #Cantidad de discretizaciones (discrt)
print(f'Tamaño de camara: {w}x{h}')
#cam.set(3, w)
#cam.set(4, h)
#if cam.isOpened():  # try to get the first frame
#    rval, frame_0 = cam.read()
#else:
#    rval = False

raw_in = 60
col_in = 170
discrt = 2
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
    #stress = np.where(stress_x+stress_y>=0,np.sqrt(stress_x**2+stress_y**2),0)
    #stress = np.where(stress_x+stress_y< 0, -np.sqrt(stress_x ** 2 + stress_y ** 2), stress)
    #stress-=np.min(stress)
    stress=np.sqrt(stress_x**2+stress_y**2)
    #stress=normalize(stress,0,255)
    image_stres[int(raw_in+zona/3+discrt/2):int(raw_in+zona/3+(campo-1)*discrt+discrt/2),
                    int(col_in+zona/3+discrt/2):int(col_in+zona/3+(campo-1)*discrt+discrt/2)]=5*mapa[:-int(discrt),:-int(discrt)]
    stress_color=cv2.applyColorMap(image_stres.astype('uint8'), cv2.COLORMAP_INFERNO)
    merge=cv2.add(frame2_RGB,stress_color)
    opencv_image = cv2.cvtColor(merge, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image)
    photo_image = ImageTk.PhotoImage(image=captured_image)
    label_widget.photo_image = photo_image
    label_widget.configure(image=photo_image)
    label_widget.after(10, ciclo)
    #key = cv2.waitKey(20)
    #if key & 0xFF == ord('q'):  # exit on q
    #    break

button1 = tk.Button(root, text="Preview DIC", command=ciclo)
button1.pack()
root.mainloop()

