import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as S
import scipy.integrate as inte
from matplotlib.colors import LogNorm

fs=1000
duration = 10  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2,dtype='float64')
#myarray=np.sin(2*np.pi*(20+(500-20)/20*np.linspace(0,duration,duration*fs))*np.linspace(0,duration,duration*fs))
#myrecording2 = sd.playrec(myarray, fs, channels=2)
print("Recording Audio")
sd.wait()
print("Audio recording complete")
#sd.play(myrecording, fs)
#sd.wait()
#print("Play Audio Complete")


def cascada(x,fs,wind='hann',lin=2048,overl=50):
    B=2*lin
    ov=int(overl/100*B)
    f,t,Spec=S.spectrogram(x,fs,window=wind,nperseg=B,
                                    noverlap=ov,scaling='spectrum')
    return f,t,Spec


signal=myrecording[:,0]+myrecording[:,1]
signal_int=inte.cumtrapz(signal,dx=1/fs)
f,t,Sxx=cascada(signal,fs,lin=75,overl=50)
plt.subplot(211)
tiem=np.linspace(0,duration,len(myrecording[:,0]))
plt.plot(tiem,signal)
plt.ylabel('Voltaje [V]')
plt.xlim([0,np.max(tiem)])
plt.grid()
plt.subplot(212)
plt.pcolormesh(t,f,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)))
plt.xlabel('Tiempo [s]')
plt.ylabel('Frecuencia [Hz]')
#plt.ylim([0,1000])
plt.show()

