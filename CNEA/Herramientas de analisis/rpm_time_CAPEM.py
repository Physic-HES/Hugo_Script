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

N=2048
overl=50
fs=1/(dat_INA[0][0][1]-dat_INA[0][0][0])
B=2*N
ov=int(overl/100*B)
f, t, Sxx=S.spectrogram(dat_INA[0][1],fs,
                                window='hann',nperseg=B,
                                noverlap=ov,scaling='spectrum')
plt.pcolormesh(t, f, Sxx, shading='gouraud')