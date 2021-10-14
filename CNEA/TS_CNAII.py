import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


folder_selected='C:/Users/Yo/Documents/Hugo/TS_atuchaII'
arch=['SubidaTS04_20210728.txt','BajadaTS04_20210728.txt','SubidaTS35_20210728.txt','BajadaTS35_20210728.txt',
      'Subida_TS04_20210731.txt','Subida_TS35_20210731.txt',
      'VerificacionTS04_20210728.txt','VerificacionTS35_20210728.txt',
      'Verificacion_TS04_20210731.txt','Verificacion_TS35_20210731.txt']
head=38
dat=[]
tit=['Subida TS04 CONUAR','Bajada TS04 CONUAR','Subida TS35 CONUAR','Bajada TS35 CONUAR',
      'Subida TS04 Piletas CNAII','Subida TS35 Piletas CNAII',
      'Verificacion TS04 CONUAR','Verificacion TS35 CONUAR',
      'Verificacion TS04 Piletas CNAII','Verificacion TS35 Piletas CNAII']
sg=['SGZ1_000','SGZ1_045','SGZ1_090',
     'SGZ2_000','SGZ2_045','SGZ2_090',
     'SGZ3_000','SGZ3_090']
tubo=['TS04','TS35']
zonas=['Zona 1','Zona 2','Zona 3']

ord=np.array([[0,1,2,3,4,5,6,7],#Subida TS04 CONUAR
              [0,1,2,3,4,5,6,7],#Bajada TS04 CONUAR
              [0,1,2,3,4,5,6,7],#Subida TS35 CONUAR
              [0,1,2,3,4,5,6,7],#Bajada TS35 CONUAR
              [5,2,4,3,1,6,7,0],#Subida TS04 Piletas CNAII
              [0,1,2,3,4,5,6,7],#Subida TS35 Piletas CNAII
              [0,1,2,3,4,5,6,7],#Verificacion TS04 CONUAR
              [0,1,2,3,4,5,6,7],#Verificacion TS35 CONUAR
              [5,2,4,3,1,6,7,0],#Verificacion TS04 Piletas CNAII
              [0,1,2,3,4,5,6,7]])#Verificacion TS35 Piletas CNAII


for k in range(len(arch)):
    datframe=pd.read_csv(folder_selected+'/'+arch[k],delimiter='\t', header=head)
    dat.append(datframe.values)

M=np.zeros([10,9])
for j in range(10):
    M[j,:]=np.max(np.abs(dat[j][:, 1:]), 0)

Mw=np.zeros([10,9])
for j in range(10):
    Mw[j,:]=np.argmax(np.abs(dat[j][:, 1:]), 0)

Ms=np.zeros([10,9])
for j in range(10):
    for k in range(len(dat[j][0,1:])-1):
        Ms[j,k]=np.abs(dat[j][int(Mw[j,k]),k+1])/dat[j][int(Mw[j,k]),k+1]

Max_Strain=M*Ms
Max_Strain[4,:]=Max_Strain[4,[5,2,4,3,1,6,7,0,8]]
Max_Strain[8,:]=Max_Strain[8,[5,2,4,3,1,6,7,0,8]]

np.savetxt('Max_Strain.txt',Max_Strain,fmt='%4.3f',delimiter='\t')

for k in range(len(arch)):
    for j in range(len(dat[k][0,1:])-1):
        if j<3:
            plt.figure(1+3*k)
            plt.title(zonas[0] + ' ' + tit[k])
        elif np.abs(j-4)<=1:
            plt.figure(2+3*k)
            plt.title(zonas[1] + ' ' + tit[k])
        elif j>5:
            plt.figure(3+3*k)
            plt.title(zonas[2] + ' ' + tit[k])
        plt.plot(dat[k][:,0],dat[k][:,ord[k,j]+1],label=sg[j])
        plt.text(dat[k][int(Mw[k,ord[k,j]]),0],dat[k][int(Mw[k,ord[k,j]]),ord[k,j]+1],'%4.2f'%dat[k][int(Mw[k,ord[k,j]]),ord[k,j]+1])
        plt.grid('on')
        plt.xlabel('Tiempo [s]')
        plt.ylabel(r'Strees [$\mu$S]')
        plt.xlim([0,np.max(dat[k][:,0])])
        plt.legend()

plt.show()


