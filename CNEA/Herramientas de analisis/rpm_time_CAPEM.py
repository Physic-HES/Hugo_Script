import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from scipy import signal as S

dat_INA=[]
vec=[]
ruta='D:/BackUp Hugo Sosa/CNEA/Servicios EECE/Bomba INA/txt/'
m=[758,763,765,767,769,771,773,775]
pbar = tqdm(total=7, desc='Importando datos...')
for j in m:
    for c in np.arange(1,4):
        archivo=r'REC0%g_ch%g'%(j,c)
        imp_dat=pd.read_csv(ruta+archivo+'.txt', delimiter='\t',header=24)
        cols = imp_dat.values
        if c == 1:
            vec.append(cols[:,0])
            vec.append(cols[:,1])
        if c > 1:
            vec.append(cols[:,1])
    pbar.update(1)
    dat_INA.append(vec)
pbar.close()

def passband(dat1,lowcut,highcut):
    pbar = tqdm(total=len(dat1), desc='Filtrando datos...')
    for j in np.arange(len(dat1)):
        dat1_=[]
        dat2=[dat1[j][0]]
        for k in np.arange(1,len(dat1[0])):
            fs = 1 / (dat1[j][k][1] - dat1[j][k][0])
            len_sig = len(dat1[j][k])
            desde = int(lowcut / (fs / 2) * len_sig)
            hasta = int(highcut / (fs / 2) * len_sig)
            vent = np.zeros(len_sig)
            vent[desde:hasta] = 1
            vent2 = np.concatenate((vent, vent[-np.sort(-np.arange(len_sig))]))
            esp=np.fft.fft(dat1[j][k],n=2*len_sig)
            rms_esp=np.sqrt(np.sum(np.abs(esp[desde:hasta]))/len(np.abs(esp[desde:hasta])))
            esp_=np.real(np.fft.ifft(vent2*esp))
            rms_esp_=np.sqrt(np.sum(np.abs(np.fft.fft(esp_[desde:hasta],n=2*len_sig)))/len(np.abs(esp_[desde:hasta])))
            fa=rms_esp/rms_esp_
            F=fa*np.real(np.fft.ifft(vent2*esp))
            nuev=F[0:len_sig]
            dat2.append(nuev)
        pbar.update(1)
        dat1_.append(dat2)
    return dat1_

N=2048
overl=50
fs=1/(dat_INA[0][0][1]-dat_INA[0][0][0])
B=2*N
ov=int(overl/100*B)
f, t, Sxx=S.spectrogram(dat_INA[0][1],fs,
                                window='hann',nperseg=B,
                                noverlap=ov,scaling='spectrum')
plt.pcolormesh(t, f, Sxx, shading='gouraud')