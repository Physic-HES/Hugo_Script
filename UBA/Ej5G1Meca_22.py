import matplotlib.pyplot as plt
import numpy as np

#Coef
m=1
L=1
g=9.865

#CI
r=0.3
r_dot=0
theta=0
theta_dot=0.7
phi=0
phi_dot=0.005
Phi=np.pi/6
Phi_dot=0

#conserv
P_phi=m*(L-r)**2*phi_dot*np.sin(Phi)**2
P_theta=m*r**2*theta_dot

#param
it=500
dt=0.009

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(it):
    ax.axes.set_xlim3d(left=-.5, right=.5)
    ax.axes.set_ylim3d(bottom=-.5, top=.5)
    ax.axes.set_zlim3d(bottom=-.5, top=.5)
    p_m1=[r*np.cos(theta),r*np.sin(theta),0]
    p_m2=[(L-r)*np.sin(Phi)*np.cos(phi),(L-r)*np.sin(Phi)*np.sin(phi),-(L-r)*np.cos(Phi)]
    masas=ax.plot([p_m1[0],p_m2[0]],[p_m1[1],p_m2[1]],[p_m1[2],p_m2[2]],'ok')
    hilo2 = ax.plot([0, p_m2[0]], [0, p_m2[1]], [0, p_m2[2]], '-b')
    hilo1=ax.plot([0,p_m1[0]],[0,p_m1[1]],[0,p_m1[2]],'-g')
    r+=r_dot*dt
    r_dot+=(P_theta**2/(2*m**2*r**3)-P_phi**2/(2*m**2*(L-r)**3*np.sin(Phi))-0.5*(L-r)*Phi_dot**2-0.5*g*np.cos(Phi))*dt
    theta+=P_theta/(m*r**2)
    phi+=P_phi/(m*(L-r)**2*np.sin(Phi)**2)
    Phi+=Phi_dot*dt
    Phi_dot+=(P_phi**2*np.cos(Phi)/(m**2*(L-r)**4*np.sin(Phi)**3)-g/(L-r)*np.sin(Phi))*dt
    plt.pause(dt)
    plt.cla()
    plt.draw()

