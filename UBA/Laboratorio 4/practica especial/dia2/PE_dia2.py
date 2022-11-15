# -*- coding: utf-8 -*-
import pyvisa as visa
import numpy as np
import time
import matplotlib.pyplot as plt

# inicializo comunicacion con equipos
rm = visa.ResourceManager()
#lista de dispositivos conectados, para ver las id de los equipos
rm.list_resources()

#inicializo generador de funciones
fungen = rm.open_resource('USB0::0x0699::0x0346::C034198::INSTR')
#le pregunto su identidad
fungen.query('*IDN?')
#le pregunto la freq
fungen.query('FREQ?')
#le seteo la freq
fungen.write('FREQ 2000')
fungen.query('FREQ?')
#le pregunto la amplitud
fungen.query('VOLT?')
#le seteo la amplitud
fungen.write('VOLT 2')
fungen.query('VOLT?')
#le pregunto si la salida esta habilitada
fungen.query('OUTPut1:STATe?')
#habilito la salida
fungen.write('OUTPut1:STATe 1')
fungen.query('OUTPut1:STATe?')
#le pregunto la impedancia de carga seteada
fungen.query('OUTPUT1:IMPEDANCE?')



#inicializo el osciloscopio
osci = rm.open_resource('USB0::0x0699::0x0363::C102223::INSTR')
#le pregunto su identidad
osci.query('*IDN?')
#le pregunto la conf del canal (1|2)
osci.query('CH1?')
#le pregunto la conf horizontal
osci.query('HOR?')
#le pregunto la punta de osciloscopio seteada
osci.query('CH2:PRObe?')


#Seteo de canal
channel=1
scale = 5
osci.write("CH{0}:SCA {1}".format(channel, scale))
osci.query("CH{0}:SCA?".format(channel))
"""escalas Voltaje (V) ojo estas listas no son completas
2e-3
5e-3
10e-3
20e-3
50e-3
100e-3
5e-2
10e-2
"""

zero = 0
osci.write("CH{0}:POS {1}".format(channel, zero))
osci.query("CH{0}:POS?".format(channel))

channel=2
scale = 2e-1
osci.write("CH{0}:SCA {1}".format(channel, scale))
osci.write("CH{0}:POS {1}".format(channel, zero))

#seteo escala horizontal
scale = 200e-6
osci.write("HOR:SCA {0}".format(scale))
osci.write("HOR:POS {0}".format(zero))	
osci.query("HOR?")
"""
escalas temporales (s)

10e-9
25e-9
50e-9
100e-9
250e-9
500e-9
1e-6
2e-6
5e-6
10e-6
25e-6
50e-6

"""


#le pido los valores de la pantalla (0:255)
data = osci.query_binary_values('CURV?', datatype='B',container=np.array)
plt.plot(data)

#le pido los parametros de la pantalla
xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';') 
xze
xin
#voltaje = (data - yoff) * ymu + yze 
#tiempo = xze + np.arange(len(data)) * xin



# Conexion usando clases
from instrumental import AFG3021B
from instrumental import TDS1002B

#osciloscopio
osci = TDS1002B('USB0::0x0699::0x0363::C108011::INSTR')
osci.get_time()
osci.set_time(scale = 1e-3)
osci.set_channel(1,scale = 2)
tiempo, data = osci.read_data(channel = 1)
plt.plot(tiempo,data)
plt.xlabel('Tiempo [s]')
plt.ylabel('Voltaje [V]')

#generador de funciones
fungen = AFG3021B(name = 'USB0::0x0699::0x0346::C036492::INSTR')
fungen.getFrequency()

#barrido de frecuencia
for freq in range(150,800,5):
    print(freq)
    fungen.setFrequency(freq)
    time.sleep(0.1)
    osci.set_time(scale = 1/freq/6)
    tiempo, data = osci.read_data(channel = 1)
    datos=np.c_[tiempo,data]
    np.savetxt(f'barrido_{freq}Hz_2Vpp.txt',datos)
    plt.plot(tiempo,data)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Voltaje [V]')
    plt.draw()
	

#Ejemplo comunicacion Multiplexor Difusividad térmica
from instrumental import Agilent34970A
mux = Agilent34970A('GPIB0::9::INSTR')
data,temp,tim,chan = mux.one_scan()
print(tim)
print(temp)
print(chan)

#Ejemplo comunicacion Amprobe38XR-A
from instrumental import Amporobe38XRA
mult = Amporobe38XRA('COM1')
value,Ylab=mult.GetValue(verbose=True)
print(value,Ylab)
value,Ylab=mult.GetValue(verbose=True)
print(value,Ylab)
mult.close()

# NI-DAQmx Python Documentation: https://nidaqmx-python.readthedocs.io/en/latest/index.html
# NI USB-621x User Manual: https://www.ni.com/pdf/manuals/371931f.pdf
import matplotlib.pyplot as plt
import numpy as np
import nidaqmx
import time


#para saber el ID de la placa conectada (DevX)
system = nidaqmx.system.System.local()
for device in system.devices:
    print(device)

#para setear (y preguntar) el modo y rango de un canal analógico
with nidaqmx.Task() as task:
    ai_channel = task.ai_channels.add_ai_voltage_chan("Dev6/ai1", max_val=1,min_val=-1)
    print(ai_channel.ai_term_cfg)    
    print(ai_channel.ai_max)
    print(ai_channel.ai_min)	
	

## Medicion por tiempo/samples de una sola vez
def medicion_una_vez(duracion, fs):
    cant_puntos = int(duracion*fs)
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.BAL_DIFF
        task.ai_channels.add_ai_voltage_chan("Dev6/ai1", terminal_config = modo, 
                                             max_val=1, min_val=-1)
               
        task.timing.cfg_samp_clk_timing(fs,samps_per_chan = cant_puntos,
                                        sample_mode = nidaqmx.constants.AcquisitionType.FINITE)
        
        datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
    datos = np.asarray(datos)    
    t = np.linspace(0,duracion, cant_puntos)
    return datos, t

duracion = 5 #segundos
fs = 250000 #Frecuencia de muestreo
y, t = medicion_una_vez(duracion, fs)

plt.plot(y)
plt.grid()
plt.show()

#%%
## Medicion continua
def medicion_continua(duracion, fs):
    cant_puntos = int(duracion*fs)
    with nidaqmx.Task() as task:
        modo= nidaqmx.constants.TerminalConfiguration.DIFF
        task.ai_channels.add_ai_voltage_chan("Dev5/ai1", terminal_config = modo)
        task.timing.cfg_samp_clk_timing(fs, sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS)
        task.start()
        t0 = time.time()
        total = 0
        while total<cant_puntos:
            time.sleep(0.1)
            datos = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)           
            total = total + len(datos)
            t1 = time.time()
            print("%2.3fs %d %d %2.3f" % (t1-t0, len(datos), total, total/(t1-t0)))            

fs = 250000 #Frecuencia de muestreo
duracion = 10 #segundos
medicion_continua(duracion, fs)