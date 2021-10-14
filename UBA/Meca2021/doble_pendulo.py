#from matplotlib import rc
#rc('animation', html='jshtml')
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint as ODE
import matplotlib.animation as animation

m1=1.5
m2=1.5
g=10
l1=1.5
l2=1.5
theta1_0=-np.pi/3
theta1p_0=0
theta2_0=-np.pi/12
theta2p_0=0

def f(y,t,m1,m2,l1,l2):
    dydt = [y[2],
            y[3],
            m2/m1*(np.tan(y[1]-y[0])*(y[2]**2+l2/l1*y[3]/np.cos(y[1]-y[0]))+g/l1*(np.sin(y[1])/np.cos(y[1]-y[0])-(m1+m2)/m2*np.sin(y[0]))),
            -(m1+m2)/m1*(l1/l2*y[2]**2*np.sin(y[1]-y[0])+g/l2*(np.sin(y[1])-np.sin(y[0])*np.cos(y[1]-y[0])))-m2/m1*y[3]**2*np.tan(y[1]-y[0])]
    return dydt


y0=[theta1_0,theta2_0,theta1p_0,theta2p_0]
t=np.linspace(0,8,300)

sol=ODE(f,y0,t,args=(m1,m2,l1,l2))

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
def frame(w):
    ax.clear()
    plt.xlim(left=-3.3, right=3.3)
    plt.ylim(bottom=-5.3, top=1.3)
    theta1=sol[w,0]
    theta2=sol[w,1]
    r1=l1*np.array([np.sin(theta1),-np.cos(theta1)])
    r2=r1+l2*np.array([np.sin(theta2),-np.cos(theta2)])
    barra1 = ax.plot([0,r1[0]],[0,r1[1]],'-b')
    barra2 = ax.plot([r1[0],r2[0]],[r1[1],r2[1]],'-b')
    masas = ax.plot([r1[0],r2[0]],[r1[1],r2[1]],'ok')
    return barra1, barra2, masas


anim = animation.FuncAnimation(fig, frame, frames=300, blit=False, repeat=True)
anim.save('two_pendul.gif', writer='imagemagick', fps=60)
