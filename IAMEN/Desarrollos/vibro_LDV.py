import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from scipy.signal import spectrogram

# Función para generar la señal simulada del fotodetector
def generate_signal(shift_freq, osc_freq, t):
    m=(1-0.001*np.abs(2*np.pi*osc_freq*4*np.sin(2*np.pi*osc_freq*t)))
    signal = 1+m*np.sin(200*np.pi*shift_freq*t-4*np.pi*osc_freq*np.cos(2*np.pi*(osc_freq)*t))
    return signal

# Función para actualizar los gráficos
def update_plot(shift_freq, osc_freq):
    fig.clear()

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(224)

    # Dibujar el diagrama del setup experimental
    laser = Rectangle((-2.5, -0.25), 1.5, 0.5, edgecolor='black', facecolor='none') # laser
    ax1.add_patch(laser) 
    fd = Rectangle((8, 3-0.25), 0.25, 0.5, edgecolor='black', facecolor='black') # FD
    ax1.add_patch(fd) 
    ob = Rectangle((10, -1), 0.1, 2, edgecolor='black', facecolor='black') # Objeto
    ax1.add_patch(ob) 
    bragg_rect = Rectangle((2.5, -0.25), 2, 0.5, edgecolor='black', facecolor='none') # Red de Bragg
    ax1.add_patch(bragg_rect) 

    # Anotaciones
    ax1.text(2.5,0.5,'Red de Bragg')
    ax1.text(-0.5,-1-0.25/2,r'BS$_1$')
    ax1.text(7-0.5,-1-0.25/2,r'BS$_3$')
    ax1.text(7-0.5,3+0.75,r'BS$_2$')
    ax1.text(-0.5,3+0.75,'M')
    ax1.text(-2.5,0.5,'Láser')
    ax1.annotate(text=' ', xy=(10+0.25/2-0.5,1.25), xytext=(10+0.25/2+0.5,0.9+0.25), arrowprops=dict(arrowstyle='<->'))
    ax1.arrow(1,-0.25,0.75,0,head_width=0.15)
    ax1.text(1.25,-0.75,r'$f_0$')
    ax1.arrow(1,3+0.25,0.75,0,head_width=0.15)
    ax1.text(1.25,3+0.5,r'$f_0$')
    ax1.arrow(8,-0.25,1,0,head_width=0.15)
    ax1.text(8,-0.75,r'$f_0+\Delta f_B$')
    ax1.arrow(9+0.15,0.25,-1,0,head_width=0.15)
    ax1.text(7.75,0.5,r'$f_0+\Delta f_B+\Delta f_D$')

    for (x, y) in [(0, 0), (7, 3)]: #BS 1 y 2
        ax1.add_patch(Rectangle((x-0.5, y-0.5), 1, 1, edgecolor='black', facecolor='none'))
        ax1.plot([x-0.5, x+0.5], [y-0.5, y+0.5], 'k')
    ax1.plot([0-0.5, 0+0.5], [3-0.5, 3+0.5], 'k') # Espejo
    ax1.add_patch(Rectangle((7-0.5, 0-0.5), 1, 1, edgecolor='black', facecolor='none')) # BS3
    ax1.plot([7-0.5, 7+0.5], [0+0.5, 0-0.5], 'k') # BS3

    ax1.plot([0, 0, 1, 8], [0, 3, 3, 3], 'r', linewidth=2)  # Haz de referencia (rojo)
    ax1.plot([-1, 3.5], [0, 0], 'r', linewidth=2)              # Haz inicial (rojo)
    ax1.plot([3.5, 10], [0, 0], color=(1-0.75*shift_freq/10, shift_freq/10, 0), linewidth=2)  # Haz después de Bragg (magenta)
    ax1.plot([7, 7], [0.05, 2.95], color=(1-0.75*shift_freq/10, shift_freq/10, osc_freq/4), linewidth=2)  # Haz reflejado (vertical) 

    # Hazes adicionales
    ax1.plot([7, 10], [0.05, 0.05], color=(1-0.75*shift_freq/10, shift_freq/10, osc_freq/4), linewidth=2)  # Haz hacia el objeto oscilante
    ax1.plot([7, 8], [2.95, 2.95], color=(1-0.75*shift_freq/10, shift_freq/10, osc_freq/4), linewidth=2)  # Haz hacia el fotodetector

    ax1.set_xlim(-3, 11)
    ax1.set_ylim(-1, 4.5)
    ax1.set_aspect('equal', 'box')
    ax1.axis('off')
    ax1.set_title('Laser Doppler Vibrometer')

    # Generar y graficar la señal del fotodetector
    t = np.linspace(0, 1, 5000)
    signal = generate_signal(shift_freq, osc_freq, t)
    ax2.plot(t, signal, color='b')
    ax2.set_title('Señal en el Fotodetector')
    ax2.set_ylabel('Amplitud')
    ax2.set_xlim(0, 1)

    # Generar y graficar el espectrograma de la señal
    f, t_spec, Sxx = spectrogram(signal, fs=5000,nperseg=200, noverlap=100)
    ax3.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
    ax3.set_xlabel('Tiempo [s]')
    ax3.set_ylabel('Frecuencia [Hz]')
    ax3.set_ylim([0,1500])

    canvas.draw()

# Crear la aplicación tkinter
root = tk.Tk()
root.title("Simulación de Vibrometro Laser")

# Crear el contenedor para el gráfico
fig = plt.Figure(figsize=(12, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Crear un marco para los sliders
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

# Crear los sliders
shift_freq_slider = tk.DoubleVar(value=1.0)
osc_freq_slider = tk.DoubleVar(value=1.0)

def on_shift_freq_slider_change(event):
    update_plot(shift_freq_slider.get(), osc_freq_slider.get())

def on_osc_freq_slider_change(event):
    update_plot(shift_freq_slider.get(), osc_freq_slider.get())

shift_freq_label = tk.Label(frame, text="Freq. Red de Bragg")
shift_freq_label.pack(side=tk.LEFT, padx=5)
shift_freq_scale = ttk.Scale(frame, from_=0, to=10.0, orient=tk.HORIZONTAL, variable=shift_freq_slider, command=on_shift_freq_slider_change)
shift_freq_scale.pack(side=tk.LEFT, padx=5)

osc_freq_label = tk.Label(frame, text="Freq. Oscilación Objeto")
osc_freq_label.pack(side=tk.LEFT, padx=5)
osc_freq_scale = ttk.Scale(frame, from_=0, to=4.0, orient=tk.HORIZONTAL, variable=osc_freq_slider, command=on_osc_freq_slider_change)
osc_freq_scale.pack(side=tk.LEFT, padx=5)

# Inicializar el gráfico
update_plot(shift_freq_slider.get(), osc_freq_slider.get())

# Ejecutar la aplicación tkinter
root.mainloop()