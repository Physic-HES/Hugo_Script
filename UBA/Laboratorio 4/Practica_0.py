import time
import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
from instrumental import AFG3021B
from instrumental import TDS1002B

rm = visa.ResourceManager()
lista=rm.list_resources()

if len(lista)>0:
    for j in range(len(lista)):
        instr=visa.ResourceManager().open_resource(lista[j])
        name=instr.query('*IDN?')
        rm.close()
        if 'TDS' in name:
            osci = TDS1002B(lista[j])
            print('Osciloscopio conectado')
        elif 'AFG' in name:
            fungen = AFG3021B(lista[j])
            print('Generador conectado')
        else:
            print('No coinciden con los instrumentos del labo')
    Ok=True
else:
    print('No hay nada conectado')
    Ok=False

if Ok:
    freq=np.linspace(2,100,25)
    T0=[]
    T1=[]
    T2=[]
    ind=0
    for f in freq:
        fungen.setFrequency(f)
        osci.set_time(1/f)
        time.sleep(20 / f)
        dat_1=osci.read_data(1)
        dat_2=osci.read_data(2)
        fft_dat1 = np.fft.fft(dat_1[1])
        fft_dat2 = np.fft.fft(dat_2[1])
        T_=fft_dat1/fft_dat2
        T_=T_[0:int(len(T_)/2)]
        T_amp=np.max(np.abs(fft_dat1))/np.max(np.abs(fft_dat2))
        T_fase=np.angle(T_[np.argmax(np.abs(T_[10:]))])
        T0.append(f)
        T1.append(T_amp)
        T2.append(T_fase)
        ind+=1
    plt.subplot(2, 1, 1)
    plt.plot(T0[0:ind], T1[0:ind])
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Coeficiente de transferencia')
    plt.title('Filtro pasa alto C=47 nF R=10 kOhm')
    plt.subplot(2, 1, 2)
    plt.plot(T0[0:ind], T2[0:ind])
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Diferencia de fase')
    plt.show()



