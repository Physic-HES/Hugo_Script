import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize as op
from scipy.integrate import odeint

#import archivos del ensayo
BM1 = pd.read_csv('Bomba_mecanica_1.txt')
BM2 = pd.read_csv('Bomba_mecanica_2.txt')
BM_apag = pd.read_csv('perdidas_bomba_mec_apagada.txt')
BD_1 = pd.read_csv('Bomba_difusora_1.txt')
BD_apag = pd.read_csv('Bomba_difusora_apagada.txt')

#conveccion:
conv_dNPT=pd.read_csv('conveccion_desdeNPT.txt')
conv_dVacioBM=pd.read_csv('conveccion_desde_Vacio_BM.txt')
conv_dNPT2=pd.read_csv('conveccion_desdeNPT_2.txt')
conv_en_vacio=pd.read_csv('conveccion_en_vacio.txt')
conv_en_vacio1=pd.read_csv('conveccion_en_vacio_1.txt')
conv_en_vacio_baj=pd.read_csv('conveccion_en_vacio_bajada.txt')


def bombeo(x,a,b,c):
    g=(a-c)*np.exp(-b*x)+c
    return g

def perdida(x,a,b,c):
    g=(a-c)*np.exp(-b*x)+c
    return g

def desgase(x,a,b):
    g=a*x+b
    return g

def f(y, t, a, b, c):
    return c +a*y**4 +b*y

def y(t, a, b, c, y0):
    """
    Solution to the ODE y'(t) = f(t,y,a,b) with initial condition y(0) = y0
    """
    y_ = odeint(f, y0, t, args=(a, b, c))
    return y_.ravel()

def cal(t,a,b,c):
    return (c-a)*np.exp(-t/b)+a

def enf(t,a,b,c):
    return a*np.exp(-t/b)+c

def r2(f_real,f_ajust):
    r_2=1-np.sum((f_real-f_ajust)**2)/np.sum((f_real-np.mean(f_real))**2)
    return r_2


ajust_desgase_BM_apag=pd.DataFrame()
ajust_perd_BD_apag=pd.DataFrame()
ajust_BM1=pd.DataFrame()
ajust_BM2=pd.DataFrame()

ajust_cov_dNPT=pd.DataFrame()
ajust_cov_dVacio=pd.DataFrame()
ajust_cov_dNPT2=pd.DataFrame()
ajust_cov_vacio=pd.DataFrame()
ajust_cov_vacio1=pd.DataFrame()
ajust_cov_vacio_baj=pd.DataFrame()

#Ajustes bomba mecanica
popt_BM,pcov_BM=op.curve_fit(desgase,BM_apag.values[:,0],BM_apag.values[:,1])
ajust_desgase_BM_apag['Descripcion']=['Q_d/V','P_0']
ajust_desgase_BM_apag['Valores']=[popt_BM[0],popt_BM[1]]
ajust_desgase_BM_apag['Desvio']=[np.sqrt(pcov_BM[0,0]),np.sqrt(pcov_BM[1,1])]
ajust_desgase_BM_apag['Unidades']=['mbar/s','mbar']
print('Ajuste de bomba mecanica apagada por desgase FIGURA 3')
print(ajust_desgase_BM_apag)
x=np.linspace(np.min(BM_apag.values[:,0]),np.max(BM_apag.values[:,0]),len(BM_apag.values[:,0]))
desg=desgase(x,popt_BM[0],popt_BM[1])
print(f'R^2= {r2(BM_apag.values[:,1],desg)}')
plt.figure(3)
plt.plot(BM_apag.values[:,0],BM_apag.values[:,1],'.',label='Bomba mecánica apagada')
plt.plot(x,desg,linewidth=3,label='Ajuste por desgase')
plt.xlim([np.min(BM_apag.values[:,0]),np.max(BM_apag.values[:,0])])
plt.legend()
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Presión [mbar]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

rango_ajuste=np.abs(BD_apag.values[:,0]-1735)<867.5
popt_BD,pcov_BD=op.curve_fit(perdida,BD_apag.values[rango_ajuste,0],BD_apag.values[rango_ajuste,1],[0.012,1/500,0.002])
ajust_perd_BD_apag['Descripcion']=['P_0','-L_perd/V','P_ext']
ajust_perd_BD_apag['Valores']=[popt_BD[0],popt_BD[1],popt_BD[2]]
ajust_perd_BD_apag['Desvio']=[np.sqrt(pcov_BD[0,0]),np.sqrt(pcov_BD[1,1]),np.sqrt(pcov_BD[2,2])]
ajust_perd_BD_apag['Unidades']=['mbar','s^-1','mbar']
print('Ajuste de bomba mecanica apagada por perdida FIGURA 5')
print(ajust_perd_BD_apag)
x=np.linspace(np.min(BD_apag.values[rango_ajuste,0]),np.max(BD_apag.values[rango_ajuste,0]),len(BD_apag.values[rango_ajuste,0]))
perd=perdida(x,popt_BD[0],popt_BD[1],popt_BD[2])
print(f'R^2= {r2(BD_apag.values[rango_ajuste,1],perd)}')
plt.figure(5)
plt.plot(BD_apag.values[:,0],BD_apag.values[:,1],'.',label='Bomba Difusora apagada')
plt.plot(x,perd,linewidth=3,label='Ajuste por perdidas')
plt.legend()
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Presión [mbar]',fontsize=14)
plt.xlim([np.min(BD_apag.values[:,0]),np.max(BD_apag.values[:,0])])
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

rango_ajuste=np.abs(BM1.values[:,0]-30.5)<44.5/2
#rango_ajuste=BM1.values[:,0]>8
start=[3E11,2,1E-4]
popt_B1,pcov_B1=op.curve_fit(bombeo,BM1.values[rango_ajuste,0],BM1.values[rango_ajuste,1],start)
print('Ajuste de bomba mecanica al encender por bombeo FIGURA 1')
ajust_BM1['Descripcion']=['P_0','S_i/V','P_f']
ajust_BM1['Valores']=[popt_B1[0],popt_B1[1],popt_B1[2]]
ajust_BM1['Desvio']=[np.sqrt(pcov_B1[0,0]),np.sqrt(pcov_B1[1,1]),np.sqrt(pcov_B1[2,2])]
ajust_BM1['Unidades']=['mbar','s^-1','mbar']
print(ajust_BM1)
x=np.linspace(np.min(BM1.values[rango_ajuste,0]),np.max(BM1.values[rango_ajuste,0]),len(BM1.values[rango_ajuste,0]))
bomb=bombeo(x,popt_B1[0],popt_B1[1],popt_B1[2])
bomb_=bombeo(x,start[0],start[1],start[2])
print(f'R^2= {r2(BM1.values[rango_ajuste,1],bomb)}')
plt.figure(1)
plt.loglog(BM1.values[:,0],BM1.values[:,1],'.',label='Presion del recinto con BM')
plt.loglog(x,bomb,linewidth=3,label='Ajuste a la ecuacion de bombeo')
#plt.loglog(x,bomb_,linewidth=3,label='Iteracion inicial del ajuste')
plt.xlim([np.min(BM1.values[:,0]),np.max(BM1.values[:,0])])
plt.grid()
plt.legend()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Presión [mbar]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

#rango_ajuste=np.abs(BM2.values[:,0]-51.5)<44.5
rango_ajuste=BM2.values[:,0]>7
popt_B2,pcov_B2=op.curve_fit(bombeo,BM2.values[rango_ajuste,0],BM2.values[rango_ajuste,1],[0.7,1/10,0.025])
ajust_BM2['Descripcion']=['P_0','S_i/V','P_f']
ajust_BM2['Valores']=[popt_B2[0],popt_B2[1],popt_B2[2]]
ajust_BM2['Desvio']=[np.sqrt(pcov_B2[0,0]),np.sqrt(pcov_B2[1,1]),np.sqrt(pcov_B2[2,2])]
ajust_BM2['Unidades']=['mbar','s^-1','mbar']
print('Ajuste de bomba mecanica al encender por bombeo FIGURA 2')
print(ajust_BM2)
x=np.linspace(np.min(BM2.values[rango_ajuste,0]),np.max(BM2.values[rango_ajuste,0]),len(BM2.values[rango_ajuste,0]))
bomb=bombeo(x,popt_B2[0],popt_B2[1],popt_B2[2])
print(f'R^2= {r2(BM2.values[rango_ajuste,1],bomb)}')
plt.figure(2)
plt.loglog(BM2.values[:,0],BM2.values[:,1],'.',label='Presion del recinto con BM')
plt.xlim([np.min(BM2.values[:,0]),np.max(BM2.values[:,0])])
#plt.semilogx(x,bomb,label='Ajuste a la ecuacion de bombeo')
plt.grid()
plt.legend()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Presión [mbar]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

#AJUSTE CONVECCION

popt, cov = op.curve_fit(y, conv_dNPT.values[:,0], conv_dNPT.values[:,2],[-1.8E-12,-0.0017,0.28,25])
popt2, cov2 = op.curve_fit(cal, conv_dNPT.values[:,0], conv_dNPT.values[:,2],[popt[2]/popt[1],500,25])
ajust_cov_dNPT['Descripcion']=['P_0/gamma','tau','T_0']
ajust_cov_dNPT['Valores']=[popt2[0],popt2[1],popt2[2]]
ajust_cov_dNPT['Desvio']=[np.sqrt(cov2[0,0]),np.sqrt(cov2[1,1]),np.sqrt(cov2[2,2])]
ajust_cov_dNPT['Unidades']=['C','s','C']
print('Parametros de calentamiento en CNP FIGURA 6')
print(ajust_cov_dNPT)
x=np.linspace(np.min(conv_dNPT.values[:,0]),np.max(conv_dNPT.values[:,0]),len(conv_dNPT.values[:,0]))
conv=y(x,popt[0],popt[1],popt[2],popt[3])
cale=cal(x,popt2[0],popt2[1],popt2[2])
#print(f'R^2 1er modelo= {r2(conv_dNPT.values[:,2],conv)}')
print(f'R^2 2do modelo= {r2(conv_dNPT.values[:,2],cale)}')
plt.figure(6)
plt.plot(conv_dNPT.values[:,0], conv_dNPT.values[:,2],'.',label='Temperatura con CNP')
#plt.plot(x,conv,label='Ajuste sobre ODE sin aprox')
plt.plot(x,cale,linewidth=3,label='Ajuste sobre solucion')
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Temperatura [C]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
calent1=[x,cale]

#popt, cov = op.curve_fit(y, conv_dVacioBM.values[:,0], conv_dVacioBM.values[:,2],[-1.8E-12,-0.0017,0.28,25])
#ajust_cov_dVacio['Descripcion']=['gamma','beta','alpha']
#ajust_cov_dVacio['Valores']=[popt[0],popt[1],popt[2]]
#ajust_cov_dVacio['Desvio']=[np.sqrt(cov[0,0]),np.sqrt(cov[1,1]),np.sqrt(cov[2,2])]
#ajust_cov_dVacio['Unidades']=['s^-1*T^-3','s^-1','T*s^-1']
#print(ajust_cov_dVacio)
#x=np.linspace(np.min(conv_dVacioBM.values[:,0]),np.max(conv_dVacioBM.values[:,0]),len(conv_dVacioBM.values[:,0]))
#conv=y(x,popt[0],popt[1],popt[2],popt[3])
#print(f'R^2= {r2(conv_dVacioBM.values[:,2],conv)}')
#plt.figure(60)
#plt.plot(conv_dVacioBM.values[:,0], conv_dVacioBM.values[:,2],label='Conveccion desde Vacio')
#plt.plot(x,conv,label='Ajuste')
#plt.grid()
#plt.xlabel('Tiempo [seg]')
#plt.ylabel('Temperatura [C]')
#plt.legend()

popt, cov = op.curve_fit(y, conv_dNPT2.values[:,0], conv_dNPT2.values[:,2],[-1.8E-12,-0.0017,0.28,25])
popt2, cov2 = op.curve_fit(enf, conv_dNPT2.values[:,0], conv_dNPT2.values[:,2],[popt[2]/popt[1],500,200])
ajust_cov_dNPT2['Descripcion']=['T_e','tau']
ajust_cov_dNPT2['Valores']=[popt2[0],popt2[1]]
ajust_cov_dNPT2['Desvio']=[np.sqrt(cov2[0,0]),np.sqrt(cov2[1,1])]
ajust_cov_dNPT2['Unidades']=['C','s']
print('Parametros de enfriamiento en CNP en la FIGURA 7')
print(ajust_cov_dNPT2)
x=np.linspace(np.min(conv_dNPT2.values[:,0]),np.max(conv_dNPT2.values[:,0]),len(conv_dNPT2.values[:,0]))
conv=y(x,popt[0],popt[1],popt[2],popt[3])
enfr=enf(x,popt2[0],popt2[1],popt2[2])
#print(f'R^2 1er modelo= {r2(conv_dNPT2.values[:,2],conv)}')
print(f'R^2 2er modelo= {r2(conv_dNPT2.values[:,2],enfr)}')
plt.figure(7)
plt.plot(conv_dNPT2.values[:,0], conv_dNPT2.values[:,2],'.',label='Temperatura con CNP')
#plt.plot(x,conv,label='Ajuste sobre ODE sin aprox')
plt.plot(x,enfr,linewidth=3,label='Ajuste sobre solucion')
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Temperatura [C]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
enfr1=[x,enfr]

#popt, cov = op.curve_fit(y, conv_en_vacio.values[:,0], conv_en_vacio.values[:,2],[-1.8E-12,-0.0017,0.28,25])
#popt2, cov2 = op.curve_fit(enf, conv_en_vacio.values[:,0], conv_en_vacio.values[:,2],[popt[2]/popt[1],10000,200])
#ajust_cov_vacio['Descripcion']=['gamma','beta','alpha','tau']
#ajust_cov_vacio['Valores']=[popt[0],popt[1],popt[2],popt2[1]]
#ajust_cov_vacio['Desvio']=[np.sqrt(cov[0,0]),np.sqrt(cov[1,1]),np.sqrt(cov[2,2]),np.sqrt(cov2[1,1])]
#ajust_cov_vacio['Unidades']=['s^-1*T^-3','s^-1','T*s^-1','s']
#print('Parametros de enfriamiento en vacio')
#print(ajust_cov_vacio)
#x=np.linspace(np.min(conv_en_vacio.values[:,0]),np.max(conv_en_vacio.values[:,0]),len(conv_en_vacio.values[:,0]))
#conv=y(x,popt[0],popt[1],popt[2],popt[3])
#enfr=enf(x,popt2[0],popt2[1],popt2[2])
#print(f'R^2 1er modelo= {r2(conv_en_vacio.values[:,2],conv)}')
#print(f'R^2 2er modelo= {r2(conv_en_vacio.values[:,2],enfr)}')
#plt.figure(70)
#plt.plot(conv_en_vacio.values[:,0], conv_en_vacio.values[:,2],label='Temperatura en vacio')
#plt.plot(x,conv,label='Ajuste sobre ODE sin aprox')
#plt.plot(x,enfr,label='Ajuste sobre solucion con aprox')
#plt.grid()
#plt.xlabel('Tiempo [seg]')
#plt.ylabel('Temperatura [C]')
#plt.legend()

popt, cov = op.curve_fit(y, conv_en_vacio1.values[:,0], conv_en_vacio1.values[:,2],[-1.8E-12,-0.0017,0.28,25])
popt2, cov2 = op.curve_fit(cal, conv_en_vacio1.values[:,0], conv_en_vacio1.values[:,2],[popt[2]/popt[1],500,25])
ajust_cov_vacio1['Descripcion']=['P_0/gamma','tau','T_0']
ajust_cov_vacio1['Valores']=[popt2[0],popt2[1],popt2[2]]
ajust_cov_vacio1['Desvio']=[np.sqrt(cov2[0,0]),np.sqrt(cov2[1,1]),np.sqrt(cov2[2,2])]
ajust_cov_vacio1['Unidades']=['C','s','C']
print('Parametros de calentamiento en vacio FIGURA 8')
print(ajust_cov_vacio1)
x=np.linspace(np.min(conv_en_vacio1.values[:,0]),np.max(conv_en_vacio1.values[:,0]),len(conv_en_vacio1.values[:,0]))
conv=y(x,popt[0],popt[1],popt[2],popt[3])
cale=cal(x,popt2[0],popt2[1],popt2[2])
#print(f'R^2 1er modelo= {r2(conv_en_vacio1.values[:,2],conv)}')
print(f'R^2 2do modelo= {r2(conv_en_vacio1.values[:,2],cale)}')
plt.figure(8)
plt.plot(conv_en_vacio1.values[:,0], conv_en_vacio1.values[:,2],'.',label='Temperatura en vacio')
#plt.plot(x,conv,label='Ajuste sobre ODE sin aprox')
plt.plot(x,cale,linewidth=3,label='Ajuste sobre solucion')
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Temperatura [C]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
calent2=[x,cale]

popt, cov = op.curve_fit(y, conv_en_vacio_baj.values[:,0], conv_en_vacio_baj.values[:,2],[-1.8E-12,-0.0017,0.28,25])
popt2, cov2 = op.curve_fit(enf, conv_en_vacio_baj.values[:,0], conv_en_vacio_baj.values[:,2],[popt[2]/popt[1],1000,200])
ajust_cov_vacio_baj['Descripcion']=['T_e','tau']
ajust_cov_vacio_baj['Valores']=[popt2[0],popt2[1]]
ajust_cov_vacio_baj['Desvio']=[np.sqrt(cov2[0,0]),np.sqrt(cov2[1,1])]
ajust_cov_vacio_baj['Unidades']=['C','s']
print('Parametros de enfriamiento en vacio FIGURA 9')
print(ajust_cov_vacio_baj)
x=np.linspace(np.min(conv_en_vacio_baj.values[:,0]),np.max(conv_en_vacio_baj.values[:,0]),len(conv_en_vacio_baj.values[:,0]))
conv=y(x,popt[0],popt[1],popt[2],popt[3])
enfr=enf(x,popt2[0],popt2[1],popt2[2])
#print(f'R^2 1er modelo= {r2(conv_en_vacio_baj.values[:,2],conv)}')
print(f'R^2 2er modelo= {r2(conv_en_vacio_baj.values[:,2],enfr)}')
plt.figure(9)
plt.plot(conv_en_vacio_baj.values[:,0], conv_en_vacio_baj.values[:,2],'.',label='Temperatura en vacio')
#plt.plot(x,conv,label='Ajuste sobre ODE sin aprox')
plt.plot(x,enfr,linewidth=3,label='Ajuste sobre solucion')
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Temperatura [C]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()
enfr2=[x,enfr]

plt.figure(90)
plt.plot(BD_1.values[:,0],BD_1.values[:,1],linewidth=3,label='Bomba Difusora 1')
plt.xlim([np.min(BD_1.values[:,0]),np.max(BD_1.values[:,0])])
plt.ylim([0,.12])
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Presión [mbar]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()

plt.figure(100)
plt.plot(conv_dNPT.values[:,0], conv_dNPT.values[:,2],'.',label='Temperatura con CNP')
plt.plot(conv_en_vacio1.values[:,0], conv_en_vacio1.values[:,2],'*',label='Temperatura en vacio')
plt.plot(calent1[0],calent1[1],linewidth=3,label='Ajuste en CNP')
plt.plot(calent2[0],calent2[1],linewidth=3,label='Ajuste en vacio')
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Temperatura [C]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()

plt.figure(101)
plt.plot(conv_dNPT2.values[:,0], conv_dNPT2.values[:,2],'.',label='Temperatura con CNP')
plt.plot(conv_en_vacio_baj.values[:,0], conv_en_vacio_baj.values[:,2],'*',label='Temperatura en vacio')
plt.plot(enfr1[0],enfr1[1],linewidth=3,label='Ajuste en CNP')
plt.plot(enfr2[0],enfr2[1],linewidth=3,label='Ajuste en vacio')
plt.grid()
plt.xlabel('Tiempo [seg]',fontsize=14)
plt.ylabel('Temperatura [C]',fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend()

plt.show()
