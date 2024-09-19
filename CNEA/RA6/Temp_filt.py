import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as S

Ensayo_CC = 'C:\\Users\\user\\Documents\\EECE\\RA 6\\Mediciones en RA-6\\RA6\\Mediciones\\10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z\\EXCITACION\\temp_txt\\'
Ensayo_CP = 'C:\\Users\\user\\Documents\\EECE\\RA 6\\Mediciones en RA-6\\RA6\\Mediciones\\10-7-24 ENSAYO CON CAMION EN PORTON\\CAMION\\temp_txt\\'

def cargar(carp,n):
    for c in range(1,5):
        if c==1:
            ch = np.loadtxt(carp+f'REC{n}_ch{c}.txt',skiprows=16)
        else:
            ch = np.c_[ch,np.loadtxt(carp+f'REC{n}_ch{c}.txt',skiprows=16)[:,1]]
    return ch

def graf(tit,ens):
    plt.figure()
    for c in range(1,5):
        plt.plot(ens[:,0],ens[:,c],label=f'Ch{c}')
    plt.legend()
    plt.title(tit)

def fourier(ens,lineas=1024,overl=50):
    fs = 1/(ens[1,0]-ens[0,0])
    B=2*lineas
    Sc2=1/np.mean(S.get_window('hann',lineas))
    for c in range(1,5):
        if c == 1:
            f,m = S.welch(ens[:,c],fs,window='hann',nperseg=B,noverlap=ov,scaling='spectrum')
            Spec = np.c_[f,np.sqrt(m*Sc2)]
        else:
            _,m =S.welch(ens[:,c],fs,window='hann',nperseg=B,noverlap=ov,scaling='spectrum')
            Spec = np.c_[Spec,np.sqrt(m*Sc2)]
    return Spec

CP_X = cargar(Ensayo_CP,1754)
CP_Y = cargar(Ensayo_CP,1750)
CP_Z = cargar(Ensayo_CP,1741)

CC_Z = cargar(Ensayo_CC,1769)

CP_X_fourier = fourier(CP_X)
CP_Y_fourier = fourier(CP_Y)
CP_Z_fourier = fourier(CP_Z)

CC_Z_fourier = fourier(CC_Z)

graf('Ensayo Camion en el porton - Eje X',CP_X)
graf('Ensayo Camion en el porton - Eje Y',CP_Y)
graf('Ensayo Camion en el porton - Eje Z',CP_Z)
graf('Ensayo Camion en el calle - Eje Z',CC_Z)

graf('Espectros Ensayo Camion en el porton - Eje X',CP_X_fourier)
graf('Espectros Ensayo Camion en el porton - Eje Y',CP_Y_fourier)
graf('Espectros Ensayo Camion en el porton - Eje Z',CP_Z_fourier)
graf('Espectros Ensayo Camion en el calle - Eje Z',CC_Z_fourier)

plt.show()