import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt


def Circ_3p(p1, p2, p3):
    v1 = np.array([p2[0], p2[1]]) - np.array([p1[0], p1[1]])
    v2 = np.array([p3[0], p3[1]]) - np.array([p1[0], p1[1]])
    M = LA.inv(np.array([v1, v2]))
    dnv1 = LA.norm([np.array(p2)])**2 - LA.norm([np.array(p1)])**2
    dnv2 = LA.norm([np.array(p3)])**2 - LA.norm([np.array(p1)])**2
    V = np.array([dnv1, dnv2])
    P = 1/2*np.dot(M,np.transpose([V]))
    r = LA.norm(np.array(p1)-np.transpose(P))
    return [P, r]


print('')
print('### ENCONTRAR CENTRO Y RADIO DE UN CIRCULO A PARTIR DE TRES PUNTOS ###')
print('Introduzca los tres puntos del circulo de la siguiente manera: ')
print('[[p1x,p1y],[p2x,p2y],[p3x,p3y]]')
D2 = eval('np.array('+input()+')')

[P, r] = Circ_3p(D2[0, :], D2[1, :], D2[2, :])
print(r'Circulo de radio %g, centrado en [%g,%g]' % (r, P[0], P[1]))
teta = np.arange(0, 2*np.pi+2*np.pi/100, 2*np.pi/100)
fig, ax = plt.subplots()
ax.grid()
ax.plot(r*np.cos(teta)+P[0], r*np.sin(teta)+P[1], 'r')
ax.plot(D2[:, 0], D2[:, 1], '.b', label='Puntos')
ax.arrow(np.double(P[0]), np.double(P[1]), r*np.cos(np.pi/4), r*np.sin(np.pi/4))
ax.plot(P[0], P[1], '.m', label='Centro')
ax.set_aspect('equal')
plt.show()

