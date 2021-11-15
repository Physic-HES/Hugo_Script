import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from scipy import signal as S

dat_INA=[]
ruta='D:/BackUp Hugo Sosa/CNEA/Servicios EECE/Bomba INA/txt/'
m=[758,763,765,767,769,771,773,775]
pbar = tqdm(total=8, desc='Importando datos...')
for j in m:
    vec = []
    for c in np.arange(1,4):
        archivo=r'REC0%g_ch%g'%(j,c)
        imp_dat=pd.read_csv(ruta+archivo+'.txt', delimiter='\t',header=14)
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
    pbar = tqdm(total=len(dat1), desc='Analizando archivo...')
    dat1_ = []
    for j in np.arange(len(dat1)):
        dat2=[dat1[j][0]]
        fs = 1 / (dat1[j][0][1] - dat1[j][0][0])
        pbar2 = tqdm(total=len(dat1[0]) - 1, desc='Filtrando canales...')
        for k in np.arange(1,len(dat1[0])):
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
            pbar2.update(1)
        pbar2.close()
        pbar.update(1)
        dat1_.append(dat2)
    pbar.close()
    return dat1_


dat1_=passband(dat_INA,46,53)

def get_rpm(X,m):
    df=pd.DataFrame()
    for j in np.arange(0,len(m)):
        for k in np.arange(1,len(X[j])):
            print([j,k])
            ceros = np.where(np.diff(np.sign(np.diff(X[j][k]))))[0]
            df[r'time_REC%g_ch%g'%(m[j],k)]=X[j][0][ceros[:len(ceros)-1]]
            df[r'rpm_REC%g_ch%g'%(m[j],k)]=1/np.diff(X[j][k][ceros])/2*60
            plt.plot(df[r'time_REC%g_ch%g'%(m[j],k)],df[r'rpm_REC%g_ch%g'%(m[j],k)],label=r'REC%g_ch%g'%(m[j],k))

get_rpm(dat1_,m)
