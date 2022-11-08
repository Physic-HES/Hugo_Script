import numpy as np
import pandas as pd
import scipy.signal as S
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy import optimize as op


def sin_mod(t,a,f,phi):
    return np.abs(a*np.sin(2*np.pi*f*t+phi))


arch_t=['tiempo_doppler','tiempo2_doppler_736Hz_2Vpp','tiempo2_doppler_150Hz_2Vpp']

arch_d=['datos_doppler_635Hz_2Vpp','datos2_doppler_736Hz_2Vpp','datos2_doppler_150Hz_2Vpp']
datos=[]
for j in range(3):
    t1=pd.read_csv(arch_t[j],header=None)
    d1=pd.read_csv(arch_d[j],header=None)
    datos.append(np.c_[t1,d1])

def grafic():
    for j in range(3):
        plt.figure()
        f,t,Sxx=S.spectrogram(datos[j][:,1],1/(datos[j][1,0]-datos[j][0,0]),window='hann',nperseg=2*75,
                              noverlap=int(95/100*2*75),scaling='spectrum')
        plt.subplot2grid((3,2),(0,0),rowspan=2)
        plt.pcolormesh(t*1000,f/1000,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)),cmap='jet')
        plt.ylabel(r'Frecuencia [$kHz$]')
        lamb=632E-9
        ind=np.argmax(Sxx,axis=0)
        plt.subplot2grid((3,2),(2,0),rowspan=1)
        plt.plot(t*1000,f[ind]*lamb/2*1000,'.r',label=f'Maximos $\lambda f$')
        plt.xlim([np.min(t*1000),np.max(t*1000)])
        plt.xlabel(r'Tiempo [$ms$]')
        plt.grid()
        plt.ylabel(r'Velocidad [$mm/s$]')
        if j==0:
            popt1, pcov1 = op.curve_fit(sin_mod, t,f[ind]*lamb/2*1000,[5,635,1])
        elif j==1:
            popt1, pcov1 = op.curve_fit(sin_mod, t, f[ind] * lamb / 2 * 1000, [5, 736, 1])
        elif j==2:
            popt1, pcov1 = op.curve_fit(sin_mod, t, f[ind] * lamb / 2 * 1000, [5, 150, 1])
        t2=np.linspace(0,np.max(t),1000)
        Y=sin_mod(t2,popt1[0],popt1[1],popt1[2])
        plt.plot(t2*1000,Y,label=r'Ajuste $|vel|$')
        plt.plot(t2*1000,popt1[0]*np.sin(2*np.pi*popt1[1]*t2+popt1[2]),'g',label='Velocidad')
        tiem=datos[j][:,0]-np.min(datos[j][:,0])
        plt.legend()
        plt.subplot2grid((3,2),(0,1),rowspan=1)
        plt.title(arch_d[j])
        plt.plot(tiem*1000,datos[j][:,1]*1000,label='Fotodiodo')
        plt.legend()
        plt.ylabel(r'Voltaje [$mV$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        vel=popt1[0]*np.sin(2*np.pi*popt1[1]*tiem+popt1[2])
        plt.subplot2grid((3,2),(1,1),rowspan=1)
        plt.plot(tiem*1000,vel,'g',label='Velocidad')
        plt.ylabel(r'Velocidad [$mm/s$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        plt.subplot2grid((3,2),(2,1),rowspan=1)
        plt.plot(tiem*1000,1E3*(np.cumsum(vel)*tiem[1]-(np.cumsum(vel)*tiem[1]).mean()),'m',label='Desplazamiento')
        plt.ylabel(r'Desplazamiento [$\mu m$]')
        plt.xlabel(r'Tiempo [$ms$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()


#grafic()
#print(datos[1][:,1])
#plt.figure(datos[1][:,0],np.unwrap(datos[1][:,1]))

def resp(datos):
    frec=150
    velocidad=[]
    for j in range(len(datos)):
        plt.figure()
        f,t,Sxx=S.spectrogram(datos[j][:,1],1/(datos[j][1,0]-datos[j][0,0]),window='hann',nperseg=2*75,
                              noverlap=int(95/100*2*75),scaling='spectrum')
        plt.subplot2grid((3,2),(0,0),rowspan=2)
        plt.pcolormesh(t*1000,f/1000,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)),cmap='jet')
        plt.ylabel(r'Frecuencia [$kHz$]')
        lamb=632E-9
        ind=np.argmax(Sxx,axis=0)
        plt.subplot2grid((3,2),(2,0),rowspan=1)
        plt.plot(t*1000,f[ind]*lamb/2*1000,'.r',label=f'Maximos $\lambda f$')
        plt.xlim([np.min(t*1000),np.max(t*1000)])
        plt.xlabel(r'Tiempo [$ms$]')
        plt.grid()
        plt.ylabel(r'Velocidad [$mm/s$]')
        popt1, pcov1 = op.curve_fit(sin_mod, t,f[ind]*lamb/2*1000,[5,frec,1])
        t2=np.linspace(0,np.max(t),1000)
        Y=sin_mod(t2,popt1[0],popt1[1],popt1[2])
        plt.plot(t2*1000,Y,label=r'Ajuste $|vel|$')
        plt.plot(t2*1000,popt1[0]*np.sin(2*np.pi*popt1[1]*t2+popt1[2]),'g',label='Velocidad')
        tiem=datos[j][:,0]-np.min(datos[j][:,0])
        plt.legend()
        plt.subplot2grid((3,2),(0,1),rowspan=1)
        plt.title(f'Excitando con 2Vpp a {frec} Hz')
        plt.plot(tiem*1000,datos[j][:,1]*1000,label='Fotodiodo')
        plt.legend()
        plt.ylabel(r'Voltaje [$mV$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        vel=popt1[0]*np.sin(2*np.pi*popt1[1]*tiem+popt1[2])
        plt.subplot2grid((3,2),(1,1),rowspan=1)
        plt.plot(tiem*1000,vel,'g',label='Velocidad')
        plt.ylabel(r'Velocidad [$mm/s$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        plt.subplot2grid((3,2),(2,1),rowspan=1)
        plt.plot(tiem*1000,1E3*(np.cumsum(vel)*tiem[1]-(np.cumsum(vel)*tiem[1]).mean()),'m',label='Desplazamiento')
        plt.ylabel(r'Desplazamiento [$\mu m$]')
        plt.xlabel(r'Tiempo [$ms$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        #plt.savefig(f'Barrido_caracterizacion/2Vpp_{frec}Hz.png')
        plt.close()
        frec+=5
        velocidad.append(np.c_[tiem*1000,vel])
    return velocidad

#plt.show()
#datos2=[]
#for j in range(150,800,5):
#    dat=pd.read_csv(f'/home/hp1opticaiamend/PycharmProjects/Hugo_Script/UBA/Laboratorio 4/practica especial/Barrido_caracterizacion/barrido_{j}Hz_2Vpp.txt',delimiter=' ',header=None)
#    datos2.append(dat.values)

#velo=resp(datos2)
#f=range(150,800,5)
#vel_pk=[]
#for k in range(len(f)):
#    vel_pk.append(np.sqrt(2)*np.std(velo[k][:,1]))

#plt.plot(f,vel_pk)
#plt.ylabel('Velocidad 0-pk [mm/s]')
#plt.xlabel('Frecuencia [Hz]')
#plt.grid()
#plt.show()

escalon2V=pd.read_csv('dia2/Escalon_250mHz_2V.txt',delimiter=' ',header=None)
f,t,Sxx=S.spectrogram(escalon2V.values[:,1],1/(escalon2V.values[1,0]-escalon2V.values[0,0]),window='hann',nperseg=2*1800,
                              noverlap=int(50/100*2*1800),scaling='spectrum')
plt.pcolormesh(t,f/1000,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)/10),cmap='jet')
plt.ylim([0,30])
plt.show()
