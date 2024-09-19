import numpy as np
import matplotlib.pyplot as plt

# Funcion de importacion de datos ya procesados en EDM
def import_EDM(test0,test1,arch):
    carp0 = 'C:\\Users\\user\\Documents\\EECE\\RA 6\\Mediciones en RA-6\\RA6\\Mediciones\\'
    carp1 = 'APS_H_COH_txt'
    dat = np.loadtxt(carp0+test0+'\\'+test1+'\\'+carp1+'\\'+arch,skiprows=27)
    return dat

CC_D10_Z_fi_APS_ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO INCIAL','APS(ch1).txt')
CC_D10_Z_fi_APS_ch2 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO INCIAL','APS(ch2).txt')
CC_D10_Z_fi_APS_ch3 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO INCIAL','APS(ch3).txt')
CC_D10_Z_fi_APS_ch4 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO INCIAL','APS(ch4).txt')

CC_D10_Z_ff_APS_ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO FINAL','APS(ch1).txt')
CC_D10_Z_ff_APS_ch2 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO FINAL','APS(ch2).txt')
CC_D10_Z_ff_APS_ch3 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO FINAL','APS(ch3).txt')
CC_D10_Z_ff_APS_ch4 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','FONDO FINAL','APS(ch4).txt')

CC_D10_Z_fd_APS_ch1 = np.c_[CC_D10_Z_fi_APS_ch1[:,0],np.abs(np.sqrt(2*CC_D10_Z_ff_APS_ch1[:,1])-np.sqrt(2*CC_D10_Z_fi_APS_ch1[:,1]))]
CC_D10_Z_fd_APS_ch2 = np.c_[CC_D10_Z_fi_APS_ch2[:,0],np.abs(np.sqrt(2*CC_D10_Z_ff_APS_ch2[:,1])-np.sqrt(2*CC_D10_Z_fi_APS_ch2[:,1]))]
CC_D10_Z_fd_APS_ch3 = np.c_[CC_D10_Z_fi_APS_ch3[:,0],np.abs(np.sqrt(2*CC_D10_Z_ff_APS_ch3[:,1])-np.sqrt(2*CC_D10_Z_fi_APS_ch3[:,1]))]
CC_D10_Z_fd_APS_ch4 = np.c_[CC_D10_Z_fi_APS_ch4[:,0],np.abs(np.sqrt(2*CC_D10_Z_ff_APS_ch4[:,1])-np.sqrt(2*CC_D10_Z_fi_APS_ch4[:,1]))]

CC_D10_Z_fp_APS_ch1 = np.c_[CC_D10_Z_fi_APS_ch1[:,0],1/2*(np.sqrt(2*CC_D10_Z_ff_APS_ch1[:,1])+np.sqrt(2*CC_D10_Z_fi_APS_ch1[:,1]))]
CC_D10_Z_fp_APS_ch2 = np.c_[CC_D10_Z_fi_APS_ch2[:,0],1/2*(np.sqrt(2*CC_D10_Z_ff_APS_ch2[:,1])+np.sqrt(2*CC_D10_Z_fi_APS_ch2[:,1]))]
CC_D10_Z_fp_APS_ch3 = np.c_[CC_D10_Z_fi_APS_ch3[:,0],1/2*(np.sqrt(2*CC_D10_Z_ff_APS_ch3[:,1])+np.sqrt(2*CC_D10_Z_fi_APS_ch3[:,1]))]
CC_D10_Z_fp_APS_ch4 = np.c_[CC_D10_Z_fi_APS_ch4[:,0],1/2*(np.sqrt(2*CC_D10_Z_ff_APS_ch4[:,1])+np.sqrt(2*CC_D10_Z_fi_APS_ch4[:,1]))]

CC_D10_Z_APS_ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','APS(ch1).txt')
CC_D10_Z_APS_ch2 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','APS(ch2).txt')
CC_D10_Z_APS_ch3 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','APS(ch3).txt')
CC_D10_Z_APS_ch4 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','APS(ch4).txt')

CC_D10_Z_H_ch2ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','H(ch2,ch1).txt')
CC_D10_Z_H_ch3ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','H(ch3,ch1).txt')
CC_D10_Z_H_ch4ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','H(ch4,ch1).txt')

CC_D10_Z_COH_ch2ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','COH(ch2,ch1).txt')
CC_D10_Z_COH_ch3ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','COH(ch3,ch1).txt')
CC_D10_Z_COH_ch4ch1 = import_EDM('10-7-24 CAMION POR CALLE DE AFUERA SOLO EN Z','EXCITACION','COH(ch4,ch1).txt')

plt.figure()
plt.plot(CC_D10_Z_fp_APS_ch1[:,0],CC_D10_Z_fp_APS_ch1[:,1],label='CC_D10_Z_fp_APS_ch1')
plt.plot(CC_D10_Z_fp_APS_ch2[:,0],CC_D10_Z_fp_APS_ch2[:,1],label='CC_D10_Z_fp_APS_ch2')
plt.plot(CC_D10_Z_fp_APS_ch3[:,0],CC_D10_Z_fp_APS_ch3[:,1],label='CC_D10_Z_fp_APS_ch3')
plt.plot(CC_D10_Z_fp_APS_ch4[:,0],CC_D10_Z_fp_APS_ch4[:,1],label='CC_D10_Z_fp_APS_ch4')
plt.legend()
plt.title('Espectro de Fondo Promedio - Ensayo Camión Calle')
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'Auto Power Spectrum [$(m/s^2)$ 0-peak]')

plt.figure()
plt.plot(CC_D10_Z_fd_APS_ch1[:,0],CC_D10_Z_fd_APS_ch1[:,1],label='CC_D10_Z_fd_APS_ch1')
plt.plot(CC_D10_Z_fd_APS_ch2[:,0],CC_D10_Z_fd_APS_ch2[:,1],label='CC_D10_Z_fd_APS_ch2')
plt.plot(CC_D10_Z_fd_APS_ch3[:,0],CC_D10_Z_fd_APS_ch3[:,1],label='CC_D10_Z_fd_APS_ch3')
plt.plot(CC_D10_Z_fd_APS_ch4[:,0],CC_D10_Z_fd_APS_ch4[:,1],label='CC_D10_Z_fd_APS_ch4')
plt.legend()
plt.title('Diferencia Absoluta en Espectros de Fondo - Ensayo Camión Calle')
plt.xlabel('Frequency [Hz]')
plt.ylim([-7.5E-6,1.63E-4])
plt.ylabel(r'Auto Power Spectrum [$(m/s^2)$ 0-peak]')

plt.figure()
plt.plot(CC_D10_Z_APS_ch1[:,0],np.sqrt(2*CC_D10_Z_APS_ch1[:,1]),label='CC_D10_Z_APS_ch1')
plt.plot(CC_D10_Z_APS_ch2[:,0],np.sqrt(2*CC_D10_Z_APS_ch2[:,1]),label='CC_D10_Z_APS_ch2')
plt.plot(CC_D10_Z_APS_ch3[:,0],np.sqrt(2*CC_D10_Z_APS_ch3[:,1]),label='CC_D10_Z_APS_ch3')
plt.plot(CC_D10_Z_APS_ch4[:,0],np.sqrt(2*CC_D10_Z_APS_ch4[:,1]),label='CC_D10_Z_APS_ch4')
plt.legend()
plt.title('APS Durante Excitacion - Ensayo Camión Calle')
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'Auto Power Spectrum [$(m/s^2)$ 0-peak]')

plt.figure()
plt.plot(CC_D10_Z_H_ch2ch1[:,0],np.sqrt(CC_D10_Z_H_ch2ch1[:,1]**2+CC_D10_Z_H_ch2ch1[:,2]**2),label='CC_D10_Z_H_ch2ch1')
plt.plot(CC_D10_Z_H_ch3ch1[:,0],np.sqrt(CC_D10_Z_H_ch3ch1[:,1]**2+CC_D10_Z_H_ch3ch1[:,2]**2),label='CC_D10_Z_H_ch3ch1')
plt.plot(CC_D10_Z_H_ch4ch1[:,0],np.sqrt(CC_D10_Z_H_ch4ch1[:,1]**2+CC_D10_Z_H_ch4ch1[:,2]**2),label='CC_D10_Z_H_ch4ch1')
plt.legend()
plt.title('Funcion de Transferencia Durante Excitacion - Ensayo Camión Calle')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Transfer Factor')

plt.figure()
plt.plot(CC_D10_Z_COH_ch2ch1[:,0],CC_D10_Z_COH_ch2ch1[:,1],label='CC_D10_Z_COH_ch2ch1')
plt.plot(CC_D10_Z_COH_ch3ch1[:,0],CC_D10_Z_COH_ch3ch1[:,1],label='CC_D10_Z_COH_ch3ch1')
plt.plot(CC_D10_Z_COH_ch4ch1[:,0],CC_D10_Z_COH_ch4ch1[:,1],label='CC_D10_Z_COH_ch4ch1')
plt.legend()
plt.title('Funcion de Coherencia Durante Excitacion - Ensayo Camion Calle')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Coherence Factor')


sismo = np.loadtxt('SRS_.txt',delimiter='\t')
sismo_interp = np.interp(CC_D10_Z_H_ch2ch1[:,0],sismo[:,0],sismo[:,1],left=0.05,right=0.05)

plt.figure()
plt.plot(CC_D10_Z_H_ch2ch1[:,0],np.sqrt(CC_D10_Z_H_ch2ch1[:,1]**2+CC_D10_Z_H_ch2ch1[:,2]**2)*sismo_interp,label='CC_D10_Z_R_ch2ch1')
plt.plot(CC_D10_Z_H_ch3ch1[:,0],np.sqrt(CC_D10_Z_H_ch3ch1[:,1]**2+CC_D10_Z_H_ch3ch1[:,2]**2)*sismo_interp,label='CC_D10_Z_R_ch3ch1')
plt.plot(CC_D10_Z_H_ch4ch1[:,0],np.sqrt(CC_D10_Z_H_ch4ch1[:,1]**2+CC_D10_Z_H_ch4ch1[:,2]**2)*sismo_interp,label='CC_D10_Z_R_ch4ch1')
plt.plot(CC_D10_Z_H_ch2ch1[:,0],sismo_interp,label='Sismo')
plt.legend()
plt.title('Respuesta a un Sismo según Funcion de Transferencia Obtenida de Ensayo Camión Calle')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Aceleracion [G]')

print(CC_D10_Z_APS_ch1.shape)

plt.show()