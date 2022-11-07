# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:08:40 2022

@author: Publico
"""

import SR830
import matplotlib.pyplot as plt
import nidaqmx
from instrumental import AFG3021B
import numpy as np


#generador de funciones
fungen = AFG3021B(name = 'USB0::0x0699::0x0346::C036492::INSTR')
fungen.getFrequency()

#barrido de frecuencia
T=[]
f=[]
p=[]
fig,ax=plt.subplots(2,1)
L=SR830.SR830('GPIB0::8::INSTR')
file=open('lockin_2_400mV_piezo_modo_50k.txt','w')
file.write('AMP_VRMS, phase \n')
for freq in np.linspace(50264,50304,160):
    f.append(freq)
    fungen.setFrequency(freq)
    gen_amp=400/(2*np.sqrt(2)*1000)
    L.auto_scale()
    med=L.get_medicion(isXY=False)
    print([freq,med[0]])
    T.append(med[0]/gen_amp)
    p.append(med[1])
    file.write(f'{T[-1]}, {p[-1]} \n')
    ax[0].semilogy(f,T,'.b',label='Transferencia')
    ax[0].set_ylabel('Transferencia [V_lockin/V_gen]')
    ax[1].plot(f,np.array(p),'.r',label='Fase')
    ax[1].set_xlabel('Frecuencia [Hz]')
    ax[1].set_ylabel('Fase [DEG]')
    plt.pause(0.1)
    plt.draw()

file.close()

#para saber el ID de la placa conectada (DevX)
system = nidaqmx.system.System.local()
for device in system.devices:
    print(device)

#para setear (y preguntar) el modo y rango de un canal analógico
with nidaqmx.Task() as task:
    ai_channel = task.ai_channels.add_ai_voltage_chan("Dev5/ai1", max_val=1,min_val=-1)
    print(ai_channel.ai_term_cfg)    
    print(ai_channel.ai_max)
    print(ai_channel.ai_min)	
	

## Medicion por tiempo/samples de una sola vez
def medicion_una_vez(duracion, fs):
    cant_puntos = int(duracion*fs)
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.DIFF
        #modo= nidaqmx.constants.TerminalConfiguration.RSE
        ai_channel=task.ai_channels.add_ai_voltage_chan("Dev5/ai2", terminal_config = modo, 
                                             max_val=.001, min_val=-.001)
        
        print(ai_channel.ai_term_cfg)    
        print(ai_channel.ai_max)
        print(ai_channel.ai_min)	
	        
        task.timing.cfg_samp_clk_timing(fs,samps_per_chan = cant_puntos,
                                        sample_mode = nidaqmx.constants.AcquisitionType.FINITE)
        
        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    datos = np.asarray(datos)    
    t = np.linspace(0, duracion, cant_puntos)
    return datos, t

duracion = 10 #segundos
fs = 250000 #Frecuencia de muestreo
y, t = medicion_una_vez(duracion, fs)

plt.figure()
plt.plot(t,y)

f=np.linspace(0,250000/2,int(250000*8/2))
fft_y=np.abs(np.fft.fft(y))
fft_y2=fft_y[:len(f)]
#fft_y3=fft_y2*f

plt.figure()
plt.semilogy(f,fft_y[:len(f)])
np.savetxt('frecuencia_impulso.txt',f)
np.savetxt('fft_y2_impulso.txt',fft_y2)
np.savetxt('signal_impulso.txt',y)
np.savetxt('time_impulso.txt',t)



