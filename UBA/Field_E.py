import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt


def circ(x1, x2, d, r, ro):
    Ex = np.zeros([len(x1[:, 0]), len(x1[0, :])])
    Ey = np.zeros([len(x2[:, 0]), len(x2[0, :])])
    e_0 = 8.8541878176E-12
    for k in np.arange(0, len(x1[0, :])):
        for j in np.arange(0, len(x2[:, 0])):
            D = LA.norm(np.array([x1[k, j], x2[k, j]]) - np.array(d))
            if D < r:
                Ex[k, j] = (ro / (2 * e_0) * (x1[k, j] - d[0]))
                Ey[k, j] = (ro / (2 * e_0) * (x2[k, j] - d[1]))
            if D > r:
                Ex[k, j] = (ro / (2 * e_0) * (x1[k, j] - d[0])) * (r / D)**2
                Ey[k, j] = (ro / (2 * e_0) * (x2[k, j] - d[1])) * (r / D)**2
    return Ex, Ey


def cables_inf(r1, p1, ro1, r2, p2, ro2):
    dif = LA.norm(np.array(np.array(p1)-np.array(p2)))
    L = np.max([r1, r2]) + dif +1
    Space = np.arange(-L, L, 2*L/50)
    X, Y = np.meshgrid(Space, Space)
    Eax, Eay = circ(X, Y, [p1[0], p1[1]], r1, ro1)
    Ebx, Eby = circ(X, Y, [p2[0], p2[1]], r2, ro2)
    fig, ax = plt.subplots()
    q1 = ax.quiver(X, Y, Eax+Ebx, Eay+Eby)
    teta = np.arange(0, 2 * np.pi + np.pi / 100, np.pi / 100)
    p1 = ax.plot(r1 * np.cos(teta) + p1[0], r1 * np.sin(teta) + p1[1], '-r')
    p2 = ax.plot(r2 * np.cos(teta) + p2[0], r2 * np.sin(teta) + p2[1], '-r')
    ax.set_aspect('equal')
    plt.show()


print('Escriba los datos de la 1er distribución en un vector de la siguiente manera: ')
print('[Radio,Posición_x,Posición_y,Densidad_ro]')
D1 = eval(input())
print('Ahora lo mismo pero de la 2da distribución: ')
print('[Radio,Posición_x,Posición_y,Densidad_ro]')
D2 = eval(input())

cables_inf(D1[0], D1[1:3], D1[3], D2[0], D2[1:3], D2[3])

