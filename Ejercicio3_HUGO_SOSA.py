## EJERCICIO 3
## HUGO SOSA
## LU 205/07.

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

# La Parte a) cuenta con 2 graficos, uno para las soluciones con cada N y otro para ver el orden del error global.
# La parte b) cuenta con tres graficos, una para comparar el efecto de actualizar y1
#           y despues y2 o viceversa con la solucion exacta (Yo no vi diferencias, quizas porque use el metodo A,
#           que es explicito en ambas variables. Creo que con cualquiera de los otros dos metodos se deberia
#           notar alguna diferencia), otro grafico es para las soluciones con cada N comparadas con la exacta
#           y la ultima grafica es el error en funcion del tiempo, en este grafico se puede ver que el error global
#           sin modulo respeta el periodo de la solucion exacta con un leve desfazaje para N chicos, sin embargo
#           la emvolvente de el error global es un polinomio de t cuyo orden tiende a 1 para N grandes.
# La Parte c) modifica una funcion para que se pueda escribir un string de y prima como input. Esta misma
#           funcion sirve para cualquier funcion Phy(t,y,h).


## Parte a)
def resuelve_y(y0, t0, T, N):
    y = [y0]
    t = [t0]
    h = (T-t0)/N
    for j in np.arange(0, N):
        y.append(y[j] + h*(-2 * y[j] + t[j]**2))
        t.append(t[j] + h)
    return [t, y]


def F(x):
    return 3/4*np.e**(-2*x)+1/2*(x**2-x+1/2)


Ns = np.array([10, 50, 100, 500, 1000])
Err = []
tp = np.arange(0, 10+1/1000, 1/1000)
plt.plot(tp, eval('F')(tp), label='Solucion exacta')
plt.title(r'Euler para $y\prime=-2y+t^2$ con $y(0)=1$ con distinta cantidad de pasos')
for M in Ns:
    [t, y] = resuelve_y(1, 0, 10, M)
    Err.append(np.abs(eval('F')(10) - y[-1]))
    plt.plot(t, y, label=r'Euler con %g pasos' % M)


plt.legend()
plt.grid()
plt.xlabel('Tiempo')
plt.ylabel('Valor de y')
plt.savefig('graf1_Ej3item_a.png')

plt.draw()
plt.figure(2)
H = 1/Ns
plt.loglog(H, Err, '.r', Label='ErrorG(1/N)')
z = np.polyfit(np.log(H), np.log(Err), 1)
plt.loglog(H, np.exp(z[0]*np.log(H)+z[1]), '-b', label=r'Orden=%g' % z[0])
plt.title(r'El Error Global en función de 1/N es de orden 1, es decir $\|y(10)-y_N|$ es un $O(h)$')
plt.grid()
plt.legend()
plt.xlabel('Valor de 1/N')
plt.ylabel('Error Global')
plt.savefig('graf2_Ej3item_a.png')


## Parte b)
def F2(x):
    return 1/np.sqrt(2)*np.sin(np.sqrt(2)*x)


def resuelve_yA(y1_0, y2_0, t0, T, N, Ord): # ELIJO el metodo A
    y1 = [y1_0]
    y2 = [y2_0]
    t = [t0]
    h = (T-t0)/N
    E_t = [0]
    for j in np.arange(0, N):
        if Ord == 1: # Esto es para probar que pasa cuando se alterna el orden de actualizacion de y1 e y2
            y1.append(y1[j] + h*y2[j])
            y2.append(y2[j] + h*(-2*y1[j])) # Podria escribirse con la matriz de f:=np.matrix([[0,1],[-2,0]])
        if Ord == 0:
            y2.append(y2[j] + h * (-2*y1[j]))
            y1.append(y1[j] + h * y2[j])
        E_t.append(np.abs(eval('F2')(t[j]) - y1[j]))
        t.append(t[j] + h)
    return [t, y1, y2, E_t]


tp = np.arange(0, 10+1/1000, 1/1000)
plt.draw()
plt.figure(3)
plt.plot(tp, eval('F2')(tp), '-b', label='Solucion exacta')
[ta, ya1, ya2, Ea_t] = resuelve_yA(0, 1, 0, 10, 100, 1)
[td, yd1, yd2, Ed_t] = resuelve_yA(0, 1, 0, 10, 100, 0)
plt.plot(ta, ya1, '.g', label=r'Actualizando primero y1')
plt.plot(td, yd1, '-m', label=r'Actualizando primero y2')
plt.title(r'Comparacion al actualizar y1 primero o y2 primero')
plt.legend()
plt.grid()
plt.xlabel('Tiempo')
plt.ylabel('Valor de y')
plt.savefig('graf3_Ej3item_b.png')

plt.draw()
plt.figure(4)
plt.plot(tp, eval('F2')(tp), '-b', label='Solucion exacta')
for M in Ns[1:]: # Omiti N=10, porque el error es tan grande que no me deja ver como se aproximan las demas soluciones
    [t, y1, y2, E_t] = resuelve_yA(0, 1, 0, 10, M, 1)
    plt.plot(t, y1, label=r'Euler con %g pasos' % M)


plt.title(r'Euler para $y\prime\prime=-2y$ con $y(0)=0$ y $y\prime(0)=1$ con distinta cantidad de pasos')
plt.legend()
plt.grid()
plt.xlabel('Tiempo')
plt.ylabel('Valor de y')
plt.savefig('graf4_Ej3item_b.png')

plt.draw()
plt.figure(5)


def func(x, a, b):
    return a*x**b


xf = np.linspace(0, 10, 50)
for M in Ns[1:]:
    [t, y1, y2, E_t] = resuelve_yA(0, 1, 0, 10, M, 1)
    plt.plot(t, E_t, label=r'Error(t) para %g pasos' % M)
    peaks, _ = find_peaks(E_t)
    tp, E_tp = np.transpose(t), np.transpose(E_t)
    plt.plot(tp[peaks], E_tp[peaks], '.k')
    popt, _ = curve_fit(func, tp[peaks], E_tp[peaks])
    plt.plot(xf, func(xf, *popt), '--k', label=r'Envol_fit: $ %2.3f * t^{%2.3f} $' % tuple(popt))


plt.title(r'El Error funcion del tiempo para distinta cantidad de pasos')
plt.grid()
plt.legend()
plt.xlabel('Tiempo')
plt.ylabel('Error Global')
plt.savefig('graf5_Ej3item_b.png')
plt.show()


## Parte c)


def resuelve_y2(yp, y0, t0, T, N):
    # yp: es la derivada primera,
    # y0: es el valor inicial de y,
    # t0: el tiempo inicial,
    # T: el tiempo final,
    # N: el numero de pasos
    ys = [y0]
    ts = [t0]
    h = (T-t0)/N
    for j in np.arange(0, N):
        t = ts[j]
        y = ys[j]
        ys.append(ys[j] + h*eval(yp))
        ts.append(ts[j] + h)
    return [ts, ys]

