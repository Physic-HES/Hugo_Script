import numpy as np
import pandas as pd
import scipy.signal as S
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy import optimize as op
from PIL import Image


def sin_mod(t,a,phi,f):
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


def grafic2():
    for j in range(3):
        plt.figure(figsize=(10,6))
        f,t,Sxx=S.spectrogram(datos[j][:,1],1/(datos[j][1,0]-datos[j][0,0]),window='hann',nperseg=2*75,
                              noverlap=int(95/100*2*75),scaling='spectrum')
        plt.pcolormesh(t*1000,f/1000,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)))
        plt.axis('off')
        plt.savefig(f'spectrogram_{j}.png')
        plt.axis('on')
        plt.ylabel('Frecuencia [kHz]')
        plt.xlabel('Tiempo [ms]')
        Sxx2= np.asarray(Image.open(f'spectrogram_{j}.png').convert('L'))
        Sxx2=Sxx2[72:533,125:899]
        Sxx2=np.abs(Sxx2-255)
        lamb=632E-9
        ind=np.argmax(Sxx2,axis=0)
        plt.figure()
        f2=np.linspace(0,np.max(f),Sxx2.shape[0])
        t2=np.linspace(np.min(t),np.max(t),Sxx2.shape[1])
        plt.plot(t2*1000,f2[len(f2)-1-ind]*lamb/2*1000,'.r',label=f'Maximos $\lambda f$')
        plt.xlim([np.min(t*1000),np.max(t*1000)])
        plt.xlabel(r'Tiempo [$ms$]')
        plt.grid()
        plt.ylabel(r'Velocidad [$mm/s$]')
        if j==0:
            popt1, pcov1 = op.curve_fit(sin_mod, t2,f2[len(f2)-1-ind]*lamb/2*1000,[5,1,635])
        elif j==1:
            popt1, pcov1 = op.curve_fit(sin_mod, t2, f2[len(f2)-1-ind] * lamb / 2 * 1000, [5, 1, 736])
        elif j==2:
            popt1, pcov1 = op.curve_fit(sin_mod, t2, f2[len(f2)-1-ind] * lamb / 2 * 1000, [5, 1, 150])
        t2=np.linspace(0,np.max(t),1000)
        Y=sin_mod(t2,popt1[0],popt1[1],popt1[2])
        plt.plot(t2*1000,Y,label=r'Ajuste $|vel|$')
        plt.plot(t2*1000,popt1[0]*np.sin(2*np.pi*popt1[2]*t2+popt1[1]),'g',label='Velocidad')
        tiem=datos[j][:,0]-np.min(datos[j][:,0])
        plt.legend()
        plt.subplots(3,1)
        plt.subplot(311)
        plt.title(arch_d[j])
        plt.plot(tiem*1000,datos[j][:,1]*1000,label='Fotodiodo')
        plt.legend()
        plt.ylabel(r'Voltaje [$mV$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        vel=popt1[0]*np.sin(2*np.pi*popt1[2]*tiem+popt1[1])
        plt.subplot(312)
        plt.plot(tiem*1000,vel,'g',label='Velocidad')
        plt.ylabel(r'Velocidad [$mm/s$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        plt.subplot(313)
        plt.plot(tiem*1000,1E3*(np.cumsum(vel)*tiem[1]-(np.cumsum(vel)*tiem[1]).mean()),'m',label='Desplazamiento')
        plt.ylabel(r'Desplazamiento [$\mu m$]')
        plt.xlabel(r'Tiempo [$ms$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
    plt.show()

#grafic()
grafic2()
#print(datos[1][:,1])
#plt.figure(datos[1][:,0],np.unwrap(datos[1][:,1]))

def resp(datos):
    frec=150
    vel_desp=[]
    for j in range(len(datos)):
        plt.figure(figsize=(10,6))
        f,t,Sxx=S.spectrogram(datos[j][:,1],1/(datos[j][1,0]-datos[j][0,0]),window='hann',nperseg=2*100,
                              noverlap=int(95/100*2*100),scaling='spectrum')
        plt.pcolormesh(t*1000,f/1000,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)))
        #plt.axis('off')
        #plt.axis('on')
        plt.ylabel(r'Frecuencia [$kHz$]')
        plt.xlabel(r'Tiempo [$ms$]')
        #plt.savefig(f'Barrido_caracterizacion/2Vpp_{frec}Hz.png')
        Sxx2 = np.asarray(Image.open(f'Barrido_caracterizacion/2Vpp_{frec}Hz.png').convert('L'))
        Sxx2 = Sxx2[72:533, 126:899]
        Sxx2 = np.abs(Sxx2 - 255)
        lamb=632E-9
        ind=np.argmax(Sxx2,axis=0)
        f2 = np.linspace(0, np.max(f), Sxx2.shape[0])
        t2 = np.linspace(np.min(t), np.max(t), Sxx2.shape[1])
        plt.close()
        plt.figure()
        plt.plot(t2 * 1000, f2[len(f2) - 1 - ind] * lamb / 2 * 1000, '.r', label=f'Maximos $\lambda f$')
        plt.xlim([np.min(t*1000),np.max(t*1000)])
        plt.xlabel(r'Tiempo [$ms$]')
        plt.grid()
        plt.ylabel(r'Velocidad [$mm/s$]')
        popt1, pcov1 = op.curve_fit(lambda x, a,phi: sin_mod(t2,a,phi,frec), t2,f2[len(f2) - 1 - ind]*lamb/2*1000,[4,np.pi/2])
        t2=np.linspace(0,np.max(t),1000)
        Y=sin_mod(t2,popt1[0],popt1[1],frec)
        plt.plot(t2*1000,Y,label=r'Ajuste $|vel|$')
        plt.plot(t2*1000,popt1[0]*np.sin(2*np.pi*frec*t2+popt1[1]),'g',label='Velocidad')
        tiem=datos[j][:,0]-np.min(datos[j][:,0])
        plt.legend()
        plt.savefig(f'Barrido_caracterizacion/Ajuste_2Vpp_{frec}Hz.png')
        plt.close()
        plt.subplots(3,1)
        plt.subplot(311)
        plt.title(f'Excitando con 2Vpp a {frec} Hz')
        plt.plot(tiem*1000,datos[j][:,1]*1000,label='Fotodiodo')
        plt.legend()
        plt.ylabel(r'Voltaje [$mV$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        vel=popt1[0]*np.sin(2*np.pi*frec*tiem+popt1[1])
        plt.subplot(312)
        plt.plot(tiem*1000,vel,'g',label='Velocidad')
        plt.ylabel(r'Velocidad [$mm/s$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        plt.subplot(313)
        desp=1E3*(np.cumsum(vel)*tiem[1]-(np.cumsum(vel)*tiem[1]).mean())
        plt.plot(tiem*1000,desp,'m',label='Desplazamiento')
        plt.ylabel(r'Desplazamiento [$\mu m$]')
        plt.xlabel(r'Tiempo [$ms$]')
        plt.xlim([np.min(tiem*1000),np.max(tiem*1000)])
        plt.grid()
        plt.savefig(f'Barrido_caracterizacion/Vel_desp_2Vpp_{frec}Hz.png')
        plt.close()
        print(f'Frecuencia {frec} Hz procesada')
        frec+=5
        vel_desp.append(np.c_[tiem*1000,vel,desp])
    return vel_desp

#plt.show()
datos2=[]
for j in range(150,800,5):
    dat=pd.read_csv(f'/home/hp1opticaiamend/PycharmProjects/Hugo_Script/UBA/Laboratorio 4/practica especial/Barrido_caracterizacion/barrido_{j}Hz_2Vpp.txt',delimiter=' ',header=None)
    datos2.append(dat.values)

#vel_desp=resp(datos2)
#f=range(150,800,5)
#pk=[]
#for k in range(len(f)):
#    pk.append(np.max(np.max(vel_desp[k][:,1])))

#plt.plot(f,pk)
#plt.plot(f,pk,'.')
#plt.ylabel(r'Desplazamiento 0-pk [$\mu m$]')
#plt.xlabel('Frecuencia [Hz]')
#plt.grid()
#plt.show()

#escalon2V=pd.read_csv('dia2/Escalon_250mHz_2V.txt',delimiter=' ',header=None)
#f,t,Sxx=S.spectrogram(escalon2V.values[:,1],1/(escalon2V.values[1,0]-escalon2V.values[0,0]),window='hann',nperseg=2*1800,
#                              noverlap=int(50/100*2*1800),scaling='spectrum')
#plt.pcolormesh(t,f/1000,Sxx,shading='gouraud',norm=LogNorm(vmin=np.max(Sxx)/1E5, vmax=np.max(Sxx)/10),cmap='jet')
#plt.ylim([0,30])

#fotodiodo_costado=pd.read_csv('fotodiofo_costado.txt',header=None,delimiter=' ')
#path_escalon3v='/home/hp1opticaiamend/PycharmProjects/Hugo_Script/UBA/Laboratorio 4/practica especial/dia2/Escalon_250mHz_3V.txt'
#escalon_3V=pd.read_csv(path_escalon3v,header=None,delimiter=' ')
#rango_golpe=range(int(3.8136*2.5E5),int(3.8987*2.5E5))
#golpe=escalon_3V.values[rango_golpe,:]

def peak_pro(golpe):
    plt.plot(golpe[:,0],golpe[:,1])
    peak_up,_=S.find_peaks(golpe[:,1],prominence=0.023,width=5E-5)
    peak_dawn,_=S.find_peaks(-golpe[:,1],prominence=0.023,width=5E-5)
    print(peak_up.shape)
    print(peak_dawn.shape)
    plt.plot(golpe[peak_up,0],golpe[peak_up,1],'.')
    plt.plot(golpe[peak_dawn,0],golpe[peak_dawn,1],'.')
    plt.figure()
    plt.plot(peak_up,'.')
    plt.plot(peak_dawn,'.')
    vel=632E-9/4/(golpe[peak_up,0]-golpe[peak_dawn,0])
    plt.figure()
    plt.plot((golpe[peak_up,0]-golpe[peak_dawn,0])/2+golpe[peak_dawn,0],vel)
    plt.show()

#path_doppler150hz_t='/home/hp1opticaiamend/PycharmProjects/Hugo_Script/UBA/Laboratorio 4/practica especial/tiempo2_doppler_150Hz_2Vpp'
#path_doppler150hz_d='/home/hp1opticaiamend/PycharmProjects/Hugo_Script/UBA/Laboratorio 4/practica especial/datos_doppler_635Hz_2Vpp'
#doppler150hz_t=pd.read_csv(path_doppler150hz_t,header=None)
#doppler150hz_d=pd.read_csv(path_doppler150hz_d,header=None)
#datos_dia1_150Hz=np.c_[doppler150hz_t,doppler150hz_d]
#peak_pro(datos_dia1_150Hz)
