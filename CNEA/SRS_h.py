import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy import linalg as npl
import os

# Spec del Requerimiento
def loginterp(M):
    f2=np.zeros((len(M)-1)*2000)
    amp=np.zeros((len(M)-1)*2000)
    for k in np.arange(1,len(M[:,0])):
        f=np.linspace(M[k-1,0],M[k,0],2000)
        f2[(k-1)*2000:k*2000]=f
        amp[(k-1)*2000:k*2000]=np.exp((np.log(M[k,1])-np.log(M[k-1,1]))/(np.log(M[k,0])-np.log(M[k-1,0]))*(np.log(f)-np.log(M[k-1,0]))+np.log(M[k-1,1]))
    return [f2,amp]

# Función SRS
def SRS_h1(S,Q,Spec,hs):
    Fs=1/(S[0][1]-S[0][0])
    damp_type4=1/(2*Q)
    freq_typ4=np.arange(0,Fs/2,Fs/len(S[1]))
    ini = np.log2(np.min(Spec[0]))
    fin = np.log2(np.max(Spec[0]))
    j_typ4 = np.linspace(ini,fin,hs)
    step_typ4 = np.vstack(2**j_typ4)
    freqM=np.matlib.repmat(freq_typ4,len(j_typ4),1)
    stepM=np.matlib.repmat(step_typ4,1,len(freq_typ4))
    H=(stepM**2+1j*2*damp_type4*stepM*freqM)/(stepM**2-freqM**2+1j*2*damp_type4*stepM*freqM)
    H=np.concatenate((H,np.conj(H[:,::-1])),axis=1)
    Y3=np.matlib.repmat(np.fft.fft(S[1]),len(j_typ4),1)*H
    return [step_typ4,np.max(np.abs(np.fft.ifft(Y3,axis=1)),axis=1)]

Spec=np.matrix([[100,20],[2000,2850],[10000,2850]])
Spec2=loginterp(Spec)
Q=10
hs=500
Arch = os.listdir('C:/Users/Toshiba3/Documents/HUGO/Servicios EECE/Solares/Pruebas Sergio/temp/')
plt.loglog(Spec2[0],Spec2[1],'--r',label='Requerimiento')
plt.loglog(Spec2[0],3*Spec2[1],'--k')
plt.loglog(Spec2[0],1/3*Spec2[1],'--k')
for j in np.arange(len(Arch)):
    if j<7:
        dat = np.loadtxt(r'C:/Users/Toshiba3/Documents/HUGO/Servicios EECE/Solares/Pruebas Sergio/temp/%s' % (Arch[j]),
                     skiprows=1, usecols=(0, 8))
        S = [dat[:, 0]/1000, dat[:, 1]]
    if j>=7 and j<=11:
        dat = np.loadtxt(r'C:/Users/Toshiba3/Documents/HUGO/Servicios EECE/Solares/Pruebas Sergio/temp/%s'%(Arch[j]),
                         skiprows=1, usecols=(0, 2))
        S = [dat[:, 0]/1000, dat[:, 1]]
    if j>11:
        dat = np.loadtxt(r'C:/Users/Toshiba3/Documents/HUGO/Servicios EECE/Solares/Pruebas Sergio/temp/%s'%(Arch[j]),
                         skiprows=0, usecols=(0, 1))
        S=[dat[:,0],dat[:,1]]
    srs=SRS_h1(S,10,Spec2,46)
    plt.loglog(srs[0],srs[1],label=Arch[j])
plt.grid()
plt.legend()
plt.xlabel('Frequency [Hz]')
plt.ylabel('Acceleration [G]')
plt.title('Shock Response Spectrum')
plt.show()
