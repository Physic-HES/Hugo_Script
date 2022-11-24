import soundfile as sf
import sounddevice as sd
import numpy as np
import pandas as pd
import scipy.signal as S
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
path1='/home/hp1opticaiamend/Documents/labo4/Practica especial/dia4-20221124T165400Z-001/dia4/WhatsApp_11.03.54.wav'
path2='/home/hp1opticaiamend/Documents/labo4/Practica especial/dia4-20221124T165400Z-001/dia4/WhatsApp_11.17.35.wav'
path1_='/home/hp1opticaiamend/Documents/labo4/Practica especial/dia4-20221124T165400Z-001/dia4/datos2_dia4_voz.txt'
path2_='/home/hp1opticaiamend/Documents/labo4/Practica especial/dia4-20221124T165400Z-001/dia4/datos4_dia4_voz.txt'
aud1,fs1=sf.read(path1)
aud2,fs2=sf.read(path2)
aud1_fotoD=pd.read_csv(path1_,header=None,delimiter=' ')
aud2_fotoD=pd.read_csv(path2_,header=None,delimiter=' ')
#plt.plot(aud1_fotoD.values[:,0],aud1_fotoD.values[:,1])
FS=1/aud1_fotoD.values[1,0]
f,t,Sxx=S.spectrogram(aud1_fotoD.values[int(1*FS):int(2*FS),1],FS,window='hann',nperseg=2*75,
                              noverlap=int(95/100*2*75),scaling='spectrum')
plt.pcolormesh(t,f,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)),cmap='jet')
plt.figure()
t1=np.linspace(0,1/fs1*len(aud1),len(aud1))
plt.plot(t1[int(0.5*fs1):int(2.5*fs1)],aud1[int(0.5*fs1):int(2.5*fs1)])
plt.show()