import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter,filtfilt,welch
from scipy import optimize as op

S1=pd.read_csv('senal_1.txt',delimiter=' ')
S2=pd.read_csv('senal_2.txt',delimiter=' ')
camp_52k=pd.read_csv('campana_1er_modo.txt')
lockin1=pd.read_csv('lockin_1_400mV_piezo_modo_50k.txt')
lockin1_f=np.linspace(50064,50104,160)+12
lockin2=pd.read_csv('lockin_2_400mV_piezo_modo_50k.txt')
lockin2_f=np.linspace(50264,50304,160)+12
signal_imp=pd.read_csv('signal_impulso.txt')
time_imp=pd.read_csv('time_impulso.txt')
fft_y2_imp=pd.read_csv('fft_y2_impulso.txt')
f_imp=pd.read_csv('frecuencia_impulso.txt')

#MODELO
def rlc_amp(f,R,L,C):
    Z = R + 1j * (2 * np.pi * f * L - 1 / (2 * np.pi * f * C))
    T = 9.81E3 / (9.81E3 + Z)
    return np.abs(T)

def rlc_pha(f,R,L,C):
    Z=R+1j*(2*np.pi*f*L-1/(2*np.pi*f*C))
    T=9.81E3/(9.81E3+Z)
    return np.angle(T)*180/np.pi

def rlc2_amp(f,R,L,C,C2):
    Z1 = R + 1j * (2 * np.pi * f * L - 1 / (2 * np.pi * f * C))
    Z2=-1j/(2*np.pi*f*C2)
    Z=Z1*Z2/(Z1+Z2)
    T = 9.81E3 / (9.81E3 + Z)
    return np.abs(T)

def rlc2_pha(f,R,L,C,C2):
    Z1 = R + 1j * (2 * np.pi * f * L - 1 / (2 * np.pi * f * C))
    Z2 = -1j / (2 * np.pi * f * C2)
    Z = Z1 * Z2 / (Z1 + Z2)
    T=9.81E3/(9.81E3+Z)
    return np.angle(T)*180/np.pi

def caract(R,L,C):
    Q=np.sqrt(L/C)/(R+9.81E3)
    Bw=(Q*np.sqrt(L*C))**(-1)/(2*np.pi)
    return Q, Bw


def r2(f_real,f_ajust):
    r_2=1-np.sum((f_real-f_ajust)**2)/np.sum((f_real-np.mean(f_real))**2)
    return r_2

#plt.plot(S1.values[:,0],S1.values[:,1],label='medicion 1')
#plt.plot(S2.values[:,0],S2.values[:,1],label='medicion 2')
#plt.xlabel('Tiempo [s]')
#plt.ylabel('Voltaje [V]')
#plt.xlim([0,4])
#plt.legend()
#plt.grid()

#Estimacion previa de parametros
R=9.81E3*(1-0.472)/0.472
L=R/(2*np.pi*3)
C=(2*np.pi*3)/(R*(2*np.pi*50096)**2)
C2=1/((2*np.pi*50295.88)**2*L-1/C)
step=(np.max(lockin1_f)-np.min(lockin1_f))/len(lockin1_f)
tam=(np.max(lockin2_f)-np.min(lockin1_f))/step
frec=np.linspace(np.min(lockin1_f),np.max(lockin2_f),int(tam))
frec2=np.linspace(np.min(lockin1_f)-150,np.max(lockin2_f)+150,int(tam))
res_antires=np.interp(frec,np.concatenate((lockin1_f,lockin2_f)),
                      np.concatenate((lockin1.values[:, 0],lockin2.values[:,0])))
res_antires_pha=np.interp(frec,np.concatenate((lockin1_f,lockin2_f)),
                      np.concatenate((lockin1.values[:, 1]+25,lockin2.values[:,1]+25)))
interv_NaN=np.abs(frec-(np.max(lockin1_f)+np.min(lockin2_f))/2)<(np.min(lockin2_f)-np.max(lockin1_f))/2
res_antires[interv_NaN]=np.NaN
res_antires_pha[interv_NaN]=np.NaN
#plt.figure()
#plt.semilogy(frec,res_antires,'.')
#plt.show()
# Ajuste
popt1, pcov1 = op.curve_fit(rlc2_amp, frec,res_antires,[R,L,C,C2],check_finite=False)
ajust0_amp = rlc2_amp(frec2, popt1[0], popt1[1], popt1[2], popt1[3])
ajust0_pha = rlc2_pha(frec2, popt1[0], popt1[1], popt1[2], popt1[3])
ajust1_amp = rlc2_amp(lockin1_f, popt1[0], popt1[1], popt1[2], popt1[3])
ajust2_amp = rlc2_amp(lockin2_f, popt1[0], popt1[1], popt1[2], popt1[3])
ajust1_pha = rlc2_pha(lockin1_f, popt1[0], popt1[1], popt1[2], popt1[3])
ajust2_pha = rlc2_pha(lockin2_f, popt1[0], popt1[1], popt1[2], popt1[3])
print('Parametros iniciales estimados')
print([R,L,C,C2])
print('Ajuste al modelo RLCC_2')
print(f'R^2 Amp= {r2(lockin1.values[:,0],ajust1_amp)}')
print(f'R^2 Pha= {r2(lockin1.values[:,1]+25,ajust1_pha)}')
print(f'R: {popt1[0]}+-{np.sqrt(pcov1[0,0])}')
print(f'L: {popt1[1]}+-{np.sqrt(pcov1[1,1])}')
print(f'C: {popt1[2]}+-{np.sqrt(pcov1[2,2])}')
print(f'C2: {popt1[3]}+-{np.sqrt(pcov1[3,3])}')
Q,Bw=caract(popt1[0],popt1[1],popt1[2])
print(f'Q: {Q}')
print(f'Ancho: {Bw} Hz')

fig,ax=plt.subplots(2,1)
ax[0].semilogy(camp_52k.values[:,0],camp_52k.values[:,1],'o',label='Osciloscopio')
ax[0].semilogy(frec,res_antires,'.',label='Lockin')
ax[0].semilogy(frec2,ajust0_amp,label=r'Modelo $RLCC_2$')
ax[0].legend(fontsize=14)
ax[0].set_ylabel('Transferencia',fontsize=14)
ax[0].set_xlim([np.min(frec2),np.max(frec2)])
ax[0].set_title('Resonancia y Anti-resonancia',fontsize=14)
ax[1].plot(frec,res_antires_pha,'.',color='tab:orange',label='Fase con lockin')
ax[1].plot(frec2,ajust0_pha,'-g',label='Modelo RLC')
ax[1].set_ylabel('Fase [Deg]',fontsize=14)
ax[1].set_xlabel('Frecuencia [Hz]',fontsize=14)
ax[1].set_xlim([np.min(frec2),np.max(frec2)])
ax[0].grid()
ax[1].grid()

# Ajuste2
#popt2, pcov2 = op.curve_fit(rlc2_amp, lockin2_f, lockin2.values[:, 0],[R,L,C,C2])
#ajust2_amp = rlc2_amp(lockin1_f, popt2[0], popt2[1], popt2[2], popt2[3])
#ajust2_pha = rlc2_pha(lockin1_f, popt2[0], popt2[1], popt2[2], popt2[3])
#print()
#print('Ajuste Anti-Resonancia')
#print(f'R^2 Amp= {r2(lockin2.values[:,0],ajust2_amp)}')
#print(f'R^2 Pha= {r2(lockin2.values[:,1]+25,ajust2_pha)}')
#print(f'R: {popt2[0]}+-{np.sqrt(pcov2[0,0])}')
#print(f'L: {popt2[1]}+-{np.sqrt(pcov2[1,1])}')
#print(f'C: {popt2[2]}+-{np.sqrt(pcov2[2,2])}')
#print(f'C2: {popt2[3]}+-{np.sqrt(pcov2[3,3])}')


fig2,ax2=plt.subplots(2,2)
ax2[0,0].semilogy(camp_52k.values[:,0],camp_52k.values[:,1],'o',label='Osciloscopio')
ax2[0,0].semilogy(frec,res_antires,'.',label='Lockin')
ax2[0,0].semilogy(frec2,ajust0_amp,label=r'Modelo $RLCC_2$')
ax2[0,0].legend(fontsize=10)
ax2[0,0].set_ylabel('Transferencia',fontsize=14)
ax2[0,0].set_xlim([np.min(lockin1_f),np.max(lockin1_f)])
ax2[0,0].set_ylim([0.04,0.78])
ax2[0,0].set_title('Resonancia',fontsize=14)
ax2[0,0].grid()
ax2[0,1].semilogy(frec,res_antires,'.',color='tab:orange',label='Lockin')
ax2[0,1].semilogy(frec2,ajust0_amp,'-g',label=r'Modelo $RLCC_2$')
ax2[0,1].legend(fontsize=10)
ax2[0,1].set_xlim([np.min(lockin2_f),np.max(lockin2_f)])
ax2[0,1].set_ylim([2E-5,1E-3])
ax2[0,1].set_title('Anti-esonancia',fontsize=14)
ax2[0,1].grid()
ax2[1,0].plot(frec,res_antires_pha,'.',color='tab:orange',label='Fase con lockin')
ax2[1,0].plot(frec2,ajust0_pha,'-g',label='Modelo RLC')
ax2[1,0].set_ylabel('Fase [Deg]',fontsize=14)
ax2[1,0].set_xlabel('Frecuencia [Hz]',fontsize=14)
ax2[1,0].set_xlim([np.min(lockin1_f),np.max(lockin1_f)])
ax2[1,0].grid()
ax2[1,1].plot(frec,res_antires_pha,'.',color='tab:orange',label='Fase con lockin')
ax2[1,1].plot(frec2,ajust0_pha,'-g',label='Modelo RLC')
ax2[1,1].set_xlabel('Frecuencia [Hz]',fontsize=14)
ax2[1,1].set_xlim([np.min(lockin2_f),np.max(lockin2_f)])
ax2[1,1].grid()

def butter_bandpass_filter(data, band, fs, order):
    nyq = 0.5 * fs  # Nyquist Frequency
    normal_band = np.array(band) / nyq
    # Get the filter coefficients
    b, a = butter(order, normal_band, btype='bandpass', analog=False)
    y = filtfilt(b, a, data)
    return y

signal_imp_filt=butter_bandpass_filter(signal_imp.values[:,0],[40096,60096],250000,5)
fig3,ax3=plt.subplots(2,1)
ax3[0].plot(time_imp.values[:,0],signal_imp.values[:,0]-signal_imp.values[:,0].mean(),label=r'Salida $V_2$')
ax3[0].plot(time_imp.values[:,0],signal_imp_filt,label='Pasa Banda aplicado \nde 40 a 60 kHz')
ax3[0].set_title('Respuesta ante un impulso de 1 Hz con Duty Cycle ultra corto',fontsize=14)
ax3[0].legend(fontsize=10)
ax3[0].set_xlabel('Tiempo [s]',fontsize=14)
ax3[0].set_ylabel('Voltaje [V]',fontsize=14)
ax3[0].set_xlim([0,10])
ax3[0].grid()
freq,y=welch(signal_imp_filt,250000,nperseg=2*250000,noverlap=int(50/100*2*250000),scaling='spectrum')
ax3[1].plot(freq,np.sqrt(2*y),label='$\Delta$f: 0,5 Hz\nPromedios: 19\nOverlap: 50%\nVentana:Hanning')
ax3[1].set_xlabel('Frecuencia [Hz]',fontsize=14)
ax3[1].set_xlim([49750,50500])
ax3[1].set_ylim([0,2.7E-7])
ax3[1].set_ylabel('Voltaje [V]',fontsize=14)
ax3[1].legend(fontsize=10)
ax3[1].grid()

y1=np.fft.fft(S1.values[:-1,1])
y2=np.fft.fft(S2.values[:-1,1])
freq=250000*np.linspace(0,1,len(y2))
plt.figure()
plt.loglog(freq[:int(len(freq)/2)]+2.1,np.abs(y1[:int(len(freq)/2)])/len(freq)*2,label='Exitando con cuadrada de fr/3')
plt.loglog(freq[:int(len(freq)/2)]-1.1,np.abs(y2[:int(len(freq)/2)])/len(freq)*2,label='Exitando con cuadrada de fr/6')
#plt.annotate(r'$1/3\omega_s$',xy=(50096/3,0.009),xytext=(16698,0.05),arrowprops=dict(arrowstyle="->"))
#plt.annotate(r'$1/6\omega_s$',xy=(50096/6,0.0001),xytext=(50096/6+200,0.002),arrowprops=dict(arrowstyle="->"))
plt.annotate(r'$\omega_s$',xy=(50096,0.3),xytext=(66000,0.1),arrowprops=dict(arrowstyle="->"))
plt.title('Respuesta en frecuencia ante un tren de pulsos\n de 1/3 y 1/6 de la frecuencia de resonancia',fontsize=14)
plt.xlabel('Frecuencia [Hz]',fontsize=14)
plt.xlim([30000,80000])
#plt.xlim([15086,50106])
#plt.ylim([0,0.3])
plt.ylabel('Voltaje [V]',fontsize=14)
plt.legend(fontsize=14)
plt.grid()
plt.show()

plt.figure()
plt.plot()