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


def calc(ensayos):
    result = pd.DataFrame()
    for j in np.arange(len(ensayos)):
        #Fiteo:
        # DP1
        # a_dp1 = (eps_EC)/(2*ro*A_p**2)
        DP1fit = np.polyfit(ensayos[j]['Caudal_mean[kg/s]'].values, ensayos[j]['DP1_mean[bar]'].values * 1E5, 2)
        a_dp1 = DP1fit[0]
        eps_EC = a_dp1 * 2 * ro * A_p ** 2  # perdida de carga EC

        # DP4
        # a_dp4 = (f_dp4*l_dp4/D_h)/(2*ro*A_p**2)
        l_dp4=0.2
        DP4fit=np.polyfit(ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP4_mean[bar]'].values*1E5,2)
        a_dp4 =DP4fit[0]
        f_dp4 = a_dp4*2*ro*A_p**2*D_h/l_dp4 #friccion distribuida en barras

        # DP2
        # a_dp2 = (f*l_dp2/D_h+K_sep1+(A_CE**2-A_p**2)/A_CE**2)/(2*ro*A_p**2)
        l_dp2=0.2005
        DP2fit=np.polyfit(ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP1_mean[bar]'].values*1E5,2)
        a_dp2 =DP2fit[0]
        K_sep1 = a_dp2*2*ro*A_p**2-(A_CE**2-A_p**2)/(A_CE**2)-f_dp4*l_dp2/D_h #perdida de carga consentrada del sep1 usando friccion de dp4

        # DP3
        # a_dp3 = (f*l_dp3/D_h+K_sep2+K_sep3)/(2*ro*A_p**2)
        l_dp3=0.456
        DP3fit=np.polyfit(ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP3_mean[bar]'].values*1E5,2)
        a_dp3 = DP3fit[0]
        K_sep2y3 = a_dp3*2*ro*A_p**2-f_dp4*l_dp3/D_h #perdida de carga consentrada del sep2y3 usando friccion de dp4

        # DP5
        # a_dp5 = (f*l_dp5/D_h+K_sep4+K_sep5)/(2*ro*A_p**2)
        l_dp5=0.60475
        DP5fit=np.polyfit(ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP5_mean[bar]'].values*1E5,2)
        a_dp5 = DP5fit[0]
        K_sep4y5 = a_dp5*2*ro*A_p**2-f_dp4*l_dp5/D_h #perdida de carga consentrada del sep4y5 usando friccion de dp4

        # DP6
        # a_dp6 = (f_dp6*l_dp6/D_h)/(2*ro*A_p**2)
        l_dp6=0.2275
        DP6fit=np.polyfit(ensayos[j]['Caudal_mean[kg/s]'].values,ensayos[j]['DP6_mean[bar]'].values*1E5,2)
        a_dp6 =DP6fit[0]
        f_dp6 = a_dp6*2*ro*A_p**2*D_h/l_dp6 #friccion distribuida en barras

        result=result.append({'Eps_EC':eps_EC,'K_sep1':K_sep1,'K_sep2y3':K_sep2y3,
                              'f_dp4':f_dp4,'K_sep4y5':K_sep4y5,'f_dp6':f_dp6},ignore_index=True)
    print(result)
    return result

ensayos=[prom(E1),prom(E2)]
resultados=calc(ensayos)

