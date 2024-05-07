#%%
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from tqdm import tqdm
from scipy import integrate as integ
import scipy.ndimage
import meshio
import scipy.interpolate as Sc

def importFEM(filename,H,W):
    mesh=meshio.read(filename)
    data=mesh.points+mesh.point_data['Displacement']
    data=data[data[:,2]>36.95,:]
    X,Y=np.meshgrid(np.linspace(np.min(data[:,0])+np.min(data[:,0])*0.03,np.max(data[:,0])-np.max(data[:,0])*0.03,W),
                    np.linspace(np.min(data[:,1])+np.min(data[:,1])*0.03,np.max(data[:,1])-np.max(data[:,1])*0.03,H),indexing='ij')
    points=np.zeros((len(data[:,2]),2))
    points[:,0]=data[:,0]
    points[:,1]=data[:,1]
    return Sc.griddata(points,data[:,2],(X,Y),method='nearest')


def sin_cos(fase_envu,ite):
    #filtro para fase envuelta
    w=1/105*np.ones((7,7))
    it=0
    itera=ite
    pbar = tqdm(total=itera, desc='Filtrando fase envuelta...')
    while it<itera:
        sin_=np.sin(fase_envu)
        cos_=np.cos(fase_envu)
        filsin=scipy.ndimage.convolve(sin_,w,mode='nearest')
        filcos = scipy.ndimage.convolve(cos_, w, mode='nearest')
        fase_envu=np.arctan2(filsin,filcos)
        it+=1
        pbar.update(1)
    return fase_envu


def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)


def gauss_def(X,Y,amp,p,s,ratio,angle):
    x,y=np.cos(angle)*(X-p[0])-np.sin(angle)*(Y-p[1])+p[0], np.sin(angle)*(X-p[0])+np.cos(angle)*(Y-p[1])+p[1]
    D=amp*np.exp(-(ratio[0]*(x-p[0])**2+ratio[1]*(y-p[1])**2)/(2*s**2))
    return D

# Parametros de la Camara
W,H=1248,960 # Ancho y Alto de la Imagen en pixeles
m=0.014 # Magnificacion de la camara
mu= 3.6 # Tamaño de pixel

# Parametros del Interferometro
d= 4 # Distancia de espejos al Bean Splitter en cm
D= (36+d*4)*1E4 # Distancia total al Objeto en micrones
Grano=8 # Tamaño de grano en pixeles para Imax/8 como umbral
tilt= 1 # angulo de giro del espejo en DEG
alpha=2*tilt*np.pi/180 # Angulo de shear en radianes

# Introduccion de Deformacion y calculo de shear
X,Y=np.meshgrid(range(W),range(H)) # Matrices X e Y de Pixeles
Fas=2*np.pi*np.random.random(X.shape) # Fasores Aleatorios
c=333/Grano # Apertura de filtro Pupila en pixeles
P=np.exp(-1/(2*c**2)*((X-W/2)**2+(Y-H/2)**2)) # Filtro Pupila
Phi=5*np.exp(-1/(2*(H/5)**2)*((X-W/2)**2+(Y-H/2)**2)) # Deformacion 1
#Phi=gauss_def(X,Y,1,[W/4,3*H/5],H/12,[1,1],0)+gauss_def(X,Y,2,[3*W/5,H/3],H/12,[1,0.5],np.pi/4)+gauss_def(X,Y,-1.3,[4*W/5,3*H/4],H/12,[1,0.5],-np.pi/4)+(W-X)*5E-4
#Phi=importFEM('C:/Users/user/Documents/Python Scripts/Hugo_Script/IAMEN/Desarrollos/deslaminado-CCX_Results.vtk',1248,960)
Phi=(Phi-np.min(Phi))
Speak=np.fft.ifft2(P*np.fft.fft2(Fas)) # Generacion de Speckle By Goodman
print(f'Angulo de shear: {alpha*180/np.pi/2} DEG') # Print Angulo de Shear en Grados
S=-int(np.tan(alpha)*D*m/mu) # Shear en Pixeles con direccion
print(f'Pixeles de shear: {S}') # Print de Shear en Pixeles con direccion
lamb=0.638 # Longitud de onda del laser
f=np.sin(np.abs(alpha))/lamb
print(f'Pixel de la frecuencia portadora {f*mu*W}')
Ilu=np.exp(-1/(2*650**2)*((X-W/2)**2+(Y-H/2)**2)) # Mascara de Iluminacion atenuada

#%%
# Generacion de Imagenes SPS
Im0_complex=Speak + np.roll(Speak*np.exp(1j*2*np.pi/lamb*np.sin(alpha)*mu*X),S,axis=1)
Im0=Ilu*np.abs(Im0_complex)**2 # Imagen sin Deformacion
Im0_complex_=Speak*np.exp(1j*2*np.pi/lamb*Phi) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*(np.sin(alpha)*mu*X+Phi)),S,axis=1)
Im0_=Ilu*np.abs(Im0_complex_)**2 # Imagen Con Deformacion
# Plot Imagen sin Deformacion
plt.imshow(Im0,cmap='gray')
plt.figure()
# Plot Imagen con Deformacion
plt.imshow(Im0_,cmap='gray')
plt.figure()
# Plot Imagen de la resta
plt.imshow(np.abs(Im0_-Im0),cmap='gray')

# Plots de la transformada de Fourier
Venta=np.exp(-1/(2*(f*mu*W*1/2)**2)*((X-(W/2+f*mu*W))**2+1/2*(Y-H/2)**2))
Venta=np.where(Venta>1/np.sqrt(2),Venta,0)
# Transformada Sin Deformacion
plt.figure()
plt.imshow(np.log2(np.abs(np.fft.fftshift(np.fft.fft2(Im0)))+1)+Venta, cmap='gray')
# Transformada Con Deformacion
plt.figure()
plt.imshow(np.log2(np.abs(np.fft.fftshift(np.fft.fft2(Im0_)))+1)+Venta, cmap='gray')

# Calculo de la fase envuelta
fftfilt0=np.fft.ifft2(np.fft.fftshift(Venta*(np.fft.fftshift(np.fft.fft2(Im0)))))
fftfilt0_=np.fft.ifft2(np.fft.fftshift(Venta*(np.fft.fftshift(np.fft.fft2(Im0_)))))
spsF0=np.arctan2(np.imag(fftfilt0),np.real(fftfilt0))
spsF0_=np.arctan2(np.imag(fftfilt0_),np.real(fftfilt0_))

fase_envu0_sps=(spsF0_-spsF0+np.pi)%(2*np.pi)
# Plot de la fase envuelta
plt.figure()
plt.imshow(fase_envu0_sps,cmap='gray')
plt.title('Metodo SPS')

#Plot de la fase envuelta filtrada
plt.figure()
fase_envu1_sps=sin_cos(fase_envu0_sps,40)
plt.imshow(fase_envu1_sps,cmap='gray')

#%%
#Shearografia TPS:

paso=1/4
Im0_complex_0=Speak*np.exp(1j*2*np.pi/lamb*(lamb*0*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*np.sin(alpha)*mu*X),S,axis=1)
Im0_0=Ilu*np.abs(Im0_complex_0)**2 # Imagen sin Deformacion
Im0_complex_1=Speak*np.exp(1j*2*np.pi/lamb*(lamb*1*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*np.sin(alpha)*mu*X),S,axis=1)
Im0_1=Ilu*np.abs(Im0_complex_1)**2 # Imagen sin Deformacion
Im0_complex_2=Speak*np.exp(1j*2*np.pi/lamb*(lamb*2*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*np.sin(alpha)*mu*X),S,axis=1)
Im0_2=Ilu*np.abs(Im0_complex_2)**2 # Imagen sin Deformacion
Im0_complex_3=Speak*np.exp(1j*2*np.pi/lamb*(lamb*3*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*np.sin(alpha)*mu*X),S,axis=1)
Im0_3=Ilu*np.abs(Im0_complex_3)**2 # Imagen sin Deformacion

Im0_complex_0_=Speak*np.exp(1j*2*np.pi/lamb*Phi)*np.exp(1j*2*np.pi/lamb*(lamb*0*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*(np.sin(alpha)*mu*X+Phi)),S,axis=1)
Im0_0_=Ilu*np.abs(Im0_complex_0_)**2 # Imagen Con Deformacion
Im0_complex_1_=Speak*np.exp(1j*2*np.pi/lamb*Phi)*np.exp(1j*2*np.pi/lamb*(lamb*1*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*(np.sin(alpha)*mu*X+Phi)),S,axis=1)
Im0_1_=Ilu*np.abs(Im0_complex_1_)**2 # Imagen Con Deformacion
Im0_complex_2_=Speak*np.exp(1j*2*np.pi/lamb*Phi)*np.exp(1j*2*np.pi/lamb*(lamb*2*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*(np.sin(alpha)*mu*X+Phi)),S,axis=1)
Im0_2_=Ilu*np.abs(Im0_complex_2_)**2 # Imagen Con Deformacion
Im0_complex_3_=Speak*np.exp(1j*2*np.pi/lamb*Phi)*np.exp(1j*2*np.pi/lamb*(lamb*3*paso)) + np.roll(Speak*np.exp(1j*2*np.pi/lamb*(np.sin(alpha)*mu*X+Phi)),S,axis=1)
Im0_3_=Ilu*np.abs(Im0_complex_3_)**2 # Imagen Con Deformacion

tpsF0=np.arctan2(Im0_3-Im0_1,Im0_2-Im0_0)
tpsF0_=np.arctan2(Im0_3_-Im0_1_,Im0_2_-Im0_0_)

fase_envu0_tps=(tpsF0_-tpsF0+np.pi)%(2*np.pi)
plt.figure()
plt.imshow(fase_envu0_tps,cmap='gray')
plt.title('Metodo TPS')

#%%
# Desenvolvimiento e Integracion
plt.figure()
plt.imshow(np.unwrap(fase_envu1_sps),cmap='gray')
plt.title('Desenvolvimiento SPS (con filtro sin cos)')
plt.figure()
plt.imshow(np.unwrap(fase_envu0_tps),cmap='gray')
plt.title('Desenvolvimiento TPS (sin filtro sin cos)')

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
Z=np.c_[integ.cumtrapz(np.unwrap(fase_envu1_sps)-np.mean(np.unwrap(fase_envu1_sps))),np.zeros(H)]
surf = ax.plot_surface(Y, X, lamb/(2*np.pi*np.abs(S))*Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.title('Integracion SPS')
fig, ax_tps = plt.subplots(subplot_kw={"projection": "3d"})
Z_tps=np.c_[integ.cumtrapz(np.unwrap(fase_envu0_tps)-np.mean(np.unwrap(fase_envu0_tps))),np.zeros(H)]
surf = ax_tps.plot_surface(Y, X, lamb/(2*np.pi*np.abs(S))*Z_tps, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
plt.title('Integracion TPS')

fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
surf3 = ax2.plot_surface(Y, X, Phi-lamb/(2*np.pi*np.abs(S))*Z, cmap=cm.Blues,
                       linewidth=0, antialiased=False, alpha=0.25)
#surf2 = ax2.plot_surface(Y, X, lamb/(2*np.pi*np.abs(S))*Z, cmap=cm.coolwarm,
#                       linewidth=0, antialiased=False, alpha=0.75)
surf2 = ax2.plot_surface(Y, X, Phi-lamb/(2*np.pi*np.abs(S))*Z_tps, cmap=cm.Greens,
                       linewidth=0, antialiased=False, alpha=0.25)

#axisEqual3D(ax)

# Cortes de mitad de imagen:
# Frentes de onda
plt.figure()
plt.grid()
plt.plot(X[int(H/2),:],Phi[int(H/2),:],'-b',label='Fase de Deformacion Espejo Fijo')
plt.plot(X[int(H/2),:],np.roll(Phi,S,axis=1)[int(H/2),:],'--b',label='Fase de Deformacion Espejo Movil')
plt.fill_between(X[int(H/2),:],Phi[int(H/2),:],np.roll(Phi,S,axis=1)[int(H/2),:],color='orange',alpha=0.25)
plt.plot(X[int(H/2),:],lamb/(2*np.pi)*(fase_envu1_sps[int(H/2),:]-fase_envu1_sps[int(H/2),:].min()),label='Fase envuelta')
plt.plot(X[int(H/2),:],lamb/(2*np.pi)*(np.unwrap(fase_envu1_sps)[int(H/2),:]-np.unwrap(fase_envu1_sps)[int(H/2),:].mean()),label='Desenvolvimiento de Fase')
plt.plot(X[int(H/2),:],lamb/(2*np.pi*np.abs(S))*Z[int(H/2),:],label='Integracion de Fase desenvuelta / Shear')
plt.ylabel(r'Deformación [$\mu m$]')
plt.xlabel('Ancho del sensor [pixeles]')
plt.legend()

# Frentes de onda con inclinacion incluida
plt.figure()
plt.grid()
Im0c2=np.roll(np.exp(1j*2*np.pi/lamb*np.sin(alpha)*X),S,axis=1)
Im0c2_=np.roll(np.exp(1j*2*np.pi/lamb*(np.sin(alpha)*X+Phi)),S,axis=1)
Im0c2_B=np.exp(1j*2*np.pi/lamb*Phi)
f0=np.arctan2(np.imag(Im0c2),np.real(Im0c2))
f0_=np.arctan2(np.imag(Im0c2_),np.real(Im0c2_))
f0_B=np.arctan2(np.imag(Im0c2_B),np.real(Im0c2_B))
plt.plot(X[int(H/2),:],lamb/(2*np.pi)*np.unwrap(f0)[int(H/2),:],label=r'$\Delta \Phi$ sin deformación')
plt.plot(X[int(H/2),:],lamb/(2*np.pi)*(np.unwrap(f0_)[int(H/2),:]-np.unwrap(f0_B)[int(H/2),:]),label=r'$\Delta \Phi$ con deformación')
plt.plot(X[int(H/2),:],lamb/(2*np.pi)*(np.unwrap(f0_)[int(H/2),:]-np.unwrap(f0_B)[int(H/2),:]-np.unwrap(f0)[int(H/2),:]),label='Diferencia')
plt.ylabel(r'Camino óptico [$\mu m$]')
plt.xlabel('Ancho del sensor [pixeles]')
plt.legend()
plt.show()