from scipy import optimize as opt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

folder_selected='/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/'
arch='EECE0322022_'
Caudal=['Q15_','Q20_','Q25_','Q30_','Q35_']
barrido=['01.txt','02.txt']
head=38

def ensayo(cau,barr,type):
      folder_selected = '/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/txt/'
      arch = 'EECE0322022_'
      if type=='DP':
            col=[0,2,4,5,6,7,8,9,13]
            titles = ['Time [s]', 'Temp [C]', 'DP1 [bar]', 'DP2 [bar]',
                      'DP3 [bar]', 'DP4 [bar]', 'DP5 [bar]', 'DP6 [bar]', 'Caudal [kg/s]']
            datframe = pd.read_csv(folder_selected + arch + r'Q%2.0f_' % cau + r'%02.0f.txt' % barr,
                                   delimiter='\t', usecols=col, index_col=False, header=34, names=titles, nrows=65)
      elif type=='ABS':
            col=[1,10,11,12]
            titles=['Time [s]','ABS1 [bar]','ABS2 [bar]','ABS3 [bar]']
            datframe = pd.read_csv(folder_selected + arch + r'Q%2.0f_' % cau + r'%02.0f.txt' % barr,
                             delimiter='\t', usecols=col, index_col=False, header=34, names=titles)
      return datframe

#Constantes:
dens=pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t', index_col=False)
ro=dens.values[6,1] #densidad
mu=dens.values[6,3] #viscosidad
D_CE=0.1082 #Diametro canal de ensayo en m
D_barr=0.0129 #Diametro barras en m
A_CE=np.pi*D_CE**2/4
A_barr=37*np.pi*D_barr**2/4
A_p=A_CE-A_barr #Area de paso
P_m=np.pi*D_CE+37*np.pi*D_barr #Perimetro mojado
D_h=4*A_p/P_m #Diametro hidraulico
l_dp4=0.2
l_dp2=0.2005
l_dp3=0.456
l_dp5=0.60475
l_dp6=0.2275


E1=[1,2]
E2=[3,4]

def prom(E):
    dep1=pd.DataFrame()
    Q = [15, 20, 25, 30, 35]
    for j in E:
        for q in Q:
            ens=ensayo(q,j,'DP')
            dep1=dep1.append({'Caudal_mean[kg/s]': ens['Caudal [kg/s]'].mean(),'Caudal_std[kg/s]': ens['Caudal [kg/s]'].std(),
                              'DP1_mean[bar]': ens['DP1 [bar]'].mean(),'DP1_std[kg/s]': ens['DP1 [bar]'].std(),
                              'DP2_mean[bar]': ens['DP2 [bar]'].mean(), 'DP2_std[kg/s]': ens['DP2 [bar]'].std(),
                              'DP3_mean[bar]': ens['DP3 [bar]'].mean(), 'DP3_std[kg/s]': ens['DP3 [bar]'].std(),
                              'DP4_mean[bar]': ens['DP4 [bar]'].mean(), 'DP4_std[kg/s]': ens['DP4 [bar]'].std(),
                              'DP5_mean[bar]': ens['DP5 [bar]'].mean(), 'DP5_std[kg/s]': ens['DP5 [bar]'].std(),
                              'DP6_mean[bar]': ens['DP6 [bar]'].mean(), 'DP6_std[kg/s]': ens['DP6 [bar]'].std()},
                             ignore_index=True)
    return dep1


def func1(x,eps_EC):
    dens = pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t',
                       index_col=False)
    ro = dens.values[6, 1]  # densidad
    D_CE = 0.1082  # Diametro canal de ensayo en m
    A_CE = np.pi * D_CE ** 2 / 4
    A_barr = 37 * np.pi * D_barr ** 2 / 4
    A_p = A_CE - A_barr  # Area de paso
    return eps_EC / (2 * ro * A_p ** 2) * x ** 2

def func2(x,f_dp4):
    dens = pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t',
                       index_col=False)
    ro = dens.values[6, 1]  # densidad
    D_CE = 0.1082  # Diametro canal de ensayo en m
    D_barr = 0.0129  # Diametro barras en m
    A_CE = np.pi * D_CE ** 2 / 4
    A_barr = 37 * np.pi * D_barr ** 2 / 4
    A_p = A_CE - A_barr  # Area de paso
    P_m = np.pi * D_CE + 37 * np.pi * D_barr  # Perimetro mojado
    D_h = 4 * A_p / P_m  # Diametro hidraulico
    l_dp4 = 0.2
    return (f_dp4 * l_dp4 / D_h) / (2 * ro * A_p ** 2) * x ** 2

def func3(x,K_sep1,f_dp4):
    dens = pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t',
                       index_col=False)
    ro = dens.values[6, 1]  # densidad
    D_CE = 0.1082  # Diametro canal de ensayo en m
    D_barr = 0.0129  # Diametro barras en m
    A_CE = np.pi * D_CE ** 2 / 4
    A_barr = 37 * np.pi * D_barr ** 2 / 4
    A_p = A_CE - A_barr  # Area de paso
    P_m = np.pi * D_CE + 37 * np.pi * D_barr  # Perimetro mojado
    D_h = 4 * A_p / P_m  # Diametro hidraulico
    l_dp2 = 0.2005
    return (f_dp4*l_dp2/D_h+K_sep1+(A_CE**2-A_p**2)/A_CE**2)/(2*ro*A_p**2)*x**2

def func4(x,K_sep2y3,f_dp4):
    dens = pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t',
                       index_col=False)
    ro = dens.values[6, 1]  # densidad
    D_CE = 0.1082  # Diametro canal de ensayo en m
    D_barr = 0.0129  # Diametro barras en m
    A_CE = np.pi * D_CE ** 2 / 4
    A_barr = 37 * np.pi * D_barr ** 2 / 4
    A_p = A_CE - A_barr  # Area de paso
    P_m = np.pi * D_CE + 37 * np.pi * D_barr  # Perimetro mojado
    D_h = 4 * A_p / P_m  # Diametro hidraulico
    l_dp3 = 0.456
    return (f_dp4*l_dp3/D_h+K_sep2y3)/(2*ro*A_p**2)*x**2

def func5(x,K_sep4y5,f_dp4):
    dens = pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t',
                       index_col=False)
    ro = dens.values[6, 1]  # densidad
    D_CE = 0.1082  # Diametro canal de ensayo en m
    D_barr = 0.0129  # Diametro barras en m
    A_CE = np.pi * D_CE ** 2 / 4
    A_barr = 37 * np.pi * D_barr ** 2 / 4
    A_p = A_CE - A_barr  # Area de paso
    P_m = np.pi * D_CE + 37 * np.pi * D_barr  # Perimetro mojado
    D_h = 4 * A_p / P_m  # Diametro hidraulico
    l_dp5 = 0.60475
    return (f_dp4*l_dp5/D_h+K_sep4y5)/(2*ro*A_p**2)*x**2

def func6(x,f_dp6):
    dens = pd.read_csv('/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/dens_temp.txt', delimiter='\t',
                       index_col=False)
    ro = dens.values[6, 1]  # densidad
    D_CE = 0.1082  # Diametro canal de ensayo en m
    D_barr = 0.0129  # Diametro barras en m
    A_CE = np.pi * D_CE ** 2 / 4
    A_barr = 37 * np.pi * D_barr ** 2 / 4
    A_p = A_CE - A_barr  # Area de paso
    P_m = np.pi * D_CE + 37 * np.pi * D_barr  # Perimetro mojado
    D_h = 4 * A_p / P_m  # Diametro hidraulico
    l_dp6 = 0.2275
    return (f_dp6*l_dp6/D_h)/(2*ro*A_p**2)*x**2

def calc(ensayos):
    result = pd.DataFrame()
    for j in np.arange(len(ensayos)):
        if j==0:
            title='Ensayo 1'
        elif j>0:
            title='Ensayo 2'

        #Fiteo:
        # DP1
        # a_dp1 = (eps_EC)/(2*ro*A_p**2)
        popt1,pcov1=opt.curve_fit(func1,ensayos[j]['Caudal_mean[kg/s]'].values,
                                  ensayos[j]['DP1_mean[bar]'].values * 1E5)
        popt1[0] # perdida de carga EC
        plt.figure()
        plt.ylabel(r'$\Delta$P [Pa]')
        plt.xlabel(r'Caudal [kg/s]')
        plt.title(title)
        plt.grid()
        plt.plot(ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP1_mean[bar]'].values * 1E5,'.r',
                 label='DP1_mean[bar]')
        plt.plot(np.linspace(15,35,num=100),popt1[0]/(2*ro*A_p**2)*np.linspace(15,35,num=100)**2)
        plt.legend()

        # DP4
        # a_dp4 = (f_dp4*l_dp4/D_h)/(2*ro*A_p**2)
        popt2,pcov2=opt.curve_fit(func2,ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP4_mean[bar]'].values * 1E5)
        popt2[0] #friccion distribuida en barras
        plt.figure()
        plt.ylabel(r'$\Delta$P [Pa]')
        plt.xlabel(r'Caudal [kg/s]')
        plt.grid()
        plt.title(title)
        plt.plot(ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP4_mean[bar]'].values * 1E5, '.',
                 label='DP4_mean[bar]')
        plt.plot(np.linspace(15, 35, num=100), (popt2[0]*l_dp4/D_h) / (2 * ro * A_p ** 2) * np.linspace(15, 35, num=100) ** 2)

        # DP6
        # a_dp6 = (f_dp6*l_dp6/D_h)/(2*ro*A_p**2)
        popt6, pcov6 = opt.curve_fit(func6, ensayos[j]['Caudal_mean[kg/s]'].values,
                                     ensayos[j]['DP6_mean[bar]'].values * 1E5)
        popt6[0] #friccion distribuida en barras
        plt.plot(ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP6_mean[bar]'].values * 1E5, '.',
                 label='DP6_mean[bar]')
        plt.plot(np.linspace(15, 35, num=100),
                 (popt6[0] * l_dp6 / D_h) / (2 * ro * A_p ** 2) * np.linspace(15, 35, num=100) ** 2)

        # DP2
        # a_dp2 = (f_dp4*l_dp2/D_h+K_sep1+(A_CE**2-A_p**2)/A_CE**2)/(2*ro*A_p**2)
        popt3,pcov3=opt.curve_fit(lambda x,K_sep1: func3(x,K_sep1,popt2[0]),
                                  ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP2_mean[bar]'].values * 1E5)
        popt3[0] #perdida de carga consentrada del sep1 usando friccion de dp4
        plt.plot(ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP2_mean[bar]'].values * 1E5, '.',
                 label='DP2_mean[bar]')
        plt.plot(np.linspace(15, 35, num=100),
                 (popt2[0] * l_dp2 / D_h+popt3[0]+(A_CE**2-A_p**2)/A_CE**2) / (2 * ro * A_p ** 2) * np.linspace(15, 35, num=100) ** 2)

        # DP3
        # a_dp3 = (f_dp4*l_dp3/D_h+K_sep2y3)/(2*ro*A_p**2)
        popt4, pcov4 = opt.curve_fit(lambda x, K_sep2y3: func4(x, K_sep2y3, popt2[0]),
                                     ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP3_mean[bar]'].values * 1E5)
        popt4[0] #perdida de carga consentrada del sep2y3 usando friccion de dp4
        plt.plot(ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP3_mean[bar]'].values * 1E5, '.',
                 label='DP3_mean[bar]')
        plt.plot(np.linspace(15, 35, num=100),
                 (popt2[0] * l_dp3 / D_h + popt4[0] ) / (2 * ro * A_p ** 2) * np.linspace(15, 35, num=100) ** 2)


        # DP5
        # a_dp5 = (f_dp4*l_dp5/D_h+K_sep4y5)/(2*ro*A_p**2)
        popt5, pcov5 = opt.curve_fit(lambda x, K_sep4y5: func5(x, K_sep4y5, popt2[0]),
                                     ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP5_mean[bar]'].values * 1E5)
        popt5[0] #perdida de carga consentrada del sep4y5 usando friccion de dp4
        plt.plot(ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP5_mean[bar]'].values * 1E5, '.',
                 label='DP5_mean[bar]')
        plt.plot(np.linspace(15, 35, num=100),
                 (popt2[0] * l_dp5 / D_h + popt5[0]) / (2 * ro * A_p ** 2) * np.linspace(15, 35, num=100) ** 2)

        result=result.append({'Eps_EC':popt1[0],'Eps_EC_err':np.sqrt(pcov1[0,0]),'K_sep1':popt3[0],'K_sep1_err':np.sqrt(pcov3[0,0]),
                              'K_sep2y3':popt4[0],'K_sep2y3_err':np.sqrt(pcov4[0,0]),'f_dp4':popt2[0],'f_dp4_err':np.sqrt(pcov2[0,0]),
                              'K_sep4y5':popt5[0],'K_sep4y5_err':np.sqrt(pcov5[0,0]),'f_dp6':popt6[0],'f_dp6_err':np.sqrt(pcov6[0,0])},ignore_index=True)
        plt.legend()
    print(result[['Eps_EC', 'K_sep1', 'K_sep2y3', 'f_dp4', 'K_sep4y5', 'f_dp6']])
    plt.show()
    return result

ensayos=[prom(E1),prom(E2)]
resultados=calc(ensayos)
resultados.to_csv('result_E1y2.csv')

