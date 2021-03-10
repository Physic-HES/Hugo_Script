## EJERCICIO 10
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import linalg as npl
import imageio as img
from tqdm import tqdm

# PUNTO A
def funcion_f(x):
    f=(x+2)*(x+1)
    return f

def funcion_fprima(x):
    f=(x+2)+(x+1)
    return f

# PUNTO B
def iterador_newton_rhapson(funcion_g,funcion_gprima,x0,max_iter,tol):
    error = np.min(np.abs([x0+2,x0+1]))
    iter = 0
    while error>tol and iter<=max_iter:
        x1 = x0-funcion_g(x0)/funcion_gprima(x0)
        error = abs((1/funcion_gprima(x0))*error**2)
        iter = iter+1
        x0 = x1
    return([x0,iter-1,error])

x0=1
NR1 = iterador_newton_rhapson(funcion_f,funcion_fprima,x0,1E3,1E-5)
print(r'RAIZ OBTENIDA: %g +- %e [Con %3.0f Iteraciones NR desde x0=%3.2f]'%(NR1[0],NR1[2],NR1[1],x0))
x0=-10
NR2 = iterador_newton_rhapson(funcion_f,funcion_fprima,x0,1E3,1E-5)
print(r'RAIZ OBTENIDA: %g +- %e [Con %3.0f Iteraciones NR desde x0=%3.2f]'%(NR2[0],NR2[2],NR2[1],x0))


# PUNTO C
def iterador_newton_rhapson2(fun_f,fun_fprima,x0,max_iter,tol):
    if fun_fprima=='NO':
        def funcion(x):
            x1 = x*1.001 # Por ejemplo, aproximo usando el 100.1%
            x0 = x*0.999 # y el 99.9% de x
            f1 = fun_f(x1)
            f0 = fun_f(x0)
            f_prima = (f1-f0)/(x1-x0)
            return(f_prima)
    fun_fprima= funcion
    error = np.min(np.abs([x0 + 2, x0 + 1]))
    iter = 0
    while error > tol and iter <= max_iter:
        x1 = x0 - fun_f(x0) / fun_fprima(x0)
        error = np.min(np.abs([x0 + 2, x0 + 1]))
        iter = iter + 1
        x0 = x1
    return ([x0, iter - 1, error])

print('')
x0=1
NR1 = iterador_newton_rhapson2(funcion_f,'NO',x0,1E3,1E-5)
print(r'RAIZ OBTENIDA: %g +- %e [Con %3.0f Iteraciones NR_2 desde x0=%3.2f]'%(NR1[0],NR1[2],NR1[1],x0))
x0=-10
NR2 = iterador_newton_rhapson2(funcion_f,'NO',x0,1E3,1E-5)
print(r'RAIZ OBTENIDA: %g +- %e [Con %3.0f Iteraciones NR_2 desde x0=%3.2f]'%(NR2[0],NR2[2],NR2[1],x0))

# PUNTO D
def iterador_punto_fijo(fun_g,x0,max_iter,tol):
    error = np.min(np.abs([x0 + 2, x0 + 1]))
    iter = 0
    while error > tol and iter <= max_iter:
        x1 = fun_g(x0)
        error = np.min(np.abs([x1 + 2, x1 + 1]))
        iter = iter + 1
        x0 = x1
    return([x0,iter-1,error])

def fun_g1(x):
    f=-2/(x+3)
    return f

def fun_g2(x):
    f=-(x**2+2)/3
    return f

print('')
x0=1
PFg1 = iterador_punto_fijo(fun_g1,x0,1E3,1E-5)
print(r'RAIZ OBTENIDA: %g +- %e [Con %3.0f Iteraciones Punto Fijo con g(x)=-2/(x+3) desde x0=%3.2f]'%(PFg1[0],PFg1[2],PFg1[1],x0))
x0=-0.5 # con fun_g2 solo se puede converger a x=-1 con semillas abs(x0)<1 pues g2' no puede acotarse por 1
PFg2 = iterador_punto_fijo(fun_g2,x0,1E3,1E-5)
print(r'RAIZ OBTENIDA: %g +- %e [Con %3.0f Iteraciones Punto Fijo con g(x)=-(x^2+2)/3 desde x0=%3.2f]'%(PFg2[0],PFg2[2],PFg2[1],x0))

# PUNTO E
x = np.arange(0, 5.5, .5)
y = np.array([0.756, 0.561, 0.407, 0.372, 0.305, 0.24, 0.219, 0.209, 0.21, 0.194, 0.140])

def fun_PF(b,x,y):
    S = (y[1] - 1 / (x[1] + b)) * ((x[0] + b) / (x[1] + b)) ** 2
    for k in np.arange(2, len(x)):
        S = S + (y[k] - 1 / (x[k] + b)) * ((x[0] + b) / (x[k] + b)) ** 2
    f = 1 / (y[0] + S) - x[0]
    return f

def iterador_punto_fijo_(fun_g,x0,max_iter,tol,x,y):
    error = np.min(np.abs([x0 + 2, x0 + 1]))
    iter = 0
    while error > tol and iter <= max_iter:
        x1 = fun_g(x0,x,y)
        error = np.min(np.abs([x1 + 2, x1 + 1]))
        iter = iter + 1
        x0 = x1
    return([x0,iter-1,error])

def fun_NR(b,x,y):
    S = (y[0] - 1 / (x[0] + b)) * (1 / (x[0] + b)) ** 2
    for k in np.arange(1, len(x)):
        S = S + (y[k] - 1 / (x[k] + b)) * (1 / (x[k] + b)) ** 2
    f = S
    return f

def iterador_newton_rhapson2_(fun_f,fun_fprima,x0,max_iter,tol,x,y):
    if fun_fprima=='NO':
        def funcion(u):
            x1 = u*1.001 # Por ejemplo, aproximo usando el 100.1%
            x0 = u*0.999 # y el 99.9% de x
            f1 = fun_f(x1,x,y)
            f0 = fun_f(x0,x,y)
            f_prima = (f1-f0)/(x1-x0)
            return(f_prima)
    fun_fprima= funcion
    error = np.min(np.abs([x0 + 2, x0 + 1]))
    iter = 0
    while error > tol and iter <= max_iter:
        x1 = x0 - fun_f(x0,x,y) / fun_fprima(x0)
        error = np.min(np.abs([x0 + 2, x0 + 1]))
        iter = iter + 1
        x0 = x1
    return ([x0, iter - 1, error])

print('')
x0=1
PF = iterador_punto_fijo_(fun_PF,x0,1E4,1.5,x,y)
print(r'RAIZ OBTENIDA: %g +- %e [Con %5.0f Iteraciones Punto Fijo Ej.20 desde x0=%3.2f]'%(PF[0],PF[2],PF[1],x0))
x0=1
NR = iterador_newton_rhapson2_(fun_NR,'NO',x0,1E4,1.5,x,y)
print(r'RAIZ OBTENIDA: %g +- %e [Con %5.0f Iteraciones Newton-Rhapson Ej.20 desde x0=%3.2f]'%(NR[0],NR[2],NR[1],x0))

plt.figure(1)
plt.plot(x,y,'.',label='Datos')
plt.plot(x,1/(x+PF[0]),label='Ajuste por Punto Fijo')
plt.plot(x,1/(x+NR[0]),label='Ajuste por Newton-Rhapson')
plt.title('Ajustes por Punto Fijo y Newton-Rhapson')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()

# Ambos resultados coinciden, las iteraciones se acumulan muy rapido en torno a la raiz
# y es dificil ajustar la tol para que no corte por max iteracion

# PUNTO F
datos = pd.read_csv('data_prob7.csv')
a = np.array(datos['area_acres'])
X = np.log2(a)
Y = np.array(datos['pop_log2'])
X = (X - np.min(X)) / (np.max(X) - np.min(X))
Y = (Y - np.min(Y)) / (np.max(Y) - np.min(Y))

def fun_NR3(b,x,y):
    S = (y[0] - x[1]**b)*np.log(x[1])*x[1]**b
    for k in np.arange(2, len(x)):
        S = S + (y[k] - x[k]**b)*np.log(x[k])*x[k]**b
    f = S
    return f

x0=1
NR3 = iterador_newton_rhapson2_(fun_NR3,'NO',x0,1E4,1.5,X,Y)
print('')
print(r'RAIZ OBTENIDA: %g +- %e [Con %5.0f Iteraciones Newton-Rhapson Problema 7 desde x0=%3.2f]'%(NR3[0],NR3[2],NR3[1],x0))

plt.figure(2)
plt.plot(X,Y,'.',label='Datos')
plt.plot(X,X**NR3[0],label='Ajuste por Newton-Rhapson')

def matriz_A(x,n,tipo):
    nx = len(x)
    A = np.zeros((nx,n))
    if tipo=='polinomial':
        for i in range(nx):
            for j in range(n):
                A[i][j] = x[i]**j
    elif tipo=='senoidal':
        for i in range(nx):
            for j in range(n):
                A[i][j] = np.sin((j+1)*x[i])
    return(A)

def cuadrados(x,y,n,tipo):
    A = matriz_A(x,n,tipo)
    B = np.dot(np.transpose(A),A)
    c = np.dot(npl.inv(B),np.dot(np.transpose(A),y))
    return(c)

def genera_ajustador(c,tipo):
    if tipo=='polinomial':
        def function(z):
            w = 0
            for j in range(len(c)):
                w += c[j]*z**j
            return(w)
    elif tipo=='senoidal':
        def function(z):
            w = 0
            for j in range(len(c)):
                w += c[j]*np.sin((j+1)*z)
            return(w)
    return(function)

k = 3
n = 2*(k+1)
c_3 = cuadrados(X,Y,n,'polinomial')
f_aj = genera_ajustador(c_3,'polinomial')
x4 = np.arange(np.min(X),np.max(X)+(np.max(X)-np.min(X))/100,(np.max(X)-np.min(X))/100)
Y_aj = np.array([f_aj(xi) for xi in x4])
plt.plot(x4,Y_aj,label=r'Ajuste polinomial n=%1.0f'%n)
plt.xlabel('Area [Acres]')
plt.ylabel('Población')
plt.title('Ajustes por Cuadrados Minimos y Newton-Rhapson')
plt.legend()
plt.show()

