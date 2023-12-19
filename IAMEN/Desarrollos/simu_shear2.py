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

tam_col,tam_raw=1280,920
X,Y=np.meshgrid(range(tam_col),range(tam_raw))
f_corr=3E2 #factor de correccion
shift_obj=0.04E6
D=0.477E6
lamb=0.638
mu=3
alpha=np.arctan(shift_obj/D)
print(f'periodo espacial k = {1/(np.sin(alpha)/lamb*mu)}')
f=np.sin(alpha)/lamb*mu
Ap=1.44/(np.sin(alpha)/lamb)*mu
print(f'pixel de la portadora tam_col/2+1/k*tam_col: {tam_col/2+f*tam_col}')
print(f'pixeles de apertura de la lente pupila: {Ap}')
print(f'Corrimiento en pantalla (Shear): {int(alpha*tam_col/2)}')


c=200
c2=c/3

# SIMULACION DE SPECKLE
# By Hugo (Tarda mucho: 1600 iter/min)
def speckle_H(Im,tam_g,iter):
    c=100
    tam_col, tam_raw = len(Im[0,:]), len(Im[:,0])
    X, Y = np.meshgrid(range(tam_col), range(tam_raw))
    gauss_0 = np.exp(-1 / (2 * (1.5 * c) ** 2) * ((X - tam_col / 2) ** 2 + (Y - tam_raw / 2) ** 2))
    h=0
    px = tam_col * np.random.random()
    py = tam_raw * np.random.random()
    ph = 2 * np.pi * np.random.random()
    gran = np.exp(-1 / (2 * tam_g ** 2) * ((X - px) ** 2 + (Y - py) ** 2)) * np.exp(1j * ph)
    pbar = tqdm(total=iter, desc='Calculando speckle...')
    while h<iter:
        px = np.random.normal(tam_col/2,tam_col/2)
        py = np.random.normal(tam_raw/2,tam_raw/2)
        ph = 2*np.pi*np.random.random()
        gran += np.exp(-1 / (2 * tam_g ** 2) * ((X - px) ** 2 + (Y - py) ** 2)) * np.exp(1j * ph)
        h += 1
        pbar.update(1)
    speck = gauss_0 * np.abs(gran)
    return speck


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
    imagefield2=np.fft.ifft2(gauss_lens*np.exp(1j*alpha/2*np.pi*(X-tam_col/2)))*np.exp(1j*2*np.pi*np.sin(alpha)/lamb*mu*(X-tam_col/2))
    IMs=np.abs(imagefield+imagefield2)**2
    IMd=np.abs(imagefield*np.exp(1j*4*np.pi/lamb*phi)+imagefield2*np.exp(1j*4*np.pi/lamb*phi*(X-tam_col/2)))**2
    return gauss_0*IMs,gauss_0*IMd


#generacion de speckle
gauss_0=np.exp(-1/(2*(1.5*c)**2)*((X-tam_col/2)**2+(Y-tam_raw/2)**2))
#speckle2=speckle_G(X,2)

#Fase de la deformacion
amp=110 #amplitud de la deformacion en micrones
#DERIVADA de la deformacion fuera de plano (Out-of-Plane Deformation)
Z=-4*np.pi*(shift_obj/f_corr)/lamb*amp*np.exp(-1/(2*c**2)*((X-tam_col/2)**2+(Y-tam_raw/2)**2))*(X-tam_col/2)/(c**2)
ph_wrap=(Z+np.pi)%(2*np.pi)
phase=ph_wrap-np.mean(ph_wrap)
DEF=-amp/(c**2)*np.exp(-1/(2*c**2)*((X-tam_col/2)**2+(Y-tam_raw/2)**2))


#Imagenes con y sin carga
#Im_0=normalize(speckle2*(np.sin(2*np.pi*f*X)/2+1),0,1)
#Im_1=normalize(speckle2*(np.sin(2*np.pi*f*X+phase)/2+1),0,1)
Im_0,Im_1=speckle_G(X,2,alpha,DEF)


cv2.imshow('prueba',Im_1)
cv2.destroyWindow('prueba')

plt.figure()
plt.imshow(np.log2(Im_0+1),cmap='gray') #imagen sin carga
plt.figure()
plt.imshow(np.log2(Im_1+1),cmap='gray') #imagen con carga
#plt.figure()
#plt.imshow(np.sin(2*np.pi*f*X+phase)/2+1-(np.sin(2*np.pi*f*X)/2+1),cmap='gray') #portadora con carga menos portadora sin carga
#plt.figure()
#plt.imshow(np.log2(speckle2+1),cmap='gray') #speckle simulado (sin portadora)

# construccion de la ventana sobre la portadora
gauss=np.exp(-1/2*(((X-(tam_col/2+f*tam_col+4))/(1.5*c2))**2+((Y-tam_raw/2)/c2)**2))
gauss=np.where(((X-(tam_col/2+f*tam_col+4))/(1.5*(c2*2)))**2+((Y-tam_raw/2)/(c2*2))**2<1,gauss,0)

plt.figure()
plt.imshow(normalize(np.abs(Im_1-Im_0),0,1),cmap='gray') #imagen resta
fftIm_0=np.abs(np.fft.fftshift(np.fft.fft2(Im_0))) #fft de la imagen de referencia
plt.figure()
plt.imshow(np.log2(fftIm_0+1)) #ploteo logaritmico de la fft de la imagen de referencia
plt.imshow(gauss,cmap='hot',alpha=.2)
fftIm_1=np.abs(np.fft.fftshift(np.fft.fft2(Im_1))) #fft de la imagen con carga
plt.figure()
plt.imshow(np.log2(fftIm_1+1)) #ploteo logaritmico de la fft de la imagen con carga
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
#masc=np.where(((X-tam_col/2)/(tam_col/3))**2+((Y-tam_raw/2)/(tam_raw/3))**2<1,1,0)
#fase_envu=np.abs(np.fft.ifft2(np.fft.fftshift(masc*np.fft.fftshift(np.fft.fft2(fase_envu)))))
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
surf = ax.plot_surface(X, Y, lamb/(4*np.pi)*Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
axisEqual3D(ax)

plt.show()
