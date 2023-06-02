import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np


class DeformationAnalyzer:
    def __init__(self, window):
        self.window = window
        self.capture = None
        self.camera_frame = tk.Frame(self.window, width=800, height=600)
        self.camera_frame.pack()
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack()
        self.delay = 15  # Tiempo de actualización en milisegundos

        self.start_capture()

        self.window.mainloop()

    def start_capture(self):
        self.capture = cv2.VideoCapture(0)  # Cambiar a otro número si hay varias cámaras

        self.update_frame()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Convertir el frame a escala de grises para el procesamiento de correlación
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)

            if hasattr(self, 'prev_gray'):
                # Realizar correlación entre el frame actual y el frame anterior
                deformation_field = cv2.phaseCorrelate(self.prev_gray, gray)

                # Obtener la magnitud de la deformación
                magnitude = deformation_field[0]

                # Realizar aquí cualquier operación adicional con la magnitud de la deformación

                # Mostrar la magnitud de la deformación en la consola
                print("Magnitud de deformación:", magnitude)

            # Almacenar el frame actual para usarlo como referencia en la siguiente iteración
            self.prev_gray = gray.astype(np.float32)

            # Mostrar el frame en el canvas de tkinter
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            #self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.camera_label.config(image=image)
            self.camera_label.image = image

        self.window.after(self.delay, self.update_frame)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Deformation Analyzer")
    app = DeformationAnalyzer(window)
