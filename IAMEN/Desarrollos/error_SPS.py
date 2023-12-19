import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

W,H=1248,960
x=np.arange(W)
s2,a2=np.meshgrid(np.linspace(5,250,200),np.linspace(H/60,H/2,200))
s=150
a=H/5
Phi=1*np.exp(-1/(2*a**2)*((x-W/2)**2))
Phi_=1*np.exp(-1/(2*a**2)*((x-W/2+s)**2))
SPS=(Phi_-Phi)

plt.plot(x,Phi,label='def')
plt.plot(x,Phi_,label='def_s')
plt.plot(x,SPS,label='pseudo deriv')
plt.plot(x,np.roll(np.cumsum(SPS)/s,1),label='SPS integral')
plt.legend()

plt.figure()
plt.plot(x,Phi,label='def')
plt.plot(x,np.roll(np.cumsum(SPS)/s,int(1+s/2)),label='SPS int_corregida')
plt.plot(x,Phi-np.roll(np.cumsum(SPS)/s,int(1+s/2)),label='SPS error')
plt.legend()

plt.figure()
plt.grid()
plt.plot(x,Phi,label=f'Deformación con $\sigma$={a} px')
s=100
for j in range(5):
    Phi=1*np.exp(-1/(2*a**2)*((x-W/2)**2))
    Phi_=1*np.exp(-1/(2*a**2)*((x-W/2+s)**2))
    SPS=(Phi_-Phi)
    plt.plot(x,np.roll(np.cumsum(SPS)/s,int(1+s/2)),'--',label=f'Reconst. SPS con s={s} px')
    s+=25
plt.xlabel('Ancho de la imagen [px]')
plt.ylabel(r'Deformación [$\mu m$]')
plt.legend()

plt.figure()
plt.grid()
a=200
for j in range(3):
    Phi=1*np.exp(-1/(2*a**2)*((x-W/2)**2))
    Phi_=1*np.exp(-1/(2*a**2)*((x-W/2+s)**2))
    SPS=(Phi_-Phi)
    plt.plot(x, Phi, label=f'Deformación con s={s} px y $\sigma$={a} px')
    plt.plot(x,np.roll(np.cumsum(SPS)/s,int(1+s/2)),'--',label=f'Reconst. SPS con s={s} px y $\sigma$={a} px')
    a+=25
plt.xlabel('Ancho de la imagen [px]')
plt.ylabel(r'Deformación [$\mu m$]')
plt.legend()

Z=np.zeros((200,200))
for k in range(200):
    for j in range(200):
        Phi2 = np.exp(-1 / (2 * a2[k,j] ** 2) * ((x - W / 2) ** 2))
        Phi2_ = np.exp(-1 / (2 * a2[k,j] ** 2) * ((x - W / 2 + s2[k,j]) ** 2))
        SPS2 = (Phi2_ - Phi2)
        Z[k,j]=np.max(Phi2-np.roll(np.cumsum(SPS2)/s2[k,j],int(1+s2[k,j]/2)))

fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
surf3 = ax2.plot_surface(s2, a2, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax2.set_xlabel('Shear [px]')
ax2.set_ylabel(r'$\sigma$ [px]')
ax2.set_zlabel(r'Error [$\mu m$]')

plt.show()
