import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.integrate import odeint as ODE

m=1
g=10
a=2.5
b=1
phi_0=0
phi1_0=0
theta_0=np.pi/3
theta1_0=0
psi_0=0
psi1_0=25
lz=m*(2*b**2+4*a**2)*np.sin(theta_0)**2*phi1_0+4*m*b**2*(psi1_0+np.cos(theta_0)*phi1_0)*np.cos(theta_0)
lr=4*m*b**2*(psi1_0+np.cos(theta_0)*phi1_0)

def f(y,t,m,lz,lr):
    dydt = [y[1],
            (lz-lr*np.cos(y[0]))/(m**2*(2*b**2+4*a**2)**2*np.sin(y[0])**2)*((lz-lr*np.cos(y[0]))/np.tan(y[0])+lr)+4*m*g*a*np.sin(y[0]),
            (lz-lr*np.cos(y[0]))/(m*(2*b**2+4*a**2)*np.sin(y[0])**2),
            lr/(4*m*b**2)-np.cos(y[0])*(lz-lr*np.cos(y[0]))/(m*(2*b**2+4*a**2)*np.sin(y[0])**2)]
    return dydt


y0=[theta_0,theta1_0,phi_0,psi_0]
t=np.linspace(0,2.5,250)

sol=ODE(f,y0,t,args=(m,lz,lr))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in np.arange(len(t)):
    ax.axes.set_xlim3d(left=-2.5, right=2.5)
    ax.axes.set_ylim3d(bottom=-2.5, top=2.5)
    ax.axes.set_zlim3d(bottom=-2.5, top=2.5)
    theta=sol[i,0]
    phi=sol[i,2]
    psi=sol[i,3]
    r_ver=np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
    theta_ver=np.array([np.cos(theta)*np.cos(phi),np.cos(theta)*np.sin(phi),-np.sin(theta)])
    phi_ver=np.array([-np.sin(phi),np.cos(phi),0])
    Bar_a=a*r_ver
    R1=a*r_ver-b*np.cos(psi)*theta_ver-b*np.sin(psi)*phi_ver
    R2=a*r_ver-b*np.cos(psi)*phi_ver+b*np.sin(psi)*theta_ver
    R3=a*r_ver+b*np.cos(psi)*theta_ver+b*np.sin(psi)*phi_ver
    R4=a*r_ver+b*np.cos(psi)*phi_ver-b*np.sin(psi)*theta_ver
    barra1 = ax.plot([0,Bar_a[0]],[0,Bar_a[1]],[0,Bar_a[2]],'-g')
    barra2 = ax.plot([R1[0],R3[0]],[R1[1],R3[1]],[R1[2],R3[2]],'-b')
    barra3 = ax.plot([R2[0],R4[0]],[R2[1],R4[1]],[R2[2],R4[2]],'-b')
    masas = ax.plot([R1[0],R2[0],R3[0],R4[0]],[R1[1],R2[1],R3[1],R4[1]],[R1[2],R2[2],R3[2],R4[2]],'ok')
    plt.pause(t[1])
    plt.cla()
    plt.draw()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.axes.set_xlim3d(left=-2.5, right=2.5)
ax2.axes.set_ylim3d(bottom=-2.5, top=2.5)
ax2.axes.set_zlim3d(bottom=-2.5, top=2.5)
theta=sol[0,0]
phi=sol[0,2]
psi=sol[0,3]
r_ver=np.array([np.sin(theta)*np.cos(phi),np.sin(theta)*np.sin(phi),np.cos(theta)])
theta_ver=np.array([np.cos(theta)*np.cos(phi),np.cos(theta)*np.sin(phi),-np.sin(theta)])
phi_ver=np.array([-np.sin(phi),np.cos(phi),0])
Bar_a=a*r_ver
R1=a*r_ver-b*np.cos(psi)*theta_ver-b*np.sin(psi)*phi_ver
R2=a*r_ver-b*np.cos(psi)*phi_ver+b*np.sin(psi)*theta_ver
R3=a*r_ver+b*np.cos(psi)*theta_ver+b*np.sin(psi)*phi_ver
R4=a*r_ver+b*np.cos(psi)*phi_ver-b*np.sin(psi)*theta_ver
barra1_ = ax2.plot([0,Bar_a[0]],[0,Bar_a[1]],[0,Bar_a[2]],'-g')
barra2_ = ax2.plot([R1[0],R3[0]],[R1[1],R3[1]],[R1[2],R3[2]],'-b')
barra3_ = ax2.plot([R2[0],R4[0]],[R2[1],R4[1]],[R2[2],R4[2]],'-b')
masas_ = ax2.plot([R1[0],R2[0],R3[0],R4[0]],[R1[1],R2[1],R3[1],R4[1]],[R1[2],R2[2],R3[2],R4[2]],'ok')

