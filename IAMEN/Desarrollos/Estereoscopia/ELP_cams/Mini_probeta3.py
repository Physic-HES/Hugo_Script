import tkinter as tk
import cv2
from PIL import ImageTk, Image
import threading

# Función para obtener el video de la cámara y mostrarlo en el widget de la aplicación
def show_video_feed(video_source, video_widget):
    cap = cv2.VideoCapture(video_source)
    while True:
        ret, frame = cap.read()
        if ret:
            # Convertir la imagen capturada a RGB y escalarla al tamaño deseado
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))

            # Crear una imagen PIL a partir del marco
            img = Image.fromarray(frame)

            # Crear objeto ImageTk para mostrar en el widget
            img_tk = ImageTk.PhotoImage(image=img)

            # Actualizar la imagen en el widget
            video_widget.configure(image=img_tk)
            video_widget.image = img_tk

    # Liberar los recursos al finalizar
    cap.release()

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Video Feed")

# Crear los widgets para mostrar los videos
video_widget1 = tk.Label(root)
video_widget1.pack(side=tk.LEFT)

video_widget2 = tk.Label(root)
video_widget2.pack(side=tk.LEFT)

# Crear hilos separados para obtener y mostrar los videos
thread1 = threading.Thread(target=show_video_feed, args=(0, video_widget1))  # Primer video, índice 0
thread2 = threading.Thread(target=show_video_feed, args=(1, video_widget2))  # Segundo video, índice 1

# Iniciar los hilos
thread1.start()
thread2.start()

# Iniciar el bucle principal de la aplicación
root.mainloop()
