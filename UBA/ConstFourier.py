import numpy as np
import matplotlib.pyplot as plt

print('')
print('### Serie de Fourier a partir de a0, an, bn, el semintervalo y n ###')
print('Introduzca los parametros de la siguiente manera: ')
print('[a0,sI,N,n0]')
D0 = eval(input())
print('Introduzca ahora los siguientes coeficientes: ')
Da = input('an: ')
Db = input('bn: ')

x=np.arange(-2*np.array(D0[1]),2*np.array(D0[1]),0.01)
y1=np.array(D0[0])
for n in np.arange(np.array(D0[3]),np.array(D0[2])):
    y1=y1+eval(Da)*np.cos(n*np.pi/np.array(D0[1])*x)+eval(Db)*np.sin(n*np.pi/np.array(D0[1])*x)
plt.plot(x,y1)
plt.show()
