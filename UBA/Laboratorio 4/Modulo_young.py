import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as op
from scipy.signal import find_peaks
import time

Cobre_0im=cv2.imread('Cobre_balanza_C.png')
Cobre_0im=Cobre_0im[:,:,2].astype('float64')
Cobre_1im=cv2.imread('Cobre_680mgr_C.png')
Cobre_1im=Cobre_1im[:,:,2].astype('float64')
Cobre_2im=cv2.imread('Cobre_1743mgr_C.png')
Cobre_2im=Cobre_2im[:,:,2].astype('float64')
Cobre_3im=cv2.imread('Cobre_2136mgr_C.png')
Cobre_3im=Cobre_3im[:,:,2].astype('float64')
Cobre_4im=cv2.imread('Cobre_4729_C.png')
Cobre_4im=Cobre_4im[:,:,2].astype('float64')

Acero_0im=cv2.imread('Acero_balanza_C.png')
Acero_0im=Acero_0im[:,:,2].astype('float64')
Acero_1im=cv2.imread('Acero_686mgr_C.png')
Acero_1im=Acero_1im[:,:,2].astype('float64')
Acero_2im=cv2.imread('Acero_1743mgr_C.png')
Acero_2im=Acero_2im[:,:,2].astype('float64')
Acero_3im=cv2.imread('Acero_2136mgr_C.png')
Acero_3im=Acero_3im[:,:,2].astype('float64')
Acero_4im=cv2.imread('Acero_4729_C.png')
Acero_4im=Acero_4im[:,:,2].astype('float64')


y=np.linspace(0,0.065,650)
def graf(im,name,offset):
    c=192
    plt.plot(im[:,c],sorted((y-offset)*1E3,reverse=True),label=name)

def lin(n,a,b):
    return a*n+b


list_im=[]
list_im.append([Cobre_0im,'balanza'])
list_im.append([Cobre_1im,'680 mgr'])
list_im.append([Cobre_2im,'1743 mgr'])
list_im.append([Cobre_3im,'2136 mgr'])
list_im.append([Cobre_4im,'4729 mgr'])

list2_im=[]
list2_im.append([Acero_0im,'balanza'])
list2_im.append([Acero_1im,'686 mgr'])
list2_im.append([Acero_2im,'1743 mgr'])
list2_im.append([Acero_3im,'2136 mgr'])
list2_im.append([Acero_4im,'4729 mgr'])

def graf_all(num):
    for u in range(num):
        fig=plt.figure()
        offset1=0.0291
        fig.add_subplot(1,2,2)
        graf(list_im[u][0],list_im[u][1],offset1)
        plt.ylim([np.min(y-offset1)*1E3,np.max(y-offset1)*1E3])
        plt.grid()
        plt.legend()
        plt.ylabel('Distancia [mm]')
        plt.xlabel('Intencidad R [8-bit Scale]')
        plt.title('Perfil de intencidad')
        fig.add_subplot(1,2,1)
        plt.imshow(list_im[u][0],cmap='gist_heat')
        plt.title('Difraccion con ' + list_im[u][1] + ' del Cobre')

        fig2=plt.figure()
        offset2=0.036
        fig2.add_subplot(1,2,2)
        graf(list2_im[u][0],list2_im[u][1],offset2)
        plt.ylim([np.min(y-offset2)*1E3,np.max(y-offset2)*1E3])
        plt.grid()
        plt.legend()
        plt.ylabel('Distancia [mm]')
        plt.xlabel('Intencidad R [8-bit Scale]')
        plt.title('Perfil de intencidad')
        fig2.add_subplot(1,2,1)
        plt.imshow(list2_im[u][0],cmap='gist_heat')
        plt.title('Difraccion con '+list_im[u][1]+' del Acero')

def ajuste_min(minimos):
    popt, pcov = op.curve_fit(lin, np.arange(len(minimos)), minimos)
    return [popt[0],np.sqrt(pcov[0,0]),popt[1]]


def decai(x,alpha,A):
    return A*np.exp(-x*alpha)

def picos(data):
    data_=np.abs(data.values[:,1]-data.values[:,1].mean())
    ind,_=find_peaks(data_,height=np.max(data_)*0.1,prominence=1, width=20)
    return data.values[ind,:]

graf_all(2)

#Carga manual de los minimos de cada grafico
Yp_cobre=np.zeros((4, 3))
Yp_acero=np.zeros((5, 3))


fig,ax=plt.subplots()
cobre_minim_0=[-0.0229,-0.0154,-0.0077,0,0.0077,0.0152,0.0255,0.0297]
cobre_minim_0-=np.min(cobre_minim_0)
Yp_cobre[0, :]=ajuste_min(cobre_minim_0)
ax.errorbar(np.arange(len(cobre_minim_0)),cobre_minim_0,yerr=0.001,fmt='.')
aj1,=ax.plot(Yp_cobre[0,0]*np.arange(len(cobre_minim_0))+Yp_cobre[0,2])
cobre_minim_1=[-.024,-.0194,-.01418,-.0099,-.005,0,.0048,.0091,.0138,.019,.0234,.0285]
cobre_minim_1-=np.min(cobre_minim_1)
Yp_cobre[1, :]=ajuste_min(cobre_minim_1)
ax.errorbar(np.arange(len(cobre_minim_1)),cobre_minim_1,yerr=0.001,fmt='.')
aj2,=ax.plot(Yp_cobre[1,0]*np.arange(len(cobre_minim_1))+Yp_cobre[1,2])
cobre_minim_2=[-.0213,-.0184,-.0155,-.0122,-.0092,-.006,-.0029,0,.0029,.006,.0091,.0121,.0151,.0185,.0215,.0245,.0275]
cobre_minim_2-=np.min(cobre_minim_2)
Yp_cobre[2, :]=ajuste_min(cobre_minim_2)
ax.errorbar(np.arange(len(cobre_minim_2)),cobre_minim_2,yerr=0.001,fmt='.')
aj3,=ax.plot(Yp_cobre[2,0]*np.arange(len(cobre_minim_2))+Yp_cobre[2,2])
cobre_minim_3=[-.019,-.0164,-.0136,-.0107,-.0081,-.0056,-.003,0,.0027,.0057,.0082,.0109,.0137,.0163,.0191,.0217,.0246,.0274,.0298]
cobre_minim_3-=np.min(cobre_minim_3)
Yp_cobre[3, :]=ajuste_min(cobre_minim_3)
ax.errorbar(np.arange(len(cobre_minim_3)),cobre_minim_3,yerr=0.001,fmt='.')
aj4,=ax.plot(Yp_cobre[3,0]*np.arange(len(cobre_minim_3))+Yp_cobre[3,2])
ax.legend([aj1,aj2,aj3,aj4],[f'{0} mgr',f'{680} mgr',f'{1743} mgr',f'{2136} mgr'],fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax.set_xlabel('Numero de minimo',fontsize=14)
ax.set_ylabel('Distancia de minimos',fontsize=14)
plt.title('Distribucion de minimos para el Cobre')
plt.xlim([0,18])
plt.ylim([0,0.06])
plt.grid()

fig2,ax2=plt.subplots()
acero_minim_0=[-0.0342,-0.0272,-0.0182,-0.0095,0,0.0091,0.0181,0.0276]
acero_minim_0-=np.min(acero_minim_0)
Yp_acero[0, :]=ajuste_min(acero_minim_0)
ax2.errorbar(np.arange(len(acero_minim_0)),acero_minim_0,yerr=0.001,fmt='.')
aj1_,=ax2.plot(Yp_acero[0,0]*np.arange(len(acero_minim_0))+Yp_acero[0,2])
acero_minim_1=[-.0293,-.0221,-.0146,-.0076,0,.0074,.0146,.0215]
acero_minim_1-=np.min(acero_minim_1)
Yp_acero[1, :]=ajuste_min(acero_minim_1)
ax2.errorbar(np.arange(len(acero_minim_1)),acero_minim_1,yerr=0.001,fmt='.')
aj2_,=ax2.plot(Yp_acero[1,0]*np.arange(len(acero_minim_1))+Yp_acero[1,2])
acero_minim_2=[-.0229,-.0179,-.0117,-.0062,0,.0055,.0114,.0168,.0227]
acero_minim_2-=np.min(acero_minim_2)
Yp_acero[2, :]=ajuste_min(acero_minim_2)
ax2.errorbar(np.arange(len(acero_minim_2)),acero_minim_2,yerr=0.001,fmt='.')
aj3_,=ax2.plot(Yp_acero[2,0]*np.arange(len(acero_minim_2))+Yp_acero[2,2])
acero_minim_3=[-.0313,-.0265,-.0214,-.0163,-.0109,-.0056,0,.0052,.0105,.0158,.0207]
acero_minim_3-=np.min(acero_minim_3)
Yp_acero[3, :]=ajuste_min(acero_minim_3)
ax2.errorbar(np.arange(len(acero_minim_3)),acero_minim_3,yerr=0.001,fmt='.')
aj4_,=ax2.plot(Yp_acero[3,0]*np.arange(len(acero_minim_3))+Yp_acero[3,2])
acero_minim_4=[-.0253,-.0221,-.0186,-.015,-.0117,-.0076,-.0038,0,.0033,.0069,.0104,.0141,.0181,.0218,.0254]
acero_minim_4-=np.min(acero_minim_4)
Yp_acero[4, :]=ajuste_min(acero_minim_4)
ax2.errorbar(np.arange(len(acero_minim_4)),acero_minim_4,yerr=0.001,fmt='.')
aj5_,=ax2.plot(Yp_acero[4,0]*np.arange(len(acero_minim_4))+Yp_acero[4,2])
ax2.legend([aj1_,aj2_,aj3_,aj4_,aj5_],[f'{0} mgr',f'{680} mgr',f'{1743} mgr',f'{2136} mgr',f'{4729} mgr'],fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
ax2.set_xlabel('Numero de minimo',fontsize=14)
ax2.set_ylabel('Distancia de minimos',fontsize=14)
plt.title('Distribucion de minimos para el Acero')
plt.xlim([0,14])
plt.ylim([0,0.065])
plt.grid()

#Calculo de h con propagacion de errores
h_cobre=np.zeros((len(Yp_cobre[:,0]),2))
h_acero=np.zeros((len(Yp_acero[:,0]),2))
h_cobre[:,0]=1.494 * 670E-9 / Yp_cobre[:, 0]
h_cobre[:,1]=10*np.sqrt((670E-9 / Yp_cobre[:, 0]*0.001)**2+(1.494 * 670E-9 / Yp_cobre[:, 0]**2*Yp_cobre[:, 1])**2)
h_acero[:,0]=1.494 * 670E-9 / Yp_acero[:, 0]
h_acero[:,1]=10*np.sqrt((670E-9 / Yp_acero[:, 0]*0.001)**2+(1.494 * 670E-9 / Yp_acero[:, 0]**2*Yp_acero[:, 1])**2)
#h_cobre[-1,1]=h_cobre[-1,1]/5


pesas_cobre=np.zeros((4,2))
pesas_acero=np.zeros((5,2))
pesas_cobre[:,0]=(np.array([0,0.00068,0.001743,0.002136])+0.013979)*9.807
pesas_cobre[:,1]=2*np.ones((4,))*0.00001*9.807
pesas_acero[:,0]=(np.array([0,0.000686,0.001743,0.002136,0.004729])+0.013979)*9.807
pesas_acero[:,1]=2*np.ones((5,))*0.00001*9.807


plt.figure()
plt.errorbar(pesas_cobre[:,0], h_cobre[:,0]*1E6,xerr=pesas_cobre[:,1],yerr=h_cobre[:,1]*1E6, fmt='s', label='Defleccion Cobre $h_c$')
plt.errorbar(pesas_acero[:,0], h_acero[:,0]*1E6,xerr=pesas_acero[:,1],yerr=h_acero[:,1]*1E6, fmt='d', label='Defleccion Acero $h_a$')
plt.ylabel('Apertura h [$\mu m$]',fontsize=14)
plt.xlabel('Fuerza [$N$]',fontsize=14)
cob_coef=np.polyfit(pesas_cobre[:,0], h_cobre[:,0], 1,full=True)
ace_coef=np.polyfit(pesas_acero[:,0], h_acero[:,0], 1,full=True)
E_cobre=np.zeros((2,))
E_acero=np.zeros((2,))
E_cobre[0]=32*(0.5*0.468**2-0.468**3/3)/(np.pi*(0.005**4))/cob_coef[0][0]
E_cobre[1]=np.sqrt((32*(0.468**2)/(np.pi*(0.005**4))/cob_coef[0][0]*0.001)**2+
                   (32*(0.5*0.468*2-0.468**2)/(np.pi*(0.005**4))/cob_coef[0][0]*0.001)**2+
                   (32*(0.5*0.468**2-0.468**3/3)/(np.pi*(0.005**5))/cob_coef[0][0]*4*0.00002)**2+
                   (32*(0.5*0.468**2-0.468**3/3)/(np.pi*(0.005**4))/cob_coef[0][0]**2*np.sqrt(cob_coef[1]/len(cob_coef[0])))**2)
E_acero[0]=32*(0.52*0.464**2-0.464**3/3)/(np.pi*(0.00573**4))/ace_coef[0][0]
E_acero[1]=np.sqrt((32*(0.464**2)/(np.pi*(0.00573**4))/ace_coef[0][0]*0.001)**2+
                   (32*(0.52*0.464*2-0.464**2)/(np.pi*(0.00573**4))/ace_coef[0][0]*0.001)**2+
                   (32*(0.52*0.464**2-0.464**3/3)/(np.pi*(0.00573**5))/ace_coef[0][0]*4*0.00002)**2+
                   (32*(0.52*0.464**2-0.464**3/3)/(np.pi*(0.00573**4))/ace_coef[0][0]**2*np.sqrt(ace_coef[1]/len(ace_coef[0])))**2)
print(' ')
print('::::::::RESULTADOS ESTATICO::::::::')
print('RESULTADOS DE DIFRACCION DEL COBRE:')
print('-----------------------------------')
print('Carga [N]\tApertura [m]')
print(f'{pesas_cobre[0,0]:.3E}+-{pesas_cobre[0,1]:.0E}\t{h_cobre[0,0]:.3E}+-{h_cobre[0,1]:.0E}')
print(f'{pesas_cobre[1,0]:.3E}+-{pesas_cobre[1,1]:.0E}\t{h_cobre[1,0]:.3E}+-{h_cobre[1,1]:.0E}')
print(f'{pesas_cobre[2,0]:.3E}+-{pesas_cobre[2,1]:.0E}\t{h_cobre[2,0]:.3E}+-{h_cobre[2,1]:.0E}')
print(f'{pesas_cobre[3,0]:.3E}+-{pesas_cobre[3,1]:.0E}\t{h_cobre[3,0]:.3E}+-{h_cobre[3,1]:.0E}')
print(' ')
print('RESULTADOS DE DIFRACCION DEL ACERO:')
print('-----------------------------------')
print('Carga [N]\tApertura [m]')
print(f'{pesas_acero[0,0]:.3E}+-{pesas_acero[0,1]:.0E}\t{h_acero[0,0]:.3E}+-{h_acero[0,1]:.0E}')
print(f'{pesas_acero[1,0]:.3E}+-{pesas_acero[1,1]:.0E}\t{h_acero[1,0]:.3E}+-{h_acero[1,1]:.0E}')
print(f'{pesas_acero[2,0]:.3E}+-{pesas_acero[2,1]:.0E}\t{h_acero[2,0]:.3E}+-{h_acero[2,1]:.0E}')
print(f'{pesas_acero[3,0]:.3E}+-{pesas_acero[3,1]:.0E}\t{h_acero[3,0]:.3E}+-{h_acero[3,1]:.0E}')
print(f'{pesas_acero[4,0]:.3E}+-{pesas_acero[4,1]:.0E}\t{h_acero[4,0]:.3E}+-{h_acero[4,1]:.0E}')
print(' ')
print(f'E_c = ({E_cobre[0]/1E9:.3G} +- {E_cobre[1]/1E9:.0G}) GPa')
print(f'E_a = ({E_acero[0]/1E9:.3G} +- {E_acero[1]/1E9:.0G}) GPa')
print(' ')
plt.plot(pesas_cobre[:,0],(cob_coef[0][0]*pesas_cobre[:,0]+cob_coef[0][1])*1E6,label=f'Ajuste Cobre')
plt.plot(pesas_acero[:,0],(ace_coef[0][0]*pesas_acero[:,0]+ace_coef[0][1])*1E6,label=f'Ajuste Acero')
plt.legend(fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()

# Metodo Dinamico

temp3_c=pd.read_csv('temp3_cobre.txt',delimiter=' ')
temp4_c=pd.read_csv('temp4_cobre.txt',delimiter=' ')
temp3_a=pd.read_csv('temp3_acero.txt',delimiter=' ')
temp4_a=pd.read_csv('temp4_acero.txt',delimiter=' ')

L_c,L_a=0.498,0.494
K_c=np.array([1.875,4.694,7.855])/L_c
K_c_=np.array([1.875,4.694,7.855])/L_c**2*0.001
K_a=np.array([1.875,4.694,7.855])/L_a
K_a_=np.array([1.875,4.694,7.855])/L_a**2*0.001

L_C,L_A=0.50,0.52
d_c,d_a=4.83E-3,5.55E-3
I_c,I_a=np.pi*d_c**4/64,np.pi*d_a**4/64
I_c_,I_a_=4*np.pi*d_c**3/64*0.025E-3,4*np.pi*d_a**3/64*0.025E-3
rho_c,rho_a=0.082025/L_C,0.119013/L_A
rho_c_,rho_a_=0.082025/L_C**2*0.001,0.119013/L_A**2*0.001

f_c,f_a=9.09,14.98

popt_c,pcov_c=op.curve_fit(decai,picos(temp4_c)[:,0],np.abs(picos(temp4_c)[:,1]-picos(temp4_c)[:,1].mean()))
alpha_c=np.array([popt_c[0],np.sqrt(pcov_c[0,0])])
popt_a,pcov_a=op.curve_fit(decai,picos(temp3_a)[:,0],np.abs(picos(temp3_a)[:,1]-picos(temp3_a)[:,1].mean()))
alpha_a=np.array([popt_a[0],np.sqrt(pcov_a[0,0])])

#plt.figure()
#plt.plot(picos(temp4_c)[:,0],np.abs(picos(temp4_c)[:,1]-picos(temp4_c)[:,1].mean()),'.')
#plt.plot(picos(temp4_c)[:,0],decai(picos(temp4_c)[:,0],popt_c[0],popt_c[1]))
#plt.plot(picos(temp4_a)[:,0],np.abs(picos(temp4_a)[:,1]-picos(temp4_a)[:,1].mean()),'.')
#plt.plot(picos(temp4_a)[:,0],decai(picos(temp4_a)[:,0],popt_a[0],popt_a[1]))

df=1/(temp4_c.values[1,0]-temp4_c.values[0,0])/temp4_c.values.shape[0]
E_c=((2*np.pi*f_c)**2+alpha_c[0]**(-2))*rho_c/(I_c*K_c**4)*1E-9
E_c_=np.sqrt((4*np.pi*f_c*rho_c/(I_c*K_c**4)*df)**2
             +(rho_c/(I_c*K_c**4)*2*alpha_c[0]**(-3)*alpha_c[1])**2
             +(((2*np.pi*f_c)**2+alpha_c[0]**(-2))*1/(I_c*K_c**4)*rho_c_)**2
             +(((2*np.pi*f_c)**2+alpha_c[0]**(-2))*rho_c/(I_c**2*K_c**4)*I_c_)**2
             +(((2*np.pi*f_c)**2+alpha_c[0]**(-2))*rho_c/(I_c*K_c**5)*4*K_c_)**2)*1E-9
E_a=((2*np.pi*f_a)**2+alpha_a[0]**(-2))*rho_a/(I_a*K_a**4)*1E-9
E_a_=np.sqrt((4*np.pi*f_a*rho_a/(I_a*K_a**4)*df)**2
             +(rho_a/(I_a*K_a**4)*2*alpha_a[0]**(-3)*alpha_a[1])**2
             +(((2*np.pi*f_a)**2+alpha_a[0]**(-2))*1/(I_a*K_a**4)*rho_a_)**2
             +(((2*np.pi*f_a)**2+alpha_a[0]**(-2))*rho_a/(I_a**2*K_a**4)*I_a_)**2
             +(((2*np.pi*f_a)**2+alpha_a[0]**(-2))*rho_a/(I_a*K_a**5)*4*K_a_)**2)*1E-9



#linealidad
Lin_=[138,135,126,110,94,84.1,76.5,65.7,52]
linGillete=np.linspace(10.5,4.5,9)


plt.figure()
plt.errorbar(linGillete,np.array(Lin_)/100,yerr=320E-3/2,fmt='s')
popt_LIN,pcov_LIN=op.curve_fit(lin,linGillete,np.array(Lin_)/100)
plt.plot(linGillete,(popt_LIN[0]*linGillete+popt_LIN[1]),label='Ajuste')
plt.ylabel('Tension [mV]',fontsize=14)
plt.xlabel('Desplazamiento [mm]',fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.grid()

print(' ')
print('::::::::RESULTADOS DINAMICO::::::::')
print('LINEALIDAD TENSION-DESPLAZAMIENTO:')
print('---------------------------------')
print(f'Cte de calibracion: ({popt_LIN[0]:.3G}+-{np.sqrt(pcov_LIN[0,0]):.0G}) mV/mm')
print('FRECUENCIAS:')
print('------------')
print(f'1er Modo Cobre: {f_c:.3G} +- {df:.3G} Hz')
print(f'1er Modo Acero: {f_a:.3G} +- {df:.3G} Hz')
print('DECAIMIENTO ALPHA:')
print('------------------')
print(f'alpha_c: ({alpha_c[0]:.3G} +- {alpha_c[1]:.0G}) s^-1')
print(f'alpha_a: ({alpha_a[0]:.3G} +- {alpha_a[1]:.0G}) s^-1')
print(' ')
print('MODULOS DE YOUNG:')
print(f'E_c: ({E_c[0]:.3G} +- {E_c_[0]:.0G}) GPa')
print(f'E_a: ({E_a[0]:.3G} +- {E_a_[0]:.0G}) GPa')

plt.figure()
desp1=(temp4_c.values[:,1]-temp4_c.values[:,1].mean())/popt_LIN[0]
desp2=(temp3_a.values[:,1]-temp3_a.values[:,1].mean())/popt_LIN[0]
plt.plot(temp4_c.values[:,0],desp1,label='Cobre')
plt.plot(temp3_a.values[:,0],desp2,label='Acero')
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Desplazamiento [mm]',fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.xlim([0,10])
plt.grid()


plt.figure()
freq=np.linspace(0,1/(temp4_c.values[1,0]-temp4_c.values[0,0]),temp4_c.values.shape[0])
fft_c4=np.abs(np.fft.fft(desp1))/temp4_c.values.shape[0]*np.sqrt(2)
plt.semilogx(freq,fft_c4,label='Cobre')
plt.annotate(f'{f_c:.3G} Hz',xy=(f_c,7.5),xytext=(f_c,8.2),arrowprops=dict(arrowstyle="->"),fontsize=12)
freq=np.linspace(0,1/(temp3_a.values[1,0]-temp3_a.values[0,0]),temp3_a.values.shape[0])
fft_a3=np.abs(np.fft.fft(desp2))/temp3_a.values.shape[0]*np.sqrt(2)
plt.semilogx(freq,fft_a3,label='Acero')
plt.annotate(f'{f_a:.3G} Hz',xy=(f_a,5.52),xytext=(f_a,6.02),arrowprops=dict(arrowstyle="->"),fontsize=12)



plt.xlabel('Frecuencia [Hz]',fontsize=14)
plt.ylabel('Desplazamiento 0-pk [mm]',fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.ylim([0,9])
plt.xlim([1,500])
plt.grid()
plt.legend(fontsize=12)
plt.show()
