## EJERCICIO 9
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as npl
import pandas as pd
from tqdm import tqdm

## PUNTO A
X=np.arange(0,np.pi,np.pi/10)
Y=np.sin(X)

## PUNTO B
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


n, x = 3, np.array([0,2])
print('')
print('Punto B: ')
print(matriz_A(x,n,'polinomial'))
print(matriz_A(x,n,'senoidal'))

## PUNTO C
def cuadrados(x,y,n,tipo):
    A = matriz_A(x,n,tipo)
    B = np.dot(np.transpose(A),A)
    c = np.dot(npl.inv(B),np.dot(np.transpose(A),y))
    return(c)


x = np.array([0,1,2])
y = np.array([0,1,4])
n = 3
tipo = 'polinomial'
print('')
print('Punto C: ')
print(cuadrados(x,y,n,tipo))
print('el resultado coincide con los coef. de una cuadratica y=x² pues los datos siguen ese patron')

## PUNTO D
n = 3
tipo1 = 'polinomial'
tipo2 = 'senoidal'
c_1=cuadrados(X,Y,n,tipo1)
c_2=cuadrados(X,Y,n,tipo2)
print('')
print('Punto D: ')
print(c_1)
print(c_2)
print('la curva puede ajustarse bien a y=-a(x-pi/2)²+1 (coef: [0,a*pi,-a]) o a y=sin(x) (coef: [1,0,0])')

## PUNTO E
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


Xe=np.arange(0,np.pi,np.pi/50)
Ye=np.sin(Xe)
f_aj1=genera_ajustador(c_1,tipo1)
f_aj2=genera_ajustador(c_2,tipo2)
Ye_aj1=np.array([f_aj1(xi) for xi in Xe])
Ye_aj2=np.array([f_aj2(xi) for xi in Xe])
plt.figure(1, figsize=(9, 6))
plt.plot(Xe,Ye,'.k',label='Datos')
plt.plot(Xe,Ye_aj1,'-b',label='Ajuste Polinomial')
plt.plot(Xe,Ye_aj2,'-r',label='Ajuste Senoidal')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Ajuste polinomial y senoidal de la función $y=\sin (x)$')
plt.legend()

## PUNTO F
datos = pd.read_csv('data_prob7.csv')
a = np.array(datos['area_acres'])
x3 = np.log2(a)
y3 = np.array(datos['pop_log2'])
x4 = np.log2(np.arange(np.min(a),np.max(a)+(np.max(a)-np.min(a))/100000,(np.max(a)-np.min(a))/100000))
plt.figure(2, figsize=(9, 6))
plt.subplot(211)
plt.plot(x3,y3,'.k',label='Datos')
for k in range(4):
    n = 2*(k+1)
    c_3 = cuadrados(x3,y3,n,tipo1)
    f_aj = genera_ajustador(c_3, tipo1)
    Y_aj = np.array([f_aj(xi) for xi in x4])
    plt.plot(x4,Y_aj,label=r'Ajuste polinomial n=%1.0f'%n)
plt.xlabel('Area [Acres]')
plt.ylabel('Población')
plt.title('Ajuste polinomial de población por cuadrados minimos para distinta cantidad de coef.')
plt.legend()
# el que mejor se ajusta a los datos es n=8

## PUNTO G
def calcula_error(X,Y,ajustador):
    Y_ajustador = np.array([ajustador(xi) for xi in X])
    error = npl.norm(Y-Y_ajustador)
    return(error)

n=[]
error=[]
cont=0
for k in range(4):
    n.append(2*(k+1))
    c_f = cuadrados(x3,y3,n[cont],tipo1)
    f_aj = genera_ajustador(c_f, tipo1)
    error.append(calcula_error(x3,y3,f_aj))
    cont=cont+1

## PUNTO H
def error_calidad_modelo(X,Y,n,tipo):
    error_valores = []
    for i in range(len(X)-2):
        X_noi = X[0:-(i+1)]
        Y_noi = Y[0:-(i+1)]
        c = cuadrados(X_noi,Y_noi,n,tipo)
        ajustador = genera_ajustador(c,tipo)
        error = np.abs(Y[-(i+1)]-ajustador(X[-(i+1)]))
        error_valores.append(error)
        error_medio = np.mean(error_valores)
    return(error_medio)

plt.subplot(212)
n=[]
error2=[]
cont=0
for k in range(4):
    n.append(2*(k+1))
    c_f = cuadrados(x3,y3,n[cont],tipo1)
    f_aj = genera_ajustador(c_f, tipo1)
    error2.append(error_calidad_modelo(x3,y3,n[cont],tipo1))
    cont=cont+1
plt.plot(n,error,label='Error de ajuste')
plt.plot(n,error2,label='Error medio de predicción')
plt.yscale('log')
plt.xlabel('Cantidad de Coef de ajuste [n]')
plt.ylabel('Error de ajuste en Población')
plt.title('Comparación entre el Error de ajuste a los datos existentes y el Error predictivo de nuevos datos')
plt.legend()
plt.tight_layout()
plt.show()
