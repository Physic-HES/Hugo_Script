## GUIA DE EJERCICIOS
## HUGO SOSA
## LU 205/07.
import numpy as np
## EJERCICIO 5.a)
k=0
x=[]
while np.sqrt(k)<10:
    h=np.sqrt(k)
    if h-np.floor(h)==0:
        x.append(k)
    k = k + 1
print('Numeros cuyas raices son enteras y menores a 10: ')
print(x)
## EJERCICIO 5.b)
k=3
x=[1,2]
while k<100:
    h=k / np.arange(2, k+1, 1)
    G = list(h - np.floor(h))
    if G.count(0)==1:
        x.append(k)
    k = k + 1
print('Primeros numeros primos menores a 100: ')
print(x)