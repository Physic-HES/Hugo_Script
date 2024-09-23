import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as S
import imageio.v2 as imageio
from io import BytesIO

Ensayo_CC = 'C:\\Users\\user\\Documents\\EECE\\RA 6\\Mediciones en RA-6\\RA6\\Mediciones\\10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z\\EXCITACION\\temp_txt\\'
Ensayo_CP = 'C:\\Users\\user\\Documents\\EECE\\RA 6\\Mediciones en RA-6\\RA6\\Mediciones\\10-7-24 ENSAYO CON CAMION EN PORTON\\CAMION\\temp_txt\\'

def cargar(carp,n):
    for c in range(1,5):
        if c==1:
            ch = np.loadtxt(carp+f'REC{n}_ch{c}.txt',skiprows=16)
        else:
            ch = np.c_[ch,np.loadtxt(carp+f'REC{n}_ch{c}.txt',skiprows=16)[:,1]]
    return ch

def graf(tit,ens,iftemp=1):
    plt.figure()
    for c in range(1,ens.shape[1]):
        plt.plot(ens[:,0],ens[:,c],label=f'Ch{c}')
        rang = get_gango(ens)
        if iftemp==1:
            plt.axvline(rang[0]*(ens[1,0]-ens[0,0]),linestyle='--')
            plt.axvline(rang[-1]*(ens[1,0]-ens[0,0]),linestyle='--')
    plt.legend()
    plt.title(tit)

def fourier(ens,lineas=450,overl=50):
    fs = 1/(ens[1,0]-ens[0,0])
    B=2*lineas
    ov=int(overl/100*B)
    Sc2=1/np.mean(S.get_window('hann',lineas))
    for c in range(1,5):
        if c == 1:
            f,m = S.welch(ens[:,c],fs,window='hann',nperseg=B,noverlap=ov,scaling='spectrum')
            Spec = np.c_[f,np.sqrt(m*Sc2)]
        else:
            _,m =S.welch(ens[:,c],fs,window='hann',nperseg=B,noverlap=ov,scaling='spectrum')
            Spec = np.c_[Spec,np.sqrt(m*Sc2)]
    return Spec

def get_gango(temp):
    fs = 1/(temp[1,0]-temp[0,0])
    maxim = np.max(temp[:,1:],axis=0)
    col = np.argmax(maxim)
    ind = np.where(temp[:,int(col+1)] == np.max(maxim))[0]
    rango = range(int(ind[0]-1*fs),int(ind[0]+13*fs+1))
    return rango

def pasabanda(ens,band):
    fs = 1 / (ens[1,0] - ens[0,0])
    len_sig = ens.shape[0]
    result = np.zeros_like(ens)
    result[:,0] = ens[:,0]
    for k in np.arange(1,ens.shape[1]):
        desde = int(band[0] / (fs / 2) * len_sig)
        hasta = int(band[1] / (fs / 2) * len_sig)
        vent = np.zeros(len_sig)
        vent[desde:hasta] = 1
        vent2 = np.concatenate((vent, vent[-np.sort(-np.arange(len_sig))]))
        esp=np.fft.fft(ens[:,k],n=2*len_sig)
        rms_esp=np.sqrt(np.sum(np.abs(esp[desde:hasta]))/len(np.abs(esp[desde:hasta])))
        esp_=np.real(np.fft.ifft(vent2*esp))
        rms_esp_=np.sqrt(np.sum(np.abs(np.fft.fft(esp_[desde:hasta],n=2*len_sig)))/len(np.abs(esp_[desde:hasta])))
        fa=rms_esp/rms_esp_
        F=fa*np.real(np.fft.ifft(vent2*np.fft.fft(ens[:,k],n=2*len_sig)))
        nuev=F[0:len_sig]
        result[:,k]=nuev.T
    return result

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

CP_X = cargar(Ensayo_CP,1754)
CP_Y = cargar(Ensayo_CP,1750)
CP_Z = cargar(Ensayo_CP,1741)

CC_Z = cargar(Ensayo_CC,1769)

CP_X_fourier = fourier(CP_X[get_gango(CP_X),:])
CP_Y_fourier = fourier(CP_Y[get_gango(CP_Y),:])
CP_Z_fourier = fourier(CP_Z[get_gango(CP_Z),:])

CC_Z_fourier = fourier(CC_Z[get_gango(CC_Z),:])

graf('Ensayo Camion en el porton - Eje X',CP_X)
graf('Ensayo Camion en el porton - Eje Y',CP_Y)
graf('Ensayo Camion en el porton - Eje Z',CP_Z)
graf('Ensayo Camion en el calle - Eje Z',CC_Z)

graf('Espectros Ensayo Camion en el porton - Eje X',CP_X_fourier,0)
graf('Espectros Ensayo Camion en el porton - Eje Y',CP_Y_fourier,0)
graf('Espectros Ensayo Camion en el porton - Eje Z',CP_Z_fourier,0)
graf('Espectros Ensayo Camion en el calle - Eje Z',CC_Z_fourier,0)

CP_X_transf = np.c_[CP_X_fourier[:,0],CP_X_fourier[:,2:]/np.tile(CP_X_fourier[:,1],(3,1)).T]
CP_Y_transf = np.c_[CP_Y_fourier[:,0],CP_Y_fourier[:,2:]/np.tile(CP_Y_fourier[:,1],(3,1)).T]
CP_Z_transf = np.c_[CP_Z_fourier[:,0],CP_Z_fourier[:,2:]/np.tile(CP_Z_fourier[:,1],(3,1)).T]
CC_Z_transf = np.c_[CC_Z_fourier[:,0],CC_Z_fourier[:,2:]/np.tile(CC_Z_fourier[:,1],(3,1)).T]

graf('Transferencia Ensayo Camion en el porton - Eje X',CP_X_transf,0)
graf('Transferencia Ensayo Camion en el porton - Eje Y',CP_Y_transf,0)
graf('Transferencia Ensayo Camion en el porton - Eje Z',CP_Z_transf,0)
graf('Transferencia Ensayo Camion en el calle - Eje Z',CC_Z_transf,0)

CP_X_filt = pasabanda(CP_X,[1,10])
CP_Y_filt = pasabanda(CP_Y,[1,10])
CP_Z_filt = pasabanda(CP_Z,[1,10])
CC_Z_filt = pasabanda(CC_Z,[1,10])

graf('Ensayo Camion en el porton - Eje X (pasabandas de 1 a 10 Hz)',CP_X_filt[get_gango(CP_X_filt),:],0)
graf('Ensayo Camion en el porton - Eje Y (pasabandas de 1 a 10 Hz)',CP_Y_filt[get_gango(CP_Y_filt),:],0)
graf('Ensayo Camion en el porton - Eje Z (pasabandas de 1 a 10 Hz)',CP_Z_filt[get_gango(CP_Z_filt),:],0)
graf('Ensayo Camion en el calle - Eje Z (pasabandas de 1 a 10 Hz)',CC_Z_filt[get_gango(CC_Z_filt),:],0)

plt.show()

def anim_CP():
    plt.ion()

    fig = plt.figure(figsize=(500,800))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])
    ax1 = fig.add_subplot(gs[0],projection='3d')
    amp = 4.5E3
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(CP_X_filt[:,0],CP_X_filt[:,1],label='Ch1 X')
    ax2.plot(CP_Y_filt[:,0],CP_Y_filt[:,1],label='Ch1 Y')
    ax2.plot(CP_Z_filt[:,0],CP_Z_filt[:,1],label='Ch1 Z')
    ax2.set_xlim([9,20])
    ax2.set_xlabel('Tiempo [s]')
    ax2.set_ylabel('Aceleracion [g]')
    ax2.legend()
    images = []
    for j in range(get_gango(CP_X_filt)[0]-100,get_gango(CP_X_filt)[-1]-2000):
        ax1.scatter3D(8+amp*CP_X_filt[j,1],-2+amp*CP_Y_filt[j,1],0+amp*CP_Z_filt[j,1],'or',label='Ch1')
        ax1.scatter3D(2+amp*CP_X_filt[j,2],1+amp*CP_Y_filt[j,2],0+amp*CP_Z_filt[j,2],'or',label='Ch2')
        ax1.scatter3D(1+amp*CP_X_filt[j,3],0+amp*CP_Y_filt[j,3],7+amp*CP_Z_filt[j,3],'or',label='Ch3')
        ax1.scatter3D(2,1,-4+amp*CP_Z_filt[j,3],'or',label='Ch4')
        ax1.set_xlim([-3,10])
        ax1.set_ylim([-6,7])
        ax1.set_zlim([-5,8])
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.legend()
        axisEqual3D(ax1)
        line = ax2.axvline(CP_X_filt[j,0])
        plt.pause(0.001)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        images.append(imageio.imread(buf))
        ax1.cla()
        line.remove()
        plt.draw()

    imageio.mimsave('animacion.gif', images, fps=150)

#anim_CP()
