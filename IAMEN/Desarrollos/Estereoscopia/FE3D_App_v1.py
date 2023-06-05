import time
import tkinter as tk
from tkinter import ttk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
import numpy as np


class CameraApp:
    def __init__(self, root):
        global w, h
        self.root = root
        self.root.title("Fotogrametria 3D mediante estereo visión")

        # Crear el marco principal
        self.main_frame = tk.Frame(self.root)

        # Crear el marco para el scatter 3D
        self.scatter_frame = tk.LabelFrame(self.main_frame, text='Nube de puntos', width=480, height=480)
        self.scatter_frame.pack(side=tk.LEFT)
        self.main_frame.pack(pady=10)

        # Crear el marco para la imagen de la cámara
        self.camera_frame = tk.LabelFrame(self.main_frame,text='Estereo Visión', width=640, height=480)
        self.camera_frame.pack(anchor='nw', fill='both', expand=1)

        # Crear los sliders y el boton de guardado
        self.marco3 = tk.LabelFrame(self.main_frame, text='Configuración')
        self.marco3.pack(anchor='nw', fill='both', expand=1)

        # Barra para el control del umbral de deteccion
        self.label_slider1 = tk.Label(self.marco3, text="Umbral de detección")
        self.label_slider1.pack()
        self.slider1 = ttk.Scale(self.marco3, from_=0, to=100, command=self.porcent)
        self.slider1.set(40)
        self.slider1.pack(pady=10)

        # Barra para el control de la exposicion
        self.label_slider2 = tk.Label(self.marco3, text="Exposición de la Camara")
        self.label_slider2.pack()
        self.slider2 = ttk.Scale(self.marco3, from_=0, to=1866, command=self.expo)
        self.slider2.set(140)
        self.slider2.pack(pady=10)

        # Botón para guardar datos
        self.button_save = tk.Button(self.marco3, text="Guardar datos", command=self.guardar)
        self.button_save.pack(pady=10)

        # Crear una etiqueta para la imagen de la cámara
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()

        # Crear una figura para el scatter 3D
        self.scatter_fig = Figure(figsize=(5, 5), dpi=100)
        self.scatter_ax = self.scatter_fig.add_subplot(111, projection='3d')

        # Crear el lienzo de Matplotlib para el scatter 3D
        self.scatter_canvas = FigureCanvasTkAgg(self.scatter_fig, master=self.scatter_frame)
        self.scatter_canvas.draw()
        self.scatter_canvas.get_tk_widget().pack()

        # Inicializar la configuracion de la camara
        self.cap = cv2.VideoCapture(2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        w = 2560
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        h = 960
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, int(exp))

        # Inicializar la captura de la cámara
        self.update_camera()

    def update_camera(self):
        global im1, im2, ptos
        # Capturar un fotograma de la cámara
        self.cap.set(cv2.CAP_PROP_EXPOSURE, int(exp))
        ret, frame = self.cap.read()

        if ret:
            # Convertir la imagen de BGR a RGB
            frame_rgb = cv2.cvtColor(self.rescale_frame(frame,25), cv2.COLOR_BGR2RGB)

            # Deteccion de puntos
            for k in range(2):
                red_image = frame[:, int(k * w / 2):int((k + 1) * w / 2), 2]
                (thresh, binaryIM) = cv2.threshold(red_image, int(umbral * np.max(red_image)), 255, cv2.THRESH_BINARY)
                output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
                (numLabels, labels, stats, centroids) = output
                image = frame[:, int(k * w / 2):int((k + 1) * w / 2), :].copy()
                X1 = np.array(np.zeros((2, 1)))
                for i in range(1, numLabels):
                    if stats[i, cv2.CC_STAT_AREA] >= int(0.75 * np.mean(stats[1:, cv2.CC_STAT_AREA])):
                        (cX, cY) = centroids[i]
                        cv2.circle(image, (int(cX), int(cY)), 2, (0, 255, 0), -1)
                        cv2.rectangle(image, (int(cX - 10), int(cY - 10)), (int(cX + 10), int(cY + 10)), (0, 255, 0), 2)
                        if X1.shape == (2, 1):
                            X1 = np.array([cX, cY])
                        else:
                            X1 = np.c_[X1, np.array([cX, cY])]
                if k == 0:
                    im1 = X1.T.copy()
                    im1 = self.ordenar(im1)
                    imageL=image
                elif k == 1:
                    im2 = X1.T.copy()
                    im2 = self.ordenar(im2)
                    imageR=image
            image2 = cv2.hconcat([imageL, imageR])

            # Mostrar la imagen en la etiqueta de la cámara
            image2_=cv2.cvtColor(self.rescale_frame(image2, 20),cv2.COLOR_BGR2RGB)
            # Redimensionar la imagen para ajustarse al marco
            image = Image.fromarray(image2_)
            photo = ImageTk.PhotoImage(image=image)
            self.camera_label.config(image=photo)
            self.camera_label.image = photo


        # Realizar la iteración del scatter 3D
        if im1.shape[0] == im2.shape[0]:
            self.scatter_ax.cla()
            ptos = self.dots(im1, im2, 60, 4.3, int(w / 2), h) # Datos aleatorios para el scatter 3D
            self.scatter_ax.scatter(ptos[:, 0], ptos[:, 1], ptos[:, 2])
            self.scatter_ax.set_xlim([np.min(ptos[:, 0]) - 10, np.max(ptos[:, 0]) + 10])
            self.scatter_ax.set_ylim([150, 250])
            self.scatter_ax.set_zlim([np.min(ptos[:, 2]) - 10, np.max(ptos[:, 2]) + 10])
            self.scatter_ax.set_title('3D Reconstruction')
            self.scatter_ax.set_xlabel('Eje X [mm]')
            self.scatter_ax.set_ylabel('Eje Y [mm]')
            self.scatter_ax.set_zlabel('Eje z [mm]')
            self.axisEqual3D(self.scatter_ax)
            self.scatter_canvas.draw()

        # Llamar a esta función de nuevo después de 10 milisegundos
        self.root.after(10, self.update_camera)

    def porcent(self,value):
        global umbral
        umbral = eval(value) / 100
        print(f'El umbral de detección se fijó en {eval(value)} %')

    def expo(self,value):
        global exp
        exp = eval(value)
        print(f'La exposicion se fijó en {exp}')

    def guardar(self):
        name = 'dot3d_' + time.strftime('%Y%m%d', time.localtime()) + '.txt'
        np.savetxt(name, ptos, delimiter='\t')
        print('Los datos fueron guardados como ' + name)

    def ordenar(self,dot_des):
        dot2 = dot_des[np.argsort(dot_des[:, 1]), :]
        k = 0
        val = np.diff(dot2[:, 1]) > 2 * np.mean(np.diff(dot2[:, 1]))
        for i in range(val.shape[0]):
            if val[i]:
                dot2[k:i + 1, :] = dot2[np.argsort(dot2[k:i + 1, 0]) + k, :]
                k = i + 1
        dot2[k:, :] = dot2[np.argsort(dot2[k:, 0]) + k, :]
        return dot2

    def rescale_frame(self,frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    def dots(self,X1, X2, d, f, w, h):
        x1 = (X1[:, 0] - w / 2) * 3E-3
        y1 = (X1[:, 1] - h / 2) * 3E-3
        x2 = (X2[:, 0] - w / 2) * 3E-3
        y2 = (X2[:, 1] - h / 2) * 3E-3
        r_xy = np.multiply(np.c_[d / (x1 - x2), d / (x1 - x2)], np.c_[(x1 + x2) / 2, f * np.ones(x1.shape)])
        r_z = -.5 * (y1 * np.sqrt(((r_xy[:, 0] + d / 2) ** 2 + r_xy[:, 1] ** 2) / (x1 ** 2 + f ** 2)) +
                     y2 * np.sqrt(((r_xy[:, 0] - d / 2) ** 2 + r_xy[:, 1] ** 2) / (x2 ** 2 + f ** 2)))
        dat = np.c_[r_xy, r_z]
        return dat

    def axisEqual3D(self,ax):
        extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
        sz = extents[:, 1] - extents[:, 0]
        centers = np.mean(extents, axis=1)
        maxsize = max(abs(sz))
        r = maxsize / 2
        for ctr, dim in zip(centers, 'xyz'):
            getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

root = tk.Tk()
app = CameraApp(root)
root.mainloop()
