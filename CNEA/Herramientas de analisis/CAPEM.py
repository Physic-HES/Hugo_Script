import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd

dat2018=[]
vec=[]
ruta='C:/Users/Yo/Documents/C/Users/Toshiba3/Documents/HUGO/Servicios EECE/CAPEM/APS/txt/'
m=155
pbar = tqdm(total=12, desc='Importando datos...')
for c in np.arange(1,13):
    archivo=r'REC0%g_PA_APS(ch%g)'%(m,c)
    imp_dat2018=pd.read_csv(ruta+archivo+'.txt', delimiter='\t',header=24)
    cols = imp_dat2018.values
    if c == 1:
        vec.append(cols[:,0])
        vec.append(cols[:,1])
    if c > 1:
        vec.append(cols[:,1])
    pbar.update(1)
pbar.close()
dat2018.append(vec)

dat2020=[]
vec=[]
ruta='C:/Users/Yo/Documents/C/Users/Toshiba3/Documents/HUGO/Servicios EECE/CAPEM/med2020/APS/txt/'
m=402
ch=np.arange(1,11)
ch=np.delete(ch,5)
pbar = tqdm(total=9, desc='Importando datos...')
for c in ch:
    archivo=r'REC0%g_PA_APS(ch%g)'%(m,c)
    imp_dat2018=pd.read_csv(ruta+archivo+'.txt', delimiter='\t',header=24)
    cols = imp_dat2018.values
    if c == 1:
        vec.append(cols[:,0])
        vec.append(cols[:,1])
    if c > 1:
        vec.append(cols[:,1])
    pbar.update(1)
pbar.close()
dat2020.append(vec)

orden2018=np.array([2,3,4,5,6])
orden2020=np.array([1,3,5,2,4])
leg=['Axial','Vertical lado bomba','Horizontal lado bomba','Vertical lado motor','Horizontal lado motor']
for j in np.arange(0,5):
    plt.figure(1)
    plt.plot(dat2018[0][0],1000*dat2018[0][orden2018[j]], label=leg[j]+' 2018')
    plt.figure(2)
    plt.plot(dat2020[0][0], 1000*dat2020[0][orden2020[j]], label=leg[j] + ' 2020')

plt.figure(1)
plt.xlim([0,1000])
plt.ylim([0,0.6])
plt.ylabel('Velocidad [mm/s] 0-pk')
plt.xlabel('Frecuencia [Hz]')
plt.grid()
plt.legend()

plt.figure(2)
plt.xlim([0,1000])
plt.ylim([0,1.6])
plt.ylabel('Velocidad [mm/s] 0-pk')
plt.xlabel('Frecuencia [Hz]')
plt.grid()
plt.legend()
plt.show()
