## EJERCICIO 7
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as npl
import pandas as pd
from tqdm import tqdm


def matriz_dif(x):
    A = np.zeros((len(x),len(x)))
    A[:,0] = 1
    for q in range(1,len(x)):
        for r in range(1,len(x)):
            A[r,q] = (x[r]-x[q-1])*A[r,q-1]
    return(A)


def jacobi(A,b,x0,max_iter,tol):
    D = np.diag(np.diag(A))
    L = np.tril(A,-1)
    U = np.triu(A,1)
    M = D
    N = U + L
    B = -np.dot(npl.inv(M),N)
    C = npl.inv(M)
    xN = x0
    resto = npl.norm(xN-np.dot(npl.inv(A),b))
    iter = 0
    pbar = tqdm(total=max_iter, desc='Calculando ceof de interpolacion de Newton con Jacobi')
    while resto>tol and iter<=max_iter:
        xN = np.dot(B,xN)+np.dot(C,b)
        iter = iter + 1
        resto = npl.norm(xN-np.dot(npl.inv(A),b))
        if iter == max_iter:
            print('Max_iter reached')
        else:
            pbar.update(1)
        if resto<tol:
            print('Tol reached')
    pbar.close()
    return ([xN, iter, resto])


def newton_dif(x,y,max_iter,tol):
    A = matriz_dif(x)
    b = y
    x0 = np.zeros(len(y))
    coef = jacobi(A,b,x0,max_iter,tol)
    return(coef[0])


def funcion_interpol(x,y,max_iter,tol):
    coef = newton_dif(x,y,max_iter,tol)
    def function(m):
        X = np.ones(len(coef))
        for i in range(1,len(coef)):
            X[i] = (m-x[i-1])*X[i-1]
        return(np.dot(coef,X))
    return(function)


tol=10**-3
max_iter=10**3
x=np.arange(0,np.pi,.1)
y=np.sin(x)
x2=np.arange(0,np.pi,.01)
f1=funcion_interpol(x,y,max_iter,tol)
y2=np.array([f1(xi) for xi in x2])
plt.figure()
plt.grid()
plt.plot(x,y,'-b',label='sin(x)')
plt.plot(x2,y2,'-r',label='Interp Newton')
plt.plot(x,y,'.k',label='Ptos de interp')
plt.legend()


datos = pd.read_csv('data_prob7.csv')
a = np.array(datos['area_acres'])
x3 = np.log2(a)
y3 = np.array(datos['pop_log2'])
x4 = np.log2(np.arange(np.min(a),np.max(a)+(np.max(a)-np.min(a))/100000,(np.max(a)-np.min(a))/100000))
f2=funcion_interpol(x3,y3,max_iter,tol)
y4=np.array([f2(xi) for xi in x4])
plt.figure()
plt.grid()
plt.plot(x4,y4,'-r',label='Interp Newton')
plt.plot(x3,y3,'.k',label=r'Ptos de interp - Pob. Boston')
plt.legend()
plt.xlabel(r'log_2(Area-Boston)')
plt.ylabel(r'Población')
plt.show()
