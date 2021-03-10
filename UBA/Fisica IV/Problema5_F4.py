import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

#punto d):
plt.figure()
f_n=[]
L=2
x=np.linspace(0,L,1000)
for n in range(10):
    f_n.append(np.sqrt(2/L)*np.sin((2*n+1)*np.pi/(2*L)*x))
    plt.plot(x,f_n[n],label=r'n=%g'%n)
plt.xticks([0,L],['0','L'])
plt.yticks([])
plt.legend()

#punto f):
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
L=2
a=1
F_n=[]
C_n=[]
CI=np.zeros(1000)
Max_n=[]
x=np.linspace(0,L,1000)
N=10
for n in np.arange(0,N):
    C_n.append(a*np.sqrt(2/L)*2*L/((2*n+1)*np.pi)*(np.cos((2*n+1)*np.pi/8)-np.cos((2*n+1)*np.pi/2)))
    F_n.append(np.sqrt(2/L)*np.sin((2*n+1)*np.pi/(2*L)*x))
    CI+=C_n[n]*F_n[n]
    if n<9:
        Max_n=Max_n+[C_n[n]]+list(np.zeros(99))
    if n==9:
        Max_n = Max_n + [C_n[n]]
suma, =plt.plot(x,N*np.ones(len(x)),zs=CI,label=r'Suma $\sum_{n=0}^{9} C_nF_n(x)$', color='k')
contr, =plt.plot(0*np.ones(len(Max_n)),np.linspace(0,N-1,len(Max_n)),zs=np.array(Max_n),label='Contribución', color='m')
for j in -np.sort(-np.arange(0,N)):
    plt.plot(x,j*np.ones(len(x)),zs=C_n[j]*F_n[j],label=r'Modo n=%g'%j)
plt.xticks([0,L/4,L],['0','L/4','L'])
plt.yticks(range(10),['0','1','2','3','4','5','6','7','8','9'])
plt.xlabel('X')
plt.ylabel('Modos')
plt.xlim([0,L])
plt.ylim([0,10])
ax.set_zlabel(r'$\psi(x,0)$')
ax.set_zticks([])
ax.set_zticks([0,0.2,0.4,0.6,0.8,1])
ax.set_zticklabels(['0',' ',' ',' ',' ','a'])
plt.legend([suma,contr],[r'$\psi(x,0)\approx\sum_{n=0}^{9} C_nF_n(x)$','Contribución modal'])
plt.show()

#punto h):
def cuerda(t):
    L = 2
    a = 1
    c = 1
    x = np.linspace(0, L, 1000)
    F_n = []
    C_n = []
    N = 50
    Psi = np.zeros(len(x))
    for n in np.arange(0,N):
        C_n.append(a*np.sqrt(2/L)*2*L/((2*n+1)*np.pi)*(np.cos((2*n+1)*np.pi/8)-np.cos((2*n+1)*np.pi/2)))
        F_n.append(np.sqrt(2/L)*np.sin((2*n+1)*np.pi/(2*L)*x))
        Psi+=C_n[n]*F_n[n]*np.cos(c*(2*n+1)*np.pi/(2*L)*t)
    return Psi
fig, ax=plt.subplots()
plt.ylim([-1.25,1.25])
ims=[]
for t in np.linspace(0,8.025,100):
    h, =ax.plot(x,cuerda(t),'-b',label=r'$\psi(x,t)$')
    plt.xticks([0,L/4,L],['0','L/4','L'])
    plt.yticks([-1, 0, 1], ['-a', '0', 'a'])
    plt.xlabel('X')
    plt.ylabel(r'$\psi$')
    title=ax.text(L/4,1.05,r'Evolución temporal $\psi(x,$%1.2f$)$'%t,
                    size=plt.rcParams["axes.titlesize"],
                    ha="center", transform=ax.transAxes, )
    ims.append([h,title])

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True)
writer = PillowWriter(fps=60)
ani.save("Cuerda.gif", writer=writer)
