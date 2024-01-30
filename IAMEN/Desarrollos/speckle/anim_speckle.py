import numpy as np
import matplotlib.pyplot as plt
#plt.ion()

#for u in range(10,30):
#    Gamma=np.loadtxt(f'Gamma_{u}.txt')
#    plt.imshow(Gamma)
#    plt.pause(0.1)


tam=125
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


Gamma_10=np.loadtxt(f'Gamma_10.txt')
Gamma_11=np.loadtxt(f'Gamma_19.txt')

fft_Gamma_10=np.fft.fftshift(np.fft.fft2(Gamma_10))
fft_Gamma_10_=np.zeros_like(fft_Gamma_10)
fft_Gamma_10_[:,int(fft_Gamma_10.shape[1]/2):]=fft_Gamma_10[:,int(fft_Gamma_10.shape[1]/2):]
Gamma_10_angle=np.arctan2(np.imag(np.fft.ifft2(np.fft.fftshift(fft_Gamma_10_))),
                          np.real(np.fft.ifft2(np.fft.fftshift(fft_Gamma_10_))))
fft_Gamma_11=np.fft.fftshift(np.fft.fft2(Gamma_11))
fft_Gamma_11_=np.zeros_like(fft_Gamma_11)
fft_Gamma_11_[:,int(fft_Gamma_11.shape[1]/2):]=fft_Gamma_11[:,int(fft_Gamma_11.shape[1]/2):]
Gamma_11_angle=np.arctan2(np.imag(np.fft.ifft2(np.fft.fftshift(fft_Gamma_11_))),
                          np.real(np.fft.ifft2(np.fft.fftshift(fft_Gamma_11_))))



plt.imshow(Gamma_11-Gamma_10)
plt.figure()
plt.imshow(k[:,:,2])
plt.show()