import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy import signal as S
import scipy as scp
from tqdm import tqdm
root = tk.Tk()


def imp_test():
    # Permite seleccionar un archivo exel que tenga una columna con una lista de RECs y
    # otra columna que contenga la lista de canales que corresponden a esos RECs
    # return:
    # Una lista de dos lugares, el primero corresponde a los RECs y el segundo a los canales
    folder_selected = filedialog.askdirectory()
    tk.mainloop()
    arch1 = os.listdir(path=folder_selected)
    h=1
    print('[%2.0f] ' % (h) + arch1[0][0:7])
    arch2=[arch1[0][0:7]]
    for j in range(1,len(arch1)-1):
        if arch1[j][0:7]!=arch1[j-1][0:7]:
            h+=1
            print('[%2.0f] ' % (h) + arch1[j][0:7])
            arch2.append(arch1[j][0:7])
    lis=np.array(eval(input('Seleccione una lista de RECs: '))) - 1
    datos=[]
    head=16
    Dat=[]
    for sel in range(len(lis)):
        pbar = tqdm(total=len(arch1), desc=r'Buscando e importando datos de %s'%arch2[lis[sel]])
        for k in range(len(arch1)):
            if arch1[k][0:7]==arch2[lis[sel]]:
                datframe = pd.read_csv(folder_selected + '/' + arch1[k], delimiter='\t', header=head)
                if len(datos)>0:
                    datos.append(datframe.values[:,1])
                else:
                    datos.append(datframe.values[:,0])
                    datos.append(datframe.values[:, 1])
            pbar.update(1)
        Dat.append(datos)
        datos=[]
        pbar.close()
    return Dat,arch2

def maximos(recs,arch2):
    df=pd.DataFrame()
    for j in range(len(recs)):
        max1=[]
        for k in range(1,9):
            delta=(np.max(recs[j][k])-np.min(recs[j][k]))/2
            max1.append(delta)
        df[arch2[j]]=max1
    df.to_excel('C:/Users/hugui/Documents/EDM_dami/Maximos.xlsx')
    print(df)
    return df

def casc(recs,arch2,lineas,overl,Vmax):
    for j in range(len(recs)):
        fs=1/(recs[j][0][1]-recs[j][0][0])
        B=int(2*lineas)
        ov=int(overl/100*B)
        f, t, Sxx = S.spectrogram(recs[j][2], fs,
                          window='hann', nperseg=B,
                          noverlap=ov, scaling='spectrum')
        if Vmax == 0:
            Vmax1 = np.max(Sxx)
        elif Vmax > 0:
            Vmax1 = Vmax
        Vmin1 = Vmax1 / 1E5
        plt.figure(figsize=(10,5))
        plt.pcolormesh(t, f, Sxx,
                       shading='gouraud',
                       norm=LogNorm(vmin=Vmin1, vmax=Vmax1))
        plt.xlabel('Tiempo [seg]')
        plt.ylabel('Frecuencia [Hz]')
        plt.title([arch2[j]+r'_Ch%02.0f'%2])
        plt.savefig('C:/Users/hugui/Documents/EDM_dami/Casc_'+arch2[j]+'Ch02.png')

