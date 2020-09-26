import numpy as np
print('Introduzca la Spec SRS como [[frq,Amp],[frq,Amp],[frq,Amp]]:')
Spec=input()
print('Introduzca el factor de calidad Q:')
Q=input()
P=np.zeros(20,4)
P[:,0]=np.max(Spec[:,1])*np.random.random((27,1)) #frecuencias
P[:,1]=0.25*np.random.random((27,1)) #diley
P[:,2]=30*np.random.random((27,1)) #Amp
P[:,3]=round(75*np.random.random((27,1))) #NHS
# Sintesis de señal
def sint(P):
    w=np.zeros((np.max(P[:,0])*0.3,1))
    for j in range(len(P[:,0])):
        t=np.zeros((len(np.arange(P[j,1],P[j,1]+P[j,3]/(2*P[j,0]),1/np.max(Spec[:,0]))),1))
        t[:,0]=np.arange(P[j,1],P[j,1]+P[j,3]/(2*P[j,0]),1/np.max(Spec[:,0]))
        w1=np.zeros((len(np.arange(0,P[j,1],1/np.max(Spec[:,0]))),1))
        w2=P[j,2]*np.sin(2*np.pi*P[j,0]/P[j,3]*(t-P[j,1]))*np.sin(2*np.pi*P[j,0]*(t-P[j,1]))
        w3=np.zeros((len(np.arange(P[j,1]+P[j,3]/(2*P[j,0]),0.3,1/np.max(Spec[:,0]))),1))
        w+=[w1,w2,w3]
    return w
