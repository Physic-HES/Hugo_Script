import time
import cv2
import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def porcent(value):
    global umbral
    umbral= eval(value)/100
    print(f'El umbral de detección se fijó en {eval(value)} %')

def expo(value):
    global exp
    exp= eval(value)
    print(f'La exposicion se fijó en {exp}')

def guardar():
    name='dot3d_' + time.strftime('%Y%m%d',time.localtime()) + '.txt'
    np.savetxt(name,ptos,delimiter='\t')
    print('Los datos fueron guardados como '+name)


def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)


def ordenar(dot_des):
    dot2 = dot_des[np.argsort(dot_des[:, 1]), :]
    k = 0
    val = np.diff(dot2[:, 1]) > 2 * np.mean(np.diff(dot2[:, 1]))
    for i in range(val.shape[0]):
        if val[i]:
            dot2[k:i + 1, :] = dot2[np.argsort(dot2[k:i + 1, 0]) + k, :]
            k = i + 1
    dot2[k:, :] = dot2[np.argsort(dot2[k:, 0]) + k, :]
    return dot2


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


def dots(X1,X2,d,f,w,h):
    x1 = (X1[:, 0] - w/2)*3E-3
    y1 = (X1[:, 1] - h / 2) * 3E-3
    x2 = (X2[:, 0] - w/2)*3E-3
    y2 = (X2[:, 1] - h / 2) * 3E-3
    r_xy=np.multiply(np.c_[d/(x1-x2),d/(x1-x2)],np.c_[(x1+x2)/2,f*np.ones(x1.shape)])
    r_z=-.5*(y1*np.sqrt(((r_xy[:,0]+d/2)**2+r_xy[:,1]**2)/(x1**2+f**2))+
            y2*np.sqrt(((r_xy[:,0]-d/2)**2+r_xy[:,1]**2)/(x2**2+f**2)))
    dat=np.c_[r_xy,r_z]
    return dat


def get_ims():
    global X1, X2
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    w = 2560
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    h = 960
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cam.set(cv2.CAP_PROP_EXPOSURE, int(exp))
    rval, frame = cam.read()
    cv2.imshow(f'Modo Automatico de deteccion', frame)
    cv2.destroyAllWindows()
    time.sleep(0.01)
    fig1 = Figure()
    ax1 = fig1.add_subplot(projection='3d')
    #fig2 = Figure()
    #ax2 = fig2.add_subplot()
    cloud = ax1.scatter(0, 0, 0)
    ax1.set_xlabel('Eje X [mm]')
    ax1.set_ylabel('Eje Y [mm]')
    ax1.set_zlabel('Eje z [mm]')
    canvas1 = FigureCanvasTkAgg(fig1, master=marco1)
    canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    #canvas2 = FigureCanvasTkAgg(fig2, master=marco2)
    #canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    step=time.time()
    while True:
        global im1, im2, ptos
        rval, frame = cam.read()
        for k in range(2):
            red_image=frame[:,int(k*w/2):int((k+1)*w/2),2]
            (thresh , binaryIM) = cv2.threshold(red_image, int(umbral*np.max(red_image)), 255, cv2.THRESH_BINARY)
            output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
            (numLabels, labels, stats, centroids) = output
            image=frame[:,int(k*w/2):int((k+1)*w/2),:].copy()
            X1=np.array(np.zeros((2,1)))
            for i in range(1,numLabels):
                if stats[i,cv2.CC_STAT_AREA]>=int(0.75*np.mean(stats[1:,cv2.CC_STAT_AREA])):
                    (cX, cY) = centroids[i]
                    cv2.circle(image,(int(cX), int(cY)), 2, (0, 255, 0), -1)
                    cv2.rectangle(image, (int(cX-10), int(cY-10)), (int(cX+10), int(cY+10)), (0, 255, 0), 2)
                    if X1.shape==(2,1):
                        X1=np.array([cX,cY])
                    else:
                        X1=np.c_[X1,np.array([cX,cY])]
            if k == 0:
                im1 = X1.T.copy()
                im1=ordenar(im1)
                imageL=image
            elif k == 1:
                im2 = X1.T.copy()
                im2=ordenar(im2)
                imageR=image
        image2=cv2.hconcat([imageL,imageR])
        #ax2.imshow(rescale_frame(image2,15))
        #ax2.axis('off')
        if im1.shape[0]==im2.shape[0]:
            ptos=dots(im1,im2,60,4.3,int(w/2),h)
            cloud._offsets3d = (ptos[:,0],ptos[:,1],ptos[:,2])
            #canvas1.draw()
            #canvas2.draw()
            time.sleep(0.001)
            ax1.clear()
            #ax2.clear()
            print(f'Dimention Ok at {1/(time.time()-step):3.3} Hz of Sample Rate')
        elif np.abs(im1.shape[0]-im2.shape[0])>0:
            print('Dimention is Fail')
        step=time.time()


app = tk.Tk()
s=ttk.Style()
s.theme_use('alt')
app.title('Fotogrametria 3D - IAMEND')
marco1 = tk.LabelFrame(app,text='Nube de puntos')
marco1.pack(side=tk.LEFT)
#canvas1 = tk.Canvas(marco1)
#canvas1.pack(anchor='nw',fill='both',expand=1)

#marco2 = tk.LabelFrame(app,text='Estereo visión')
#marco2.pack(anchor='nw',fill='both',expand=1)
#canvas2 = tk.Canvas(marco2)
#canvas2.pack(anchor='nw',fill='both',expand=1)

marco3 = tk.LabelFrame(app,text='Configuración')
marco3.pack(anchor='nw',fill='both',expand=1)

label_slider1 = tk.Label(marco3, text="Umbral de intensidad máxima promedio")
label_slider1.pack()
slider1 = ttk.Scale(marco3, from_=0, to=100, command=porcent)
slider1.set(40)
slider1.pack(pady=10)

label_slider2 = tk.Label(marco3, text="Exposición de la Camara")
label_slider2.pack()
slider2 = ttk.Scale(marco3, from_=0, to=1866, command=expo)
slider2.set(140)
slider2.pack(pady=10)

# Botón para guardar datos
button_save = tk.Button(marco3, text="Guardar datos", command=guardar)
button_save.pack(pady=10)

get_ims()
app.mainloop()


