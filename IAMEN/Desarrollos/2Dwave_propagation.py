import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cv2

# Parameters
size = 200  # Size of the grid
time_steps = 200  # Number of time steps
c = np.ones((size, int(size*1.5)))*7  # Wave speed
dt = 0.1  # Time step size
dx = 1.0  # Spatial step size

# Initial conditions
u = np.zeros((size, int(size*1.5),3))
source_position = (50, 50)  # Coordinates of the source
wavelength = 8  # Wavelength of the wave
amplitude = 1.5  # Amplitude of the wave

#Coordenadas de construccion
X,Y=np.meshgrid(np.arange(int(1.5*size)),np.arange(size))

# Aperture parameters
aperture_size = 15
aperture_position = (100, 130)
logo=cv2.imread('/home/hp1opticaiamend/Pictures/logo_0.png')
logo=cv2.cvtColor(logo,cv2.COLOR_BGR2GRAY)
logo=cv2.resize(logo, (u[:,:,0].shape[1],u[:,:,0].shape[0]), interpolation =cv2.INTER_AREA)
ind_r=np.where(logo>100)[0]
ind_c=np.where(logo>100)[1]
cv2.imshow('logo',logo)
cv2.destroyAllWindows()

#import prisma
lente=cv2.imread('/home/hp1opticaiamend/Pictures/lente.png')
lente=cv2.cvtColor(lente,cv2.COLOR_BGR2GRAY)
lente=cv2.resize(lente, (u[:,:,0].shape[1],u[:,:,0].shape[0]), interpolation =cv2.INTER_AREA)
ind_r2=np.where(lente>100)[0]
ind_c2=np.where(lente>100)[1]

# Construccion de prisma
pris=np.zeros_like(c)
pris=np.where(Y>1.5*(X-2/5*size*1.5),1,0)+np.where(Y>-1.5*(X-3/5*size*1.5),1,0)+np.where(Y<130,1,0)
pris=np.where(pris==3,1,0)

# LOGO IAMEND pared
#u[ind_r,ind_c,2]=2

# Tuneling con fibra
fibra=np.zeros_like(c)
fibra=np.where(Y>32.98-12*(np.arctan(0.05*(X-50))-np.arctan(0.05*(X-250))),1,0)+np.where(Y<35.98-12*(np.arctan(0.05*(X-52.5))-np.arctan(0.05*(X-247.5))),1,0)
fibra=np.where(fibra==2,1,0)
fibra_=fibra[sorted(np.arange(fibra.shape[0]),reverse=True),:]
fibra=fibra+fibra_
fibra=np.roll(fibra,100,axis=0)

# Function to update the simulation
def update(frame):
    global u, X, Y, c

    # Condicion libre en los extremos de la imagen du=0
    u[0,1:-1,2]=u[1,1:-1,2]
    u[-1,1:-1,2]=u[-2,1:-1,2]
    u[0,0,2]=u[1,1,2]
    u[0,-1,2]=u[1,-2,2]
    u[1:-1,0,2]=u[1:-1,1,2]
    u[1:-1,-1,2]=u[1:-1,-2,2]
    u[-1,0,2]=u[-2,1,2]
    u[-1,-1,2]=u[-2,-2,2]

    # Fuentes puntuales (Laser)
    #u[range(100-2*wavelength//2,100+3*wavelength//2,wavelength//2), 25] = amplitude * np.sin(2 * np.pi * frame / wavelength)
    u[range(60,110,20), 6] = amplitude * np.sin(2 * np.pi * frame / ((1+np.random.random())*wavelength))
    u[140, 6] = amplitude * np.sin(2 * np.pi * frame / ((1+np.random.random())*wavelength))
    # caja
    #u[94,19:55]=0
    #u[106,19:55]=0
    #u[94:106,19]=0

    # Onda plana
    #u[:,1]=amplitude * np.sin(2 * np.pi * frame / wavelength)

    # lente semi esferica
    l=np.zeros_like(c)
    l=np.where((X-220)**2+(Y-100)**2<120**2,1,0)+np.where((X-40)**2+(Y-100)**2<120**2,1,0)
    c=np.where(l==2,4.5,7)

    # logo como prisma
    #c[ind_r,ind_c]=2.5

    # Bean Splitter
    #c[range(75,125),range(150,200)]=5

    # Bean Splitter
    #c[75:135,115:175]=5
    #c[range(75,136),range(115,176)]=5
    #c[range(76,136),range(115,175)]=7
    #c[range(75,135),range(116,176)]=7

    # mirror 1
    #u[140:141,115:175]=0

    # mirror 2
    #u[75:135,180:181]=0

    # iteracion
    u[1:-1, 1:-1,2] = -u[1:-1, 1:-1,0]+ 2*u[1:-1, 1:-1,1] + (c[1:-1,1:-1] * (dt / dx))**2 * (u[2:, 1:-1,1] + u[:-2, 1:-1,1] + u[1:-1, 2:,1] + u[1:-1, :-2,1] - 4 * u[1:-1, 1:-1,1])


    # LOGO IAMEND como fuente
    #u[ind_r,ind_c,2]=amplitude * np.sin(2 * np.pi * frame / wavelength)
    
    # LOGO IAMEND pared
    #u[ind_r,ind_c,2]=0

    # Doble rendija
    #u[: aperture_position[0] - 2*aperture_size,
    #  aperture_position[1] - aperture_size//4-20: aperture_position[1] + aperture_size//4-20,2] = 0
    
    #u[aperture_position[0] - aperture_size-9:aperture_position[0] + aperture_size+9,
    #  aperture_position[1] - aperture_size//4-20: aperture_position[1] + aperture_size//4-20,2] = 0
    
    #u[aperture_position[0] + 2*aperture_size:,
    #  aperture_position[1] - aperture_size//4-20: aperture_position[1] + aperture_size//4-20,2] = 0


    
    
UU=np.zeros_like(u[:,:,2])
h=1
# Create animation
fig, ax = plt.subplots(1,2)
def plot_func(frame):
    global UU, h
    update(frame)
    ax[0].clear()
    ax[1].clear()
    imag=np.zeros((size,int(size*1.5),3))
    imag[np.where(u[:,:,2]>0)[0],np.where(u[:,:,2]>0)[1],2]=u[np.where(u[:,:,2]>0)[0],np.where(u[:,:,2]>0)[1],2]
    imag[np.where(u[:,:,2]<0)[0],np.where(u[:,:,2]<0)[1],0]=np.abs(u[np.where(u[:,:,2]<0)[0],np.where(u[:,:,2]<0)[1],2])
    #imag[ind_r,ind_c,0]=imag[ind_r,ind_c,1]=imag[ind_r,ind_c,2]=0.5
    UU=(UU*(h-1)+np.abs(u[:,:,2]))/h
    ax[0].imshow(np.abs(UU), interpolation='bilinear')
    ax[0].set_title('Intensidad')
    ax[1].imshow(imag, interpolation='bilinear')
    ax[1].set_title('Onda')
    u[:, :,0]=u[:, :,1]
    u[:, :,1]=u[:, :,2]
    h+=1
        

ani = FuncAnimation(fig, plot_func, frames=time_steps, interval=2)
plt.show()
plt.imsave('IAMEND_doble_rendija.png',np.abs(UU))






