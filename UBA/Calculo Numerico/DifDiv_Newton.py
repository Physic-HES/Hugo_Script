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

def newton_dif(x,y):
    A = matriz_dif(x)
    coef = np.dot(npl.inv(A),y)
    def func(s,coef,x):
        p=(s-x[0])
        f=coef[0]
        for k in np.arange(1,len(coef)):
            f=f+coef[k]*p
            p=p*(s-x[k])
        return(f)
    return([coef,func])

print('POLINOMIO INTERPOLADOR POR METODO DE DIFERENCIAS DIVIDIDAS DE NEWTON')
D=input('Ingrese los datos como [[x0,y0],[x1,y1],...,[xn,yn]]: ')
dat=np.array(eval(D))
C=newton_dif(dat[:,0],dat[:,1])
print('Los coeficientes del polinomio quedan:')
COEF=r'a_0=%3.1f, '%C[0][0]
for k in np.arange(1,len(C[0])-1):
    COEF=COEF+r'a_%1.0f=%3.1f, '%(k,C[0][k])
COEF=COEF+r'a_%1.0f=%3.1f'%(len(C[0]),C[0][-1])
print(COEF)
x=np.arange(np.min(dat[:,0]),np.max(dat[:,0]),0.01)
y=np.array([C[1](xi,C[0],dat[:,0]) for xi in x])
plt.plot(x,y,label='Polinomio de Newton')
plt.plot(dat[:,0],dat[:,1],'.r',label='Polinomio de Newton')
plt.show()