import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy import signal as S
import scipy as scp
import tkinter as tk
from tkinter import filedialog
import os
from tqdm import tqdm
import pandas as pd
from scipy import integrate as integ
root = tk.Tk()


def imp_lista():
    # Permite seleccionar un archivo exel que tenga una columna con una lista de RECs y
    # otra columna que contenga la lista de canales que corresponden a esos RECs
    # return:
    # Una lista de dos lugares, el primero corresponde a los RECs y el segundo a los canales
    folder_selected = filedialog.askdirectory()
    tk.mainloop()
    arch1 = os.listdir(path=folder_selected)
    for j in range(len(arch1)):
        print('[%2.0f] '%(j+1)+arch1[j])
    lis=np.array(eval(input('Seleccione una lista: '))) - 1
    df = pd.read_excel(folder_selected+'/'+arch1[lis])
    M1_list=list(df.iloc[:,0])
    M2_list=list(df.iloc[:,1])
    return [M1_list,M2_list]


def selrec(M,s,n,c):
    # Permite cargar una lista excel cuyas columnas sean numeros de recs y numero de canales1
    # imput:
    # M los datos ya cargados de los que se pretende seleccionar solo algunos RECs
    # Parametros:
    # s es la lista cargada con imp_lista
    # n es el numero de columna que contiene la lista de RECs que se pretende seleccionar de M2
    # c es el numero de columna que contiene la lista de canales de correspondientes a los RECs de n
    # return:
    # devuelve la misma estructura de datos que M pero con los RECs listados en el excel
    list=[]
    for k in range(len(s[0])):
        for j in np.arange(len(M[1])):
            if len(str(s[c-1][k]))==1:
                can=str(s[c-1][k])+'.'
            elif len(str(s[c-1][k]))>1:
                can = str(s[c - 1][k])
            if M[1][j][3:12]==r'%04.0f'%(np.double(s[n-1][k]))+'_ch'+can:
                list.append(j+1)
    List_2=np.array(list)
    sig=[List_2]
    sig1=[]
    sig2=[]
    for k in np.arange(len(List_2)):
        sig.append(M[0][List_2[k]])
        sig1.append(M[1][List_2[k] - 1])
        sig2.append(M[2][List_2[k] - 1])
    return [sig,sig1,sig2,M[3]]


def carga(recs=[0],coco='si',head=13):
    # Permite cargar .txt de una carpeta a eleccion mediante interface
    # wimdows (se selecciona la carpeta y luego se cierra la ventana en blanco)
    # para que muestre los archivos dentro de la carpeta
    # Parametros:
    # coco: 'si' por default : busca la unidad de ingenieria con la que se grabo el archivos
    # head: 13 por default : Establece las N+1 primeras filas como encabezado
    # return:
    # una lista de 4 lugares,
    # en [0] hay una lista donde:
    #   el primer lugar ([0][0]) es un array con la numeracion de señales correspondiente al presente codigo
    #   a partir del segundo lugar ([0][1:]) estan las señales con una columna de tiempo y otra de señal
    # en [1] estan las etiquetas de cada señal por ej. REC0470_ch5.txt
    # en [2] esta la unidad de ingenieria de cada señal return
    # en [3] esta la ruta de ubicacion en disco de donde se ubtuvieron los archivos
    folder_selected = filedialog.askdirectory()
    tk.mainloop()
    arch1=os.listdir(path=folder_selected)
    Arch1=[]
    Arch2=[]
    for y in range(len(arch1)):
        if len(arch1[y][10:-4])==1:
            Arch1.append(arch1[y])
        elif len(arch1[y][10:-4])==2:
            Arch2.append(arch1[y])
    arch3=Arch1+Arch2
    if recs[0]==0:
        for j in range(len(arch3)):
            print('[%4.0f] ' % (j + 1) + arch3[j])
        print(' ')
        print('[1] Importar carpeta /med completa')
        print('[2] Solo algunos canales')
        q3 = eval(input('Elija una opción:'))
        if q3 == 1:
            ch = np.arange(0, len(arch3))
        elif q3 == 2:
            ch = np.array(eval(input('Seleccione Canales: '))) - 1
        arch = []
        for h in range(len(ch)):
            arch.append(arch3[ch[h]])
    elif recs[0]>0:
        arch = []
        ch = []
        for k in np.arange(len(recs)):
            for j in np.arange(len(arch3)):
                if arch3[j][3:7]=='%04.0f'%recs[k]:
                    ch.append(j)
        ch = np.array(ch)
        for h in range(len(ch)):
            arch.append(arch3[ch[h]])
        for j in range(len(arch)):
            print('[%4.0f] ' % (j + 1) + arch3[ch[j]])
    q2 = eval(input('Modificar estiquetas? [1]=Si, [2]=No :'))
    if q2 == 1:
        etiq = []
        for j in range(len(ch)):
            etiq.append(eval(input(arch[j]+': ')))
    elif q2==2:
        etiq = []
        for j in range(len(ch)):
            etiq.append(arch[j])
    dat=[]
    dat.append(ch+1)
    pbar = tqdm(total=len(arch), desc='Importando datos...')
    if coco == 'no':
        EU = str(input('Ingrese EU: '))
    elif coco=='si':
        EU=[]
    for k in np.arange(1,len(arch)+1):
        datframe=pd.read_csv(folder_selected+'/'+arch[k-1],delimiter='\t', header=head)
        dat1 = datframe.values
        if coco == 'si':
            file1 = open(folder_selected + '/' + arch[k-1], 'r')
            for j in range(13):
                Lines = file1.readline()
            EU.append(Lines[Lines.find('(') + 1:Lines.find(')')])
        dat.append(dat1)
        pbar.update(1)
    pbar.close()
    print('::: Carga de datos :::')
    print(' ')
    print('Señales importadas: %6.0f '%len(arch3))
    print('Datos por señal: %6.0f'%len(dat1[:,0]))
    print('Frecuencia de muestreo: %6.0f Hz'%(1/(dat1[1,0]-dat1[0,0])))
    print('Tiempo de registro: %6.3f seg' % (len(dat1[:,0]) * (dat1[1, 0] - dat1[0, 0])))
    return [dat,etiq,EU,folder_selected]


def welch_h(dat1,N=8192,rang=[2,1000],overl=50):
    # Permite obtener un espectro promediado en archivo tipo Spec (propio de este codigo)
    # imput:
    # dat1 son los datos temporales cargado con la funcion carga
    # Parametros:
    # N: cantidad de lineas, default: N=8192
    # rang: el rango en frecuencia de donde se quiere obtener el valor RMS, default: rang=[2,1000]
    # overl: Overlap, default: 50%
    # return:
    # lista de 5 lugares
    # en el primero [0][:] existe una lista cuyos lugares son ocupados por los espectros con columna de Frecuencia
    # en el segundo [1] estan las etiquetas de las señales junto con su valor rms
    # en el tercero [2] hay una lista de los maxmimos valores de cada espectros
    # en el cuarto [3] estan las unidades de ingenieria de cada señal return
    # en el quinto [4] esta la ruta de donde fueron cargados los archivos temporales
    dat=dat1[0][1:]
    tam=len(dat)
    etiq= dat1[1]
    fs=1/(dat[0][1,0]-dat[0][0,0])
    B=2*N
    ov=int(overl/100*B)
    EU=dat1[2]
    Sc1=LA.norm(S.get_window('hann',N))/np.sqrt(N)
    Sc2=1/np.mean(S.get_window('hann',N))
    print(' ')
    print('::: Configuracion de espectros :::')
    print(' ')
    print('Señales analizadas: %6.0f' % (tam-1))
    print('Cantidad de Lineas: %6.0f' % N)
    print('Ventana:           Hanning')
    print('Promediado:         Lineal')
    print('Tamaño de Bloque:   %6.0f' % B)
    print('Overlap:            %6.0f' % overl)
    print('Banda de analisis: %6.2f Hz'%(fs/2))
    print('Delta f:            %6.0f Hz' % (fs/2/N))
    M=[]
    RMS=[]
    Result=[]
    tech=[]
    ETIQ=[]
    print(' ')
    print('::: Valores RMS '+str(rang)+' Hz :::')
    for j in np.arange(0,tam):
        M.append(S.welch(dat[j][:,1],1/(dat[0][1,0]-dat[0][0,0]),
                         window='hann',nperseg=B,
                         noverlap=ov,scaling='spectrum'))
        desd = np.argmin(np.abs(M[0][0] - rang[0]))
        hast = np.argmin(np.abs(M[0][0] - rang[1]))
        RMS.append(np.sqrt(Sc1*np.sum(M[-1][1][desd:hast])))
        Mch=np.zeros((len(M[-1][0]),2))
        Mch[:, 0] = M[-1][0]
        Mch[:, 1] = np.sqrt(M[-1][1]*Sc2)
        Result.append(Mch)
        ETIQ.append(etiq[j] + ' RMS=%2.3e ' % RMS[-1] + EU[j])
        print(ETIQ[-1])
        tech.append(np.max(Mch[desd:hast,1]))
    return [Result,ETIQ,tech,EU,dat1[3]]


def tf(dat1,N=8192,overl=50,canales='no'):
    # Permite calcular la funcion de transferencia de todas las señales respecto de otra
    # utilizando ademas un metodo promediado tipo welch_h
    # imput:
    # dat1 son los datos temporales que se cargaron con la funcion carga
    # Parametros:
    # N: cantidad de lineas, default: N=8192
    # overl: Overlap, default: 50%
    # canales: si se desea elegir algunos canales para realizar la transferencia, default: canales='no'
    # return:
    # lista de 5 lugares
    # en el primero [0][:] existe una lista cuyo primer lugar esta reservado para la frecuencia y el resto de
    # lugares son ocupados por los espectros con amplitud y fase
    # en el segundo [1] estan las etiquetas de las señales
    # en el tercero [2] hay una lista de los maxmimos valores de cada espectros
    # en el cuarto [3] estan las unidades de ingenieria de cada señal return
    # en el quinto [4] esta la ruta de donde fueron cargados los archivos temporales
    dat=dat1[0][1:]
    tam=len(dat)
    etiq= dat1[1]
    fs=1/(dat[0][1,0]-dat[0][0,0])
    B=2*N
    ov=int(overl/100*B)
    EU=dat1[2]
    print(' ')
    print('::: Configuracion de espectros para la funcion de transferencia :::')
    print(' ')
    print('Señales analizadas: %6.0f' % (tam-1))
    print('Cantidad de Lineas: %6.0f' % N)
    print('Ventana:           Hanning')
    print('Promediado:         Lineal')
    print('Tamaño de Bloque:   %6.0f' % B)
    print('Overlap:            %6.0f' % overl)
    print('Banda de analisis: %6.2f Hz'%(fs/2))
    print('Delta f:            %6.0f Hz' % (fs/2/N))
    print(' ')
    for j in range(len(dat1[1])):
        print('[%2.0f] ' % (j + 1) + dat1[1][j])
    if canales == 'no':
        CH = range(len(dat1[0])-1)
    elif canales == 'si':
        canales1 = eval(input('Seleccionar señales: '))
        CH = np.array(canales1) - 1
    ch_ref = np.array(eval(input('Elija el canal de referencia: ')))
    CH2 = np.delete(CH, ch_ref - 1)
    M1=[0,0]
    M2=[0,0]
    Result=[np.linspace(0,fs/2,N)]
    tech=[]
    ETIQ=[]
    P=int(len(dat[0][:,1])/ov-1)
    for j in np.arange(1,len(CH2)):
        pbar = tqdm(total=P, desc='Procesando '+etiq[CH2[j-1]]+': ')
        ini = 0
        fin = B
        for p in np.arange(0,P):
            y_ref1 = scp.fft(dat[CH[ch_ref - 1]][ini:fin,1])
            y1=scp.fft(dat[CH2[j]][ini:fin,1])
            M1[0]=np.abs(y1[0:N]/y_ref1[0:N])
            M2[0]=np.angle(y1[0:N]/y_ref1[0:N],deg=True)
            ini += ov
            fin += ov
            y_ref2 = scp.fft(dat[CH[ch_ref - 1]][ini:fin,1])
            y2 = scp.fft(dat[CH2[j]][ini:fin,1])
            if p<P-1:
                M1[1]=(np.array(np.abs(y2[0:N]/y_ref2[0:N]))+np.array(M1[0]))/2
                M2[1] =(np.array(np.angle(y2[0:N]/y_ref2[0:N],deg=True))+np.array(M2[0]))/2
            pbar.update(1)
        Result.append([M1[1],M2[1]])
        tech.append(np.max(M1[1]))
        ETIQ.append(etiq[CH2[j-1]])
        pbar.close()
    return [Result,ETIQ,tech,EU,dat1[3]]


def casc(dat1,N=2048,overl=50):
    # Permite obtener un espectro en cascada promediado en archivo tipo casc (propio de este codigo)
    # imput:
    # dat1 son los datos temporales cargado con la funcion carga
    # Parametros:
    # N: cantidad de lineas, default: N=2048
    # overl: Overlap, default: 50%
    # return:
    # lista de 5 lugares
    # en el primero [0][:] cada lugar esta ocupado por otra lista de tres lugares,
    # una para t otra para f y otra para el spectrograma
    # en el segundo [1] estan las etiquetas de las señales
    # en el tercero [2] hay una lista de los maxmimos valores de cada espectrograma
    # en el cuarto [3] estan las unidades de ingenieria de cada señal return
    # en el quinto [4] esta la ruta de donde fueron cargados los archivos temporales
    dat=dat1[0][1:]
    tam=len(dat)
    etiq= dat1[1]
    B=2*N
    fs = 1 / (dat[0][1,0] - dat[0][0,0])
    ov=int(overl/100*B)
    print(' ')
    print('::: Configuracion de espectros en cascada :::')
    print(' ')
    print('Señales analizadas: %6.0f' % tam)
    print('Cantidad de Lineas: %6.0f' % N)
    print('Ventana:           Hanning')
    print('Promediado:         Lineal')
    print('Tamaño de Bloque:   %6.0f' % B)
    print('Overlap:            %6.0f' % overl)
    print('Banda de analisis: %6.2f Hz' % (fs / 2))
    print('Delta f:            %6.3f Hz' % (fs / 2 / N))
    print('Delta t:            %6.3f seg' % (ov / fs))
    EU=dat1[2]
    Result=[]
    ETIQ=[]
    tech=[]
    for j in np.arange(1,len(dat1[0])):
        f, t, Sxx=S.spectrogram(dat1[0][j][:,1],fs,
                                window='hann',nperseg=B,
                                noverlap=ov,scaling='spectrum')
        Result.append([t,f,Sxx])
        ETIQ.append(etiq[j - 1])
        tech.append(np.max(np.max(Sxx)))
    return [Result,ETIQ,EU,tech,dat1[3]]


def graf(M,type,f_amp='0pk',scale='lin',fig2='si',canales='no',Vmax=0,xlim=[0,500],save='no'):
    # Permite plotear cualquier estructura de datos elaborada en el presente codigo,
    # por ejemplo cascados, transferencias, espectros y temporales. Ademas permite
    # guardar cada espectro en formatos .png y .txt en una carpeta /fft previamente
    # creada para tal fin en la carpeta de donde se obtuvieron las señales
    # temporales que luego se procesaron en espectros.
    # imput:
    # M: estructura de datos tipo casc (funcion casc), temp (funcion carga),
    # tranf (funcion tf) o spec (funcion welch_h)
    # type : 'Spec', 'casc', 'Tranf', 'Temp'
    # f_amp: Magnitud en la que prefiere el 'Spec', default: f_amp=0pk
    # scale: escala del grafico, default: scale='lin' (lineal)
    # fig2: si se desea que cada señal se plotee en un grafico distinto o no, default: fig2='si'
    # canales: si desea plotear solo algunos canales de los datos M, modifique a 'si', default: canales='no'
    # Vmax: altura en z para los graficos de spectrograma, si no se modifica el valor por default,
    # se setea el vmax como el maximo valor en amplitud que tomo el espectrograma, default: Vmax=0
    # xlim: limite de valores en x que se muestran para espectros 'Spec', default: xlim=[0,500]
    # save: opcion de guardado de espectros tipo 'Spec', default: save='no'. Si save='si' cada
    # espectro se guarda en formatos .png y .txt en una carpeta /fft previamente
    # creada para tal fin en la carpeta de donde se obtuvieron las señales.
    if fig2=='si':
        plt.figure()
    if type=='Spec':
        if canales == 'no':
            CH = range(len(M[0]))
        elif canales == 'si':
            for j in range(len(M[0])):
                print('[%2.0f] ' %(j+1) + M[1][j])
            canales1 = eval(input('Graficar las señales: '))
            CH = np.array(canales1) - 1
        elif canales[0]=='[':
            CH=np.array(eval(canales))-1
        if f_amp=='0pk':
            fA=1
        elif f_amp=='rms':
            fA=1/np.sqrt(2)
        elif f_amp=='pkpk':
            fA=2
        if save=='si':
            pbar = tqdm(total=len(CH), desc='Guardando espectros...')
        if scale=='lin':
            l=1
            for k in CH:
                if save=='si':
                    plt.figure(l)
                plt.plot(M[0][k][:, 0], fA*M[0][k][:, 1], label=M[1][k])
                plt.xlim([np.min(M[0][k][:, 0]), np.max(M[0][k][:, 0])])
                plt.ylabel('Amp ' + f_amp + ' [' + M[3][k] + ']')
                if save=='si':
                    plt.ylim([0, 1.03 * M[2][k]])
                elif save=='no':
                    plt.ylim([0, 1.03 * np.max(M[2])])
                plt.xlabel('Frecuencia [Hz]')
                plt.grid(b='bool')
                plt.legend()
                plt.xlim(xlim)
                if save=='si':
                    plt.savefig(M[4]+'/'+'fft/fft_'+M[1][k][0:12]+'.png')
                    np.savetxt(M[4]+'/'+'fft/fft_'+M[1][k][0:12]+'.txt',
                               M[0][k],delimiter='\t',fmt='%1.6e')
                    pbar.update(1)
                    plt.close(l)
                l+=1
            if save=='si':
                pbar.close()
        elif scale=='log':
            for k in CH:
                plt.loglog(M[0][k][:, 0], fA*M[0][k][:, 1], label=M[1][k])
                plt.xlim([np.min(M[0][k][1:, 0]), np.max(M[0][k][:, 0])])
                plt.ylabel('Amp ' + f_amp + ' [' + M[3][k] + ']')
                plt.xlabel('Frecuencia [Hz]')
                plt.grid(b='bool')
                plt.legend()
                if save=='si':
                    plt.savefig(M[4]+'/'+'fft/fft_'+M[1][k][0:11]+'.png')
                    np.savetxt(M[4]+'/'+'fft/fft_'+M[1][k][0:11]+'.txt',
                               M[0][k],delimiter='\t',fmt='%1.6e')
                    pbar.update(1)
            if save == 'si':
                pbar.close()
    if type=='Tranf':
        if canales == 'no':
            CH = range(len(M[1]))
        elif canales == 'si':
            for j in range(len(M[1])):
                print('[%2.0f] ' % (j + 1) + M[1][j])
            canales1 = eval(input('Seleccionar señales: '))
            CH = np.array(canales1) - 1
        if scale=='lin':
            plt.subplot(211)
            h=0
            for k in np.arange(1,len(CH)):
                plt.plot(M[0][0],M[0][k][0], label=M[1][h])
                plt.xlim([np.min(M[0][0]), np.max(M[0][0])])
                plt.ylabel('Factor de amplificación')
                plt.ylim([0, 1.03 * np.max(np.array(M[2]))])
                h+=1
            plt.legend()
            plt.subplot(212)
            h=0
            for k in np.arange(1,len(CH)):
                plt.plot(M[0][0],M[0][k][1], label=M[1][h])
                plt.xlim([np.min(M[0][0]), np.max(M[0][0])])
                plt.ylabel('Fase [deg]')
                plt.xlabel('Frecuencia [Hz]')
                h+=1
            plt.legend()
        elif scale=='log':
            plt.subplot(211)
            h=0
            for k in np.arange(1,len(CH)):
                plt.loglog(M[0][0], M[0][k][0], label=M[1][h])
                plt.ylabel('Factor de amplificación')
                h+=1
            plt.legend()
            plt.subplot(212)
            h=0
            for k in np.arange(1,len(CH)):
                plt.loglog(M[0][0], M[0][k][1], label=M[1][h])
                plt.ylabel('Fase [deg]')
                plt.xlabel('Frecuencia [Hz]')
                plt.draw()
                h += 1
            plt.legend()
    elif type=='Temp':
        if canales == 'no':
            CH1 = np.arange(1, len(M[0]))
        elif canales == 'si':
            for j in range(len(M[1])):
                print('[%2.0f] ' %(j+1) + M[1][j])
            canales1 = eval(input('Graficar las señales: '))
            CH1 = np.array(canales1)
        for k in CH1:
            print('AMP de '+M[1][k-1][0:12]+': %1.5e ['%np.max(M[0][k][:,1])+M[2][k-1]+'] 0-pk')
            plt.plot(M[0][k][:,0], M[0][k][:,1], label=M[1][k-1])
            plt.xlim([np.min(M[0][k][:,0]), np.max(M[0][k][:,0])])
            plt.ylabel('Amp [' + M[2][k-2] + ']')
            plt.xlabel('Tiempo [seg]')
            plt.grid()
            plt.legend()
    elif type == 'casc':
        plt.close()
        if canales == 'no':
            CH = range(len(M[0]))
        elif canales == 'si':
            for j in range(len(M[0])):
                print('[%2.0f] ' %(j+1) + M[1][j])
            canales1 = eval(input('Graficar las señales: '))
            CH = np.array(canales1) - 1
        if save=='si':
            pbar = tqdm(total=len(CH), desc='Guardando cascadas...')
        for k in range(len(CH)):
            plt.figure(figsize=(10,5))
            if Vmax==0:
                Vmax1 = np.max(M[0][CH[k]][2])
            elif Vmax>0:
                Vmax1=Vmax
            Vmin1=Vmax1/1E5
            plt.pcolormesh(M[0][CH[k]][0], M[0][CH[k]][1], M[0][CH[k]][2],
                           shading='gouraud',norm=LogNorm(vmin=Vmin1, vmax=Vmax1))
            plt.ylabel('Frecuencia [Hz]')
            plt.xlabel('Tiempo [seg]')
            plt.ylim(xlim)
            cbar=plt.colorbar()
            cbar.set_label(M[1][CH[k]]+' ['+M[2][CH[k]]+']')
            plt.title(M[1][CH[k]])
            if save=='si':
                plt.savefig(M[4]+'/'+'casc/casc_'+M[1][k][0:11]+'.png')
                np.savetxt(M[4]+'/'+'casc/casc_'+M[1][k][0:11]+'.txt',
                           M[0][k][2],delimiter='\t',fmt='%1.6e')
                pbar.update(1)
                plt.close()
        if save == 'si':
            pbar.close()


def passband(dat1,lowcut,highcut,MAN='no'):
    # Permite cortar filtrar con un pasa banda una señal temporat tipo Temp (propia del presente codigo)
    # imput:
    # dat1: son los datos temporales cargado con la funcion carga
    # lowcut: la frecuencia de corte inferior
    # highcut: la frecuencia de corte superior
    # Parametros:
    # MAN: escribe en la consola los valores de amplitud maximos alcanzados
    # por la temporal filtrada en g, default: MAN='no'
    # retunn:
    # mismas caracteristicas de datos que los cargados con la funcion cargar
    # pero con todas las señales filtradas
    dat=dat1[0][1:]
    dat2=[dat1[0][0]]
    dat3=np.zeros(np.shape(dat1[0][1]))
    fs = 1 / (dat1[0][1][1,0] - dat1[0][1][0,0])
    len_sig=len(dat[0][:,0])
    desde = int(lowcut / (fs / 2) * len_sig)
    hasta = int(highcut / (fs / 2) * len_sig)
    print([desde,hasta])
    vent=np.zeros(len_sig)
    vent[desde:hasta]=1
    vent2=np.concatenate((vent,vent[-np.sort(-np.arange(len_sig))]))
    for k in np.arange(1,len(dat1[0])):
        esp=np.fft.fft(dat1[0][k][:,1],n=2*len_sig)
        rms_esp=np.sqrt(np.sum(np.abs(esp[desde:hasta]))/len(np.abs(esp[desde:hasta])))
        esp_=np.real(np.fft.ifft(vent2*esp))
        rms_esp_=np.sqrt(np.sum(np.abs(np.fft.fft(esp_[desde:hasta],n=2*len_sig)))/len(np.abs(esp_[desde:hasta])))
        fa=rms_esp/rms_esp_
        F=fa*np.real(np.fft.ifft(vent2*np.fft.fft(dat1[0][k][:,1],n=2*len_sig)))
        dat3[:,0]=dat1[0][1][:,0]
        nuev=F[0:len_sig]
        dat3[:,1]=nuev.T
        dat2.append(dat3)
    if MAN=='si':
        j=0
        for s in dat1[2]:
            if s=='m/s^2':
                print('AMP de '+dat1[1][j][0:12]+': %1.5e ['%(np.max(dat2[j+1][:,1])/10)+'g] 0-pk')
            j+=1
    return [dat2,dat1[1],dat1[2],dat1[3]]


def recortar(M,ini=0,fin=0,ultimos=0,primeros=0):
    # Permite recortar una señal temporal
    # imput:
    # M: es un conjunto de datos temporales tipo Temp, es decir como los que se
    # obtienen al usar la funcion cargar
    # Parametros:
    # ini: inicio de cortado, default: ini=0, al utilizar ini y fin los datos de tiempo comienzan
    # en ini y terminan en fin
    # fin: fin de cortado, default: fin=0. Si se utiliza el fin con valor negativo se corta
    # desde cero hasta ini y desde fin hasta que terminen los datos, ademas se unifica
    # la columna de tiempo sin cortes.
    # ultimos: si ini=fin y ultimos es mayor que cero, recorta los ultimos segundos que se le indique
    # primeros: si ini=fin y primeros es mayor que cero, se recortan los primeros segundos que se le indiquen.
    # return:
    # misma estructura de tados temporales (lista de cuatro lugares) como los que se obtienen al cargar
    # datos con la funcion cargar pero con las señales recortadas.
    sig=[M[0][0]]
    fs=1/(M[0][1][1,0]-M[0][1][0,0])
    if ini<fin:
        for j in np.arange(1,len(M[0])):
            ind_ini = np.argmin(np.abs(M[0][j][:, 0] - np.abs(ini)))
            ind_fin = np.argmin(np.abs(M[0][j][:, 0] - np.abs(fin)))
            T=M[0][j][ind_ini:ind_fin,0]
            S=M[0][j][ind_ini:ind_fin,1]
            sig_=np.zeros((len(T),len(M[0][j][1,:])))
            sig_[:,0]=T
            sig_[:,1]=S
            sig.append(sig_)
    if ini>fin:
        for j in np.arange(1,len(M[0])):
            ind_ini = np.argmin(np.abs(M[0][j][:,0] - np.abs(ini)))
            ind_fin = np.argmin(np.abs(M[0][j][:,0] - np.abs(fin)))
            size = len(M[0][1][:,0]) - (ind_fin-ind_ini)
            T=(size - 1) / fs * np.linspace(0, 1, size)
            aux=M[0][j][:,1]
            del aux[ind_ini:ind_fin]
            sig_ = np.zeros((len(T), len(M[0][j][1, :])))
            sig_[:, 0] = T
            sig_[:, 1] = aux
            sig.append(sig_)
    if ini==fin and ultimos>0:
        for j in np.arange(1,len(M[0])):
            ind_ini = np.argmin(np.abs(M[0][j][:,0] - (np.max(M[0][j][:,0])-np.abs(ultimos))))
            sig.append(M[0][j][ind_ini:,:])
    if ini==fin and primeros>0:
        for j in np.arange(1,len(M[0])):
            ind_fin = np.argmin(np.abs(M[0][j][:, 0] - np.abs(primeros)))
            sig.append(M[0][j][:ind_fin,:])
    return [sig,M[1],M[2],M[3]]


def int_spec(M,rang=[2,1000]):
    # Permite integrar los datos tipo Spec obtenidos de la funcion welch_h
    # imput:
    # M: espectros obtenidos con la funcion welch_h
    # Parametros:
    # rang: rango de frecuencias de donde se quiere obtener un valor RMS
    # return:
    # Estructura de datos igual a la obtenida con la funcion welch_h solo que con
    # los espectros integrados una vez
    N=len(M[0][0][:,0])
    Sc1 = LA.norm(S.get_window('hann', N)) / np.sqrt(N)
    Sc2 = 1 / np.mean(S.get_window('hann', N))
    M1=[]
    EU=[]
    tech=[]
    ETIQ=[]
    RMS=[]
    print(' ')
    print('::: Valores RMS ' + str(rang) + ' Hz :::')
    for j in np.arange(len(M[0])):
        M2=np.zeros((len(M[0][0][:,0])-1,2))
        M2[:,0]=M[0][j][1:,0]
        M2[:, 1] = M[0][j][1:, 1]/(2*np.pi*M[0][j][1:,0])
        M1.append(M2)
        desd = np.argmin(np.abs(M[0][0][:,0] - rang[0]))
        hast = np.argmin(np.abs(M[0][0][:,0] - rang[1]))
        RMS.append(np.sqrt(Sc1*np.sum(M1[j][desd:hast, 1]**2/Sc2)))
        if M[3][j]=='m/s^2':
            EU.append('m/s')
        elif M[3][j]=='m/s':
            EU.append('m')
        ind=M[1][j].find('=')
        ETIQ.append(M[1][j][0:ind] + '=%2.3e '%(RMS[j]) + EU[j])
        print(ETIQ[j])
        tech.append(np.max(M1[-1][desd:hast, 1]))
    return [M1,ETIQ,tech,EU,M[4]]


def int_temp(M1,Lcut1=2):
    # Permite integrar señales temporales
    # imput:
    # M1 es una temporal obtenida con la funcion carga
    # Lcut1 es la frecuencia de corte para el pasa altos, por default es 2
    M=M1
    fs = 1 / (M[0][1][1,0] - M[0][1][0,0])
    Lcut=Lcut1
    M2=passband(M, Lcut, fs/2-2)
    dat=[]
    EU = []
    dat.append(M2[0][0])
    zer=np.zeros((len(M2[0][1][:,0])-1,2))
    for k in np.arange(1,len(M1[0])):
        print(k)
        zer[:,0]=M2[0][k][0:-1,0]
        zer[:, 1] = integ.cumtrapz(M2[0][k][:, 1],M2[0][k][:,0])
        dat.append(zer)
        if M1[2][k-1]=='m/s^2':
            EU.append('m/s')
        elif M1[2][k-1]=='m/s':
            EU.append('m')
    return [dat,M[1],EU,M[3]]


def dupl(M):
    # Permite duplicar señales temporales, concatenando la señal consigo misma
    # asignandole un unico eje de tiempo
    dat=[]
    dat.append(M[0][0])
    for j in np.arange(1,len(M[0])):
        tam = len(M[0][j][:, 0])
        t = np.linspace(0, 2 * np.max(M[0][j][:, 0]), 2 * tam)
        zer=np.zeros((2*tam,2))
        zer[:,0]=t
        zer[:,1]=np.concatenate((M[0][j][:, 1],M[0][j][:, 1]))
        dat.append(zer)
    return [dat,M[1],M[2],M[3]]

#lista_M2_temp=[377,378,376,380,379,113,114,112,117,115,116,111,110,109,381,382,252,250,251,253,254,255]
