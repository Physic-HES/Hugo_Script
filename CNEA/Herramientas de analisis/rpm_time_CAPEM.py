import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from scipy import signal as S
from matplotlib.colors import LogNorm


def imp(ruta,m,can):
    dat_INA = []
    pbar = tqdm(total=can, desc='Importando datos...')
    for j in m:
        vec = []
        for c in np.arange(1,can):
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
    return dat_INA



ruta='D:/BackUp Hugo Sosa/CNEA/Servicios EECE/Bomba INA/txt/'
m=[769] #caudal20 INA
ruta2='D:/BackUp Hugo Sosa/CNEA/Servicios EECE/Bomba INA/Medicion en CAPEM/Temp/'
m2=[158] #caudal20 CAPEM 2018
ruta3='D:/BackUp Hugo Sosa/CNEA/Servicios EECE/Bomba INA/Medicion en CAPEM/Medicion2020/Temps/'
m3=[402] #caudal20 CAPEM 2020

ina=imp(ruta,m,4) #INA
cap1=imp(ruta2,m2,5) #CAPEM 2018
cap2=imp(ruta3,m3,5) #CAPEM 2020

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


ina=passband(ina,5,100)
cap1=passband(cap1,5,100)
cap2=passband(cap2,5,70)

def get_rpm(X,m,ch,title):
    #df=pd.DataFrame()
    for j in np.arange(0,len(m)):
        for k in ch:
            fs= 1/(X[j][0][1]-X[j][0][0])
            f, t, Sxx = S.spectrogram(X[j][k], fs,
                                      window='hann', nperseg=int(8*fs),
                                      noverlap=int(95/100*8*fs), scaling='spectrum')
            signal=[t,f[np.argmax(Sxx,axis=0)]*60]
            print(title+r': %g'%np.mean(signal[1])+r'+-%g RPM'%np.std(signal[1]))
            print(r'Delta T: %g seg'%t[1])
            print(r'Delta f: %g Hz o %g RPM'%(f[1],f[1]*60))
            #Vmax1 = np.max(np.max(Sxx))
            #Vmin1 = Vmax1 / 1E5
            #plt.figure()
            #plt.ylim([36 * 60, 66 * 60])
            #plt.pcolormesh(t, f*60, Sxx,
            #               shading='gouraud', norm=LogNorm(vmin=Vmin1, vmax=Vmax1))
            #plt.plot(t,f[np.argmax(Sxx,axis=0)]*60,'-r',label=r'RPM_REC%g_ch%g'%(m[j],k))
            #plt.xlabel('Tiempo [seg]')
            #plt.ylabel('RPM')
            #plt.title(title)
            #plt.legend()
            #ceros = np.where(np.diff(np.sign(np.diff(X[j][k]))))[0]
            #df[r'time_REC%g_ch%g'%(m[j],k)]=X[j][0][ceros[:len(ceros)-1]]
            #df[r'rpm_REC%g_ch%g'%(m[j],k)]=1/np.diff(X[j][k][ceros])/2*60
            #plt.plot(df[r'time_REC%g_ch%g'%(m[j],k)],df[r'rpm_REC%g_ch%g'%(m[j],k)],label=r'REC%g_ch%g'%(m[j],k))
    #plt.show()
    return signal


inaRPM=get_rpm(ina,m,[3],'RPM(t) ensayo INA')
cap1RPM=get_rpm(cap1,m2,[4],'RPM(t) ensayo CAPEM 2018')
cap2RPM=get_rpm(cap2,m3,[4],'RPM(t) ensayo CAPEM 2020')
