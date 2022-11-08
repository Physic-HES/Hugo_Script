import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as S
import scipy.integrate as inte
from matplotlib.colors import LogNorm

fs=10000
duration = 10  # seconds
#myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
#myrecording = sd.playrec(myarray, fs, channels=2)
myrecording=np.sin(2*np.pi*250*np.linspace(0,duration,duration*fs)+75*np.sin(2*np.pi*0.5*np.linspace(0,duration,duration*fs)))
print("Recording Audio")
sd.wait()
print("Audio recording complete , Play Audio")
sd.play(myrecording, fs)
sd.wait()
print("Play Audio Complete")


def cascada(x,fs,wind='hann',lin=2048,overl=50):
    B=2*lin
    ov=int(overl/100*B)
    f,t,Spec=S.spectrogram(x,fs,window=wind,nperseg=B,
                                    noverlap=ov,scaling='spectrum')
    return f,t,Spec


#signal=myrecording[:,0]+myrecording[:,1]
#signal_int=inte.cumtrapz(signal,dx=1/fs)
#f,t,Sxx=cascada(signal_int,fs,lin=1000,overl=50)
#plt.subplot(211)
#tiem=np.linspace(0,duration,len(myrecording[:,0])-1)
#plt.plot(tiem,signal_int)
#plt.ylabel('Voltaje [V]')
#plt.xlim([0,np.max(tiem)])
#plt.grid()
#plt.subplot(212)
#plt.pcolormesh(t,f,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)))
#plt.xlabel('Tiempo [s]')
#plt.ylabel('Frecuencia [Hz]')
#plt.ylim([0,2500])
#plt.show()

