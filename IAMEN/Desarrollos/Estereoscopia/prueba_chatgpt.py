import tkinter as tk
from tkinter import ttk
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Crear datos de ejemplo
num_points = 100
x = np.random.rand(num_points)
y = np.random.rand(num_points)
z = np.random.rand(num_points)

# Crear ventana principal
window = tk.Tk()
window.title("Aplicación de ejemplo")
window.geometry("800x600")

# Crear figura de Matplotlib y eje 3D
fig = Figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")

# Crear scatter inicial
scatter = ax.scatter(x, y, z)

# Crear lienzo de Matplotlib en tkinter
marco1=tk.LabelFrame(window,text='Nube de puntos')
marco1.pack()
canvas = FigureCanvasTkAgg(fig, master=marco1)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Función para actualizar los datos del scatter en cada iteración
def update_scatter():
    # Generar nuevos datos de ejemplo
    x_new = np.random.rand(num_points)
    y_new = np.random.rand(num_points)
    z_new = np.random.rand(num_points)

    # Actualizar los datos del scatter
    scatter._offsets3d = (x_new, y_new, z_new)

    # Actualizar el gráfico en la interfaz de usuario
    canvas.draw_idle()


# Botón para iniciar la iteración
marco2=tk.LabelFrame(window,text='Iteracion')
marco2.pack()
button_start = ttk.Button(marco2, text="Iniciar iteración", command=update_scatter)
button_start.pack(pady=10)

# Iniciar el bucle de eventos de la aplicación
window.mainloop()
