## EJERCICIO 2
## HUGO SOSA
## LU 205/07.

import numpy as np
import matplotlib.pyplot as plt


def primos_hasta(N):
    y = []
    for j in np.arange(1, N + 1):
        if sum(np.mod(j, np.arange(1, N + 1)) == 0) <= 2:
            y.append(j)
    return y


def cuantos_primos(N, L):
    l = L < N
    return sum(l)


# CODIGO DE LA FUNCION
# El valor mas grande hasta el cual voy a buscar primos
N = 10 ** 3
L = primos_hasta(N)
x = np.arange(1, N + 1)
y = []
# En este for, anotamos cuantos primos
# hay para cada valor xi
for xi in x:
    y.append(cuantos_primos(xi, L))

plt.plot(x, y, label='Numeros primos hasta N')
a = 0.12
b = 200
plt.plot(x, a * x + b/20*5, label=r'Lineal ax+b con a=%g y b=%g' % (a, b/20*5))
plt.plot(x, 2*b/100 * np.sqrt(x), label=r'Raiz cuadrada cx$^{1/2}$ con c=%g' % (2*b/100))
plt.plot(x[1:], x[1:] / np.log(x[1:]), label=r'Teorema $\pi(x) \sim x/ln(x)$')
plt.plot(x[1:], np.cumsum(1 / np.log(x[1:])), label=r'Integral logaritmica $\pi(x) \sim Li(x)$')
plt.title(r'$\pi(x)$ - Cantidad de numeros primos menores a cada N')
plt.xlabel('Hasta')
plt.ylabel('Cantidad de primos')
plt.xlim(0, 10**3)
plt.ylim(0, 200)
plt.grid()
plt.legend()
plt.savefig('grafico.png')
plt.show()

# Si bien la funcion lineal graficada acota a los numeros primos menores a 1000,
# esa acotacion deja de valer para algun N>1000 o para N tendiendo a infinito, lo mismo ocurre
# para la funcion raiz cuadrada pero a partir de N ~ 400, la unica que acota bien para
# N grandes es la funcion llamada Logaritmo Integral Li(x).
# NOTA: En general, desconozco bastante de teoria de numeros pero se que esta ultima cota
# esta relacionada con la validez de la hipotesis de Riemann pero no se bien como ni porque.
