import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
plt.ion()

tam=125
#x,y=np.meshgrid(np.linspace(0,tam-1,tam),np.linspace(0,tam-1,tam))
#L=10+(70-10)*np.random.random_sample((80,))
#theta=np.pi*np.random.random_sample((80,))
#z=np.zeros_like(x)
#for j in range(len(L)):
#    x_,y_=np.cos(theta[j])*x+np.sin(theta[j])*y,-np.sin(theta[j])*x+np.cos(theta[j])*y
#    z+=(np.cos(2*np.pi/L[j]*x_+2*np.pi*np.random.rand())**2+np.sin(2*np.pi/L[j]*y_+2*np.pi*np.random.rand())**2)

#Componentes de la normal
#d_x=z[:-1,1:]-z[:-1,:-1] # Derivada en X
#d_y=z[1:,:-1]-z[:-1,:-1] # Derivada en Y
#d_z=-np.ones_like(d_x) # Componente Z

#Redimensionamiento
#x=x[:-1,:-1]
#y=y[:-1,:-1]
#z=z[:-1,:-1]

#Guardado
#np.savetxt('x.txt',x)
#np.savetxt('y.txt',y)
#np.savetxt('z.txt',z)
#np.savetxt('d_x.txt',d_x)
#np.savetxt('d_y.txt',d_y)
#np.savetxt('d_z.txt',d_z)

#Importacion
x=np.loadtxt('x.txt')
y=np.loadtxt('y.txt')
z=np.loadtxt('z.txt')
d_x=np.loadtxt('d_x.txt')
d_y=np.loadtxt('d_y.txt')
d_z=np.loadtxt('d_z.txt')

#Normalizacion
n=np.zeros((d_x.shape[0],d_x.shape[1],3))
n[:,:,0]=-d_x
n[:,:,1]=-d_y
n[:,:,2]=-d_z
norm=np.zeros_like(n)
for k in range(3):
    norm[:,:,k]=np.sqrt(n[:,:,0]**2+n[:,:,1]**2+n[:,:,2]**2)
n=n/norm

#Direccion incidente
I_0=np.zeros((1,1,3))
I_0[0,0,0]=.5
I_0[0,0,1]=-.5
I_0[0,0,2]=-.5
I_0=np.tile(I_0,(tam-1,tam-1,1))

#Vector de onda k
prod_scal=np.zeros_like(I_0)
for h in range(3):
    prod_scal[:,:,h]=np.sum(I_0*n,axis=2)
k=I_0-2*prod_scal*n

#Posiciones r
ri=np.zeros((tam-1,tam-1,3))
ri[:,:,0]=x
ri[:,:,1]=y
ri[:,:,2]=z

r=np.zeros_like(ri)
r[:,:,0]=x
r[:,:,1]=y


#Direccion de decaimiento en intensidad
#m=np.zeros_like(r)
#m[:,:,0]=np.sum((r-np.tile(ri[0,0,:],(tam-1,tam-1,1)))*n,axis=2)*n[:,:,0]
#m[:,:,1]=np.sum((r-np.tile(ri[0,0,:],(tam-1,tam-1,1)))*n,axis=2)*n[:,:,1]
#m[:,:,2]=np.sum((r-np.tile(ri[0,0,:],(tam-1,tam-1,1)))*n,axis=2)*n[:,:,2]
#Funcion de amplitud gamma
#gamma=1*np.exp2(-np.sum(((r-np.tile(ri[0,0,:],(tam-1,tam-1,1)))-m)**2,axis=2)/(2*(90)**2))

#Generacion de speckle
Gamma=1j*np.zeros_like(x)
for nn in range(20):
    r[:,:,2]=(nn+10)*np.ones_like(x) # Distancia de speckle objetivo
    pbar = tqdm(total=(tam-1)**2, desc='Agregando fuentes...')
    for g in range(x.shape[1]):
        for s in range(x.shape[0]):
            #m[:,:,0]=np.sum((r-np.tile(ri[s,g,:],(999,999,1)))*n,axis=2)*n[:,:,0]
            #m[:,:,1]=np.sum((r-np.tile(ri[s,g,:],(999,999,1)))*n,axis=2)*n[:,:,1]
            #m[:,:,2]=np.sum((r-np.tile(ri[s,g,:],(999,999,1)))*n,axis=2)*n[:,:,2]
            #gamma=5*np.exp2(-np.sum(((r-np.tile(ri[s,g,:],(999,999,1)))-m)**2,axis=2)/(2*(90)**2))
            Gamma+=1*np.exp2(1j*2*np.pi/5*(np.sum(k[s,g,:]*(r-np.tile(ri[s,g,:],(tam-1,tam-1,1))),axis=2)))
            pbar.update(1)
    np.savetxt(f'Gamma_{nn+10}.txt',np.abs(Gamma)**2)


