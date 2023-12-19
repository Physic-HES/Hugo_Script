import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
from tqdm import tqdm
from scipy import integrate as integ
import scipy.ndimage


def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def normalize(arr, t_min, t_max):
    diff = t_max - t_min
    diff_arr = np.max(np.max(arr)) - np.min(np.min(arr))
    temp = (((arr - np.min(np.min(arr)))*diff)/diff_arr) + t_min
    return temp

tam_col,tam_raw=752,480
X,Y=np.meshgrid(range(tam_col),range(tam_raw))
f_corr=3E2 #factor de correccion
shift_obj=0.013E6
D=0.477E6
lamb=0.638
mu=6
alpha=np.arctan(shift_obj/D)
print(alpha)
print(f'periodo espacial k = {1/(np.sin(alpha)/lamb*mu)}')
f=np.sin(alpha)/lamb*mu
print(f'f={f}')
Ap=1.44/(np.sin(alpha)/lamb)*mu
print(f'pixel de la portadora tam_col/2+1/k*tam_col: {tam_col/2+f*tam_col}')
print(f'pixeles de apertura de la lente pupila: {Ap}')
print(f'Corrimiento en pantalla (Shear): {int(alpha*tam_col)}')


c=100
c2=c/3

# SIMULACION DE SPECKLE
#By Goodman (No tarda)
def speckle_G(Im,tam_g,alpha,phi):
    c=100/tam_g
    tam_col, tam_raw = len(Im[0,:]), len(Im[:,0])
    ph_rand=1j*2 * np.pi * np.random.random((tam_raw,tam_col))
    rand_field=np.exp(ph_rand)
    X, Y = np.meshgrid(range(tam_col), range(tam_raw))
    gauss_0 = np.exp(-1 / (2 * (1.5*200) ** 2) * ((X - tam_col / 2) ** 2 + (Y - tam_raw / 2) ** 2))
    gauss_2 = np.exp(-1 / (2 * c ** 2) * ((X - tam_col / 2) ** 2 + (Y - tam_raw / 2) ** 2))
    bandpass = gauss_2
    scatter_field=np.fft.fft2(rand_field)
    gauss_lens=bandpass*scatter_field
    imagefield=np.fft.ifft2(gauss_lens)
    phi_diff=cv2.Scharr(phi, cv2.CV_64F, 1, 0)
    imagefield2=np.fft.ifft2(gauss_lens)
    imagefield3=np.zeros_like(imagefield2)
    imagefield3[:,:int(alpha*tam_col/20)]=imagefield2[:,-int(alpha*tam_col/20):]
    imagefield3[:,int(alpha* tam_col/20):] = imagefield2[:,:-int(alpha * tam_col/20)]
    imagefield3=imagefield3*np.exp(1j*2*np.pi*f*X)
    IMs=np.abs(imagefield+imagefield3)**2
    IMd=np.abs((imagefield+imagefield3*np.exp(1j*4*np.pi/lamb*phi_diff*alpha*tam_col/20)))**2
    return IMs,IMd



#Fase de la deformacion
amp=5 #amplitud de la deformacion en micrones
DEF=amp*np.exp(-1/(2*c**2)*((X-tam_col/2)**2+(Y-tam_raw/2)**2))

#generacion de speckle
#Imagenes con y sin carga
Im_0,Im_1=speckle_G(X,2,alpha,DEF)


cv2.imshow('prueba',Im_1)
cv2.destroyWindow('prueba')
time.sleep(0.001)

plt.figure()
plt.imshow(cv2.Scharr(DEF, cv2.CV_64F, 1, 0))
print(np.max(np.max(DEF)))
plt.figure()
plt.imshow(np.log2(Im_0+1),cmap='gray') #imagen sin carga
plt.figure()
plt.imshow(np.log2(Im_1+1),cmap='gray') #imagen con carga

# construccion de la ventana sobre la portadora
gauss=np.exp(-1/2*(((X-(tam_col/2+f*tam_col+4))/(1.5*c2))**2+((Y-tam_raw/2)/c2)**2))
gauss=np.where(((X-(tam_col/2+f*tam_col+4))/(1.5*(c2*2)))**2+((Y-tam_raw/2)/(c2*2))**2<1,gauss,0)

plt.figure()
plt.imshow(normalize(np.abs(Im_1-Im_0),0,1),cmap='gray') #imagen resta
fftIm_0=np.abs(np.fft.fftshift(np.fft.fft2(Im_0))) #fft de la imagen de referencia
plt.figure()
plt.imshow(np.log2(fftIm_0+1),vmax=np.max(np.max(np.log2(fftIm_0+1)))/np.sqrt(2)) #ploteo logaritmico de la fft de la imagen de referencia
plt.imshow(gauss,cmap='hot',alpha=.2)
fftIm_1=np.abs(np.fft.fftshift(np.fft.fft2(Im_1))) #fft de la imagen con carga
plt.figure()
plt.imshow(np.log2(fftIm_1+1),vmax=np.max(np.max(np.log2(fftIm_1+1)))/np.sqrt(2)) #ploteo logaritmico de la fft de la imagen con carga
plt.imshow(gauss,cmap='hot',alpha=.2)



#filtrado y obtencion de la fase envuelta
Im_0_filt=np.fft.ifft2(np.fft.fftshift(gauss*np.fft.fftshift(np.fft.fft2(Im_0))))
phase_0_filt=np.arctan2(np.imag(Im_0_filt),np.real(Im_0_filt))
Im_1_filt=np.fft.ifft2(np.fft.fftshift(gauss*np.fft.fftshift(np.fft.fft2(Im_1))))
phase_1_filt=np.arctan2(np.imag(Im_1_filt),np.real(Im_1_filt))
diff_fase_filt=phase_1_filt-phase_0_filt
fase_envu=(diff_fase_filt+np.pi)%(2*np.pi)

#plot de la fase envuelta
plt.figure()
plt.imshow(fase_envu,cmap='gray')

#filtro para fase envuelta
w=1/105*np.ones((7,7))
it=0
itera=80
pbar = tqdm(total=itera, desc='Filtrando fase envuelta...')
while it<itera:
    sin_=np.sin(fase_envu)
    cos_=np.cos(fase_envu)
    filsin=scipy.ndimage.convolve(sin_,w,mode='nearest')
    filcos = scipy.ndimage.convolve(cos_, w, mode='nearest')
    fase_envu=np.arctan2(filsin,filcos)
    it+=1
    pbar.update(1)

#plot de la fase envuelta
plt.figure()
plt.imshow(fase_envu,cmap='gray')

plt.figure()
plt.imshow(np.unwrap(fase_envu),cmap='gray')

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
Z=np.c_[integ.cumtrapz(np.unwrap(fase_envu)-np.mean(np.unwrap(fase_envu))),np.zeros(tam_raw)]
surf = ax.plot_surface(X, Y, lamb/(4*np.pi*alpha*tam_col)*Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
#axisEqual3D(ax)

plt.show()