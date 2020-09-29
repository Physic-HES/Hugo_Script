import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy import linalg as npl

# Sintesis de señal
def sint(P,tim):
    t1=np.arange(0,tim,1/Fs)
    w = np.zeros(len(t1))
    for j in range(len(P[0,:])-1):
        t=np.arange(P[1,j],P[1,j]+P[3,j]/(2*P[0,j]),1/Fs)
        w2=P[2,j]*np.sin(2*np.pi*P[0,j]/P[3,j]*(t-P[1,j]))*np.sin(2*np.pi*P[0,j]*(t-P[1,j]))
        k=np.argmin(np.abs(t1-P[1,j]))
        w+=np.concatenate((np.zeros(k-1),w2,np.zeros(len(w)-(k-1+len(w2)))))
    return [t1,w]

def loginterp(M):
    f2=np.zeros((len(M)-1)*2000)
    amp=np.zeros((len(M)-1)*2000)
    for k in np.arange(1,len(M[:,0])):
        f=np.linspace(M[k-1,0],M[k,0],2000)
        f2[(k-1)*2000:k*2000]=f
        amp[(k-1)*2000:k*2000]=np.exp((np.log(M[k,1])-np.log(M[k-1,1]))/(np.log(M[k,0])-np.log(M[k-1,0]))*(np.log(f)-np.log(M[k-1,0]))+np.log(M[k-1,1]))
    return [f2,amp]


#print('Introduzca la Spec SRS como [[frq,Amp],[frq,Amp],[frq,Amp]]:')
#Spec=np.matrix(eval(input()))
#print('Introduzca el factor de calidad Q:')
#Q=np.array(input())
Spec=np.matrix([[100,20],[2000,2850],[10000,2850]])
Spec2=loginterp(Spec)
Q=10
hs=475
P=np.zeros((4,hs))
tim=0.3
Fs=10*np.max(Spec[:,0])
ini = np.log2(np.min(Spec[:,0]))
fin = np.log2(np.max(Spec[:,0]))
j_typ4 = np.linspace(ini,fin,hs)
step_typ4_ = 2**j_typ4
#P=np.zeros((4,len(step_typ4_[np.argmin(np.abs(step_typ4_-np.min(Spec[:,0]))):])))
P[0,:]=-np.sort(-step_typ4_)
#hs=len(P[0,:])
#P[0,:]=-np.sort(-((np.max(Spec[:,0])-np.min(Spec[:,0]))*np.random.random(hs)+np.min(Spec[:,0]))) #frecuencias
P[1,:]=np.sort((tim*3/4)*np.random.random(hs)) #diley
P[2,:]=10*np.random.random(hs) #Amp
P[3,:]=np.sort(np.floor((2*np.min(P[0,:])*tim/4-10)*np.random.random(hs)+10)) #NHS

tol = 1
req = 0
srs_=1
sp=40
dist=np.log(2)*10
while dist > np.log(1.5):
    S=sint(P,tim)
    #SRS
    damp_type4=1/(2*Q)
    freq_typ4=np.arange(0,Fs/2,Fs/len(S[1]))
    ini = np.log2(np.min(Spec[:,0]))
    fin = np.log2(np.max(Spec[:,0]))
    j_typ4 = np.linspace(ini,fin,hs)
    step_typ4 = np.vstack(2**j_typ4)
    freqM=np.matlib.repmat(freq_typ4,len(j_typ4),1)
    stepM=np.matlib.repmat(step_typ4,1,len(freq_typ4))
    H=(stepM**2+1j*2*damp_type4*stepM*freqM)/(stepM**2-freqM**2+1j*2*damp_type4*stepM*freqM)
    H=np.concatenate((H,np.conj(H[:,::-1])),axis=1)
    Y3=np.matlib.repmat(np.fft.fft(S[1]),len(j_typ4),1)*H
    SRS=[step_typ4,np.max(np.abs(np.fft.ifft(Y3,axis=1)),axis=1)]
    sp=[]
    for h in np.arange(0, len(P[0, :])):
        sp.append(Spec2[1][np.argmin(np.abs(Spec2[0]-P[0,h]))])
    P[2, :] = np.array(sp)/SRS[1][::-1] * P[2, :]
#    req=[]
#    res=[]
#    for h in np.arange(0,len(P[0,:])):
#        srs_=SRS[1][np.argmin(np.abs(SRS[0]-P[0,h]))]
#        sp=Spec2[1][np.argmin(np.abs(Spec2[0]-P[0,h]))]
#        if np.abs(np.log(srs_)-np.log(sp))>np.log(1.0000001):
#            P[2,h]=sp/srs_*P[2,h]
#        res.append(srs_)
#        req.append(sp)
    dist=np.max(np.abs(np.array(np.log(SRS[1][::-1]))-np.array(np.log(sp))))
    tol=npl.norm(np.array(SRS[1][::-1])-np.array(sp))/npl.norm(np.array(sp))
    print([dist,tol])

Sf=sint(P,tim)
plt.figure()
plt.xlim([100,10000])
plt.ylim([10,10000])
plt.loglog(SRS[0],SRS[1],label='SRS [G]')
plt.loglog(Spec2[0], Spec2[1],'--r',label='Requerimiento')
plt.loglog(Spec2[0], Spec2[1]*2, '--k')
plt.loglog(Spec2[0], Spec2[1] / 2, '--k')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Aceleracion [G]')
plt.grid()
plt.legend()
plt.figure()
plt.plot(Sf[0],Sf[1],label='Señal obtenida [G]')
plt.xlabel('Tiempo [s]')
plt.ylabel('Aceleracion [G]')
plt.grid()
plt.legend()
Sf2=np.zeros((2,len(Sf[0])))
Sf2[0,:]=Sf[0]
Sf2[1,:]=Sf[1]
np.savetxt('SRS_temp.txt', Sf2.T, delimiter='\t')

plt.show()
