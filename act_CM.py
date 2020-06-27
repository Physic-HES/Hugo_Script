import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg as npl

x=[0]
y=[np.random.random(1)-0.5]
c=0
X0 = np.array([[1, x[0], x[0] ** 2]])
Y0 = np.array([np.array(y[0]) * np.ones(3)])
M = np.dot(np.transpose(X0), X0)
V = np.transpose(X0) * np.transpose(Y0)
plt.figure()
while x[-1]<=5:
    c = c+1
    x.append(x[-1]+0.01)
    y.append([2*x[-1]**2+np.random.random(1)-0.5])
    X0 = np.array([[1, x[c], x[c] ** 2]])
    Y0 = np.array([np.array(y[c][0]) * np.ones(3)])
    M1 = np.dot(np.transpose(X0),X0)
    V1 = np.transpose(X0)*np.transpose(Y0)
    M = M + M1
    V = V + V1
    A = np.dot(npl.inv(M),V)
    plt.plot(x, y, '.r')
    q = np.array(x)
    p = A[0]+A[1]*np.array(x)+A[2]*np.array(x)**2
    h, = plt.plot(q, p, '-b')
    ax = plt.gca()
    pos = [0.1*np.max(x),np.max(y)-(0.1*np.max(y))]
    ann = plt.text(pos[0], pos[1], r'$f(x) =$ %2.2f + %2.2f$x$ + %2.2f$x^2$'%(A[0],A[1],A[2]))
    plt.pause(0.05)
    ann.remove()
    ax.lines.remove(h)
    plt.draw()
print(r'a_0=%g, a_1=%g, a_2=%g'%(A[0],A[1],A[2]))
