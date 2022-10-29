import matplotlib.pyplot as plt
import time
from instrumental import AFG3021B
from instrumental import TDS1002B
import numpy as np

#osciloscopio
osci = TDS1002B('USB0::0x0699::0x0363::C065089::INSTR')
osci.get_time()
osci.set_time(scale = 1e-3)
osci.set_channel(1,scale = 2)
tiempo, data = osci.read_data(channel = 1)
plt.plot(tiempo,data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')

#generador de funciones
fungen = AFG3021B(name = 'USB0::0x0699::0x0346::C036493::INSTR')
fungen.getFrequency()

#barrido de frecuencia
T=[]
f=[]
plt.figure()
for freq in range(30000,70000,296):
    print(freq)
    f.append(freq)
    fungen.setFrequency(freq)
    time.sleep(0.1)
    tiempo, data = osci.read_data(channel = 2)
    ch2_max=np.max(data)
    tiempo, data = osci.read_data(channel = 1)
    ch1_max=np.max(data)
    T.append(ch2_max/ch1_max)
    plt.plot(f,T)
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Transferencia [V_2/V_1]')
    plt.pause(0.1)
    plt.draw()