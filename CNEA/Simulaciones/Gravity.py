import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2

# Constantes
G = 6.67430e-11  # Constante de gravitación universal
n = 10  # Número de partículas
timestep = 1e-3  # Paso de tiempo de la simulación

# Inicialización de las partículas
masas = np.random.rand(n) * 1e21  # Masas aleatorias
posiciones = np.random.rand(n, 2) * 1e11  # Posiciones iniciales aleatorias
velocidades = np.zeros((n, 2))  # Velocidades iniciales

def calcular_fuerzas(posiciones, masas):
    """Calcula las fuerzas gravitacionales entre todas las partículas."""
    fuerzas = np.zeros((n, 2))
    for i in range(n):
        for j in range(i + 1, n):
            distancia = posiciones[j] - posiciones[i]
            distancia_norm = np.linalg.norm(distancia)
            fuerza_magnitud = G * masas[i] * masas[j] / distancia_norm**3
            fuerza = fuerza_magnitud * distancia
            fuerzas[i] += fuerza
            fuerzas[j] -= fuerza
    return fuerzas

def actualizar_sistema(posiciones, velocidades, masas, timestep):
    """Actualiza las posiciones y velocidades de las partículas."""
    fuerzas = calcular_fuerzas(posiciones, masas)
    aceleraciones = fuerzas / masas[:, np.newaxis]
    velocidades += aceleraciones * timestep
    posiciones += velocidades * timestep

cv2.imshow('logo',np.zeros((20,20)))
cv2.destroyAllWindows()
# Preparación de la animación
fig, ax = plt.subplots()
scat = ax.scatter(posiciones[:, 0], posiciones[:, 1])

def animar(frame):
    actualizar_sistema(posiciones, velocidades, masas, timestep)
    scat.set_offsets(posiciones)
    return scat,

ani = FuncAnimation(fig, animar, frames=200, interval=20, blit=True)

plt.show()