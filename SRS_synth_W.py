import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from scipy import linalg as npl

# Sintesis de señal
def sint(P):
    w=np.zeros(np.int(np.floor(Fs*0.3)))
    for j in range(len(P[0,:])-1):
        t=np.arange(P[1,j],P[1,j]+P[3,j]/(2*P[0,j]),1/Fs)
        w2=P[2,j]*np.sin(2*np.pi*P[0,j]/P[3,j]*(t-P[1,j]))*np.sin(2*np.pi*P[0,j]*(t-P[1,j]))
        k=np.int(np.floor(P[1,j]*Fs))
        if len(w)-(k+len(w2))>0:
            w+=np.concatenate((np.zeros(k),w2,np.zeros(len(w)-(k+len(w2)))))
    t1=np.linspace(0,0.3,len(w))
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
print(Spec2[0])
Q=10
hs=675
P=np.zeros((4,hs))
Fs=4*np.max(Spec[:,0])
P[0,:]=-np.sort(-((np.max(Spec[:,0])-np.min(Spec[:,0]))*np.random.random(hs)+np.min(Spec[:,0]))) #frecuencias
P[1,:]=np.sort(0.28*np.random.random(hs)) #diley
P[2,:]=10*np.random.random(hs) #Amp
P[3,:]=-np.sort(-np.floor((575-3)*np.random.random(hs)+3)) #NHS
tol = 1
req = 0
srs_=1
sp=40
while tol > 0.03:
    S=sint(P)
    #SRS
    damp_type4=1/(2*Q)
    freq_typ4=np.arange(0,Fs/2,Fs/len(S[1]))
    k_typ4 = np.log2(Fs/2)*np.e
    j_typ4 = np.arange(0,k_typ4)
    step_typ4 = np.vstack(2**(j_typ4/np.e))
    freqM=np.matlib.repmat(freq_typ4,len(j_typ4),1)
    stepM=np.matlib.repmat(step_typ4,1,len(freq_typ4))
    H=(stepM**2+1j*2*damp_type4*stepM*freqM)/(stepM**2-freqM**2+1j*2*damp_type4*stepM*freqM)
    H=np.concatenate((H,np.conj(H[:,::-1])),axis=1)
    Y3=np.matlib.repmat(np.fft.fft(S[1]),len(j_typ4),1)*H
    SRS=[step_typ4,np.max(np.abs(np.fft.ifft(Y3,axis=1)),axis=1)]
    req=[]
    res=[]
    for h in np.arange(1,len(P[0,:])):
        srs_=SRS[1][np.argmin(np.abs(SRS[0]-P[0,h]))]
        sp=Spec2[1][np.argmin(np.abs(Spec2[0]-P[0,h]))]
        if srs_<sp-sp/40:
            P[2,h]=sp/srs_*P[2,h]
        if srs_>sp+sp/40:
            P[2,h]=sp/srs_*P[2,h]
        res.append(srs_)
        req.append(sp)
    tol=npl.norm(np.array(res)-np.array(req))/npl.norm(np.array(req))
    print(tol)

Sf=sint(P)
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
