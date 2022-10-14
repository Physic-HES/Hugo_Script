import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

Cobre_0im=cv2.imread('Cobre_balanza_C.png')
Cobre_0im=Cobre_0im[:,:,2].astype('float64')
Cobre_1im=cv2.imread('Cobre_680mgr_C.png')
Cobre_1im=Cobre_1im[:,:,2].astype('float64')
Cobre_2im=cv2.imread('Cobre_1743mgr_C.png')
Cobre_2im=Cobre_2im[:,:,2].astype('float64')
Cobre_3im=cv2.imread('Cobre_2136mgr_C.png')
Cobre_3im=Cobre_3im[:,:,2].astype('float64')
Cobre_4im=cv2.imread('Cobre_4729_C.png')
Cobre_4im=Cobre_4im[:,:,2].astype('float64')

Acero_0im=cv2.imread('Acero_balanza_C.png')
Acero_0im=Acero_0im[:,:,2].astype('float64')
Acero_1im=cv2.imread('Acero_686mgr_C.png')
Acero_1im=Acero_1im[:,:,2].astype('float64')
Acero_2im=cv2.imread('Acero_1743mgr_C.png')
Acero_2im=Acero_2im[:,:,2].astype('float64')
Acero_3im=cv2.imread('Acero_2136mgr_C.png')
Acero_3im=Acero_3im[:,:,2].astype('float64')
Acero_4im=cv2.imread('Acero_4729_C.png')
Acero_4im=Acero_4im[:,:,2].astype('float64')


y=np.linspace(0,0.065,650)
def graf(im,name,offset):
    c=192
    plt.plot(im[:,c],sorted((y-offset)*1E3,reverse=True),label=name)


list_im=[]
list_im.append([Cobre_0im,'balanza'])
list_im.append([Cobre_1im,'680 mgr'])
list_im.append([Cobre_2im,'1743 mgr'])
list_im.append([Cobre_3im,'2136 mgr'])
list_im.append([Cobre_4im,'4729 mgr'])

list2_im=[]
list2_im.append([Acero_0im,'balanza'])
list2_im.append([Acero_1im,'686 mgr'])
list2_im.append([Acero_2im,'1743 mgr'])
list2_im.append([Acero_3im,'2136 mgr'])
list2_im.append([Acero_4im,'4729 mgr'])

def graf_all():
    for u in range(5):
        fig=plt.figure()
        offset1=0.0291
        fig.add_subplot(1,2,2)
        graf(list_im[u][0],list_im[u][1],offset1)
        plt.ylim([np.min(y-offset1)*1E3,np.max(y-offset1)*1E3])
        plt.grid()
        plt.legend()
        plt.ylabel('Distancia [mm]')
        plt.xlabel('Intencidad [$E^2$]')
        plt.title('Perfil de intencidad')
        fig.add_subplot(1,2,1)
        plt.imshow(list_im[u][0],cmap='gist_heat')
        plt.title('Difraccion con ' + list_im[u][1] + ' del Cobre')

        fig2=plt.figure()
        offset2=0.036
        fig2.add_subplot(1,2,2)
        graf(list2_im[u][0],list2_im[u][1],offset2)
        plt.ylim([np.min(y-offset2)*1E3,np.max(y-offset2)*1E3])
        plt.grid()
        plt.legend()
        plt.ylabel('Distancia [mm]')
        plt.xlabel('Intencidad [$E^2$]')
        plt.title('Perfil de intencidad')
        fig2.add_subplot(1,2,1)
        plt.imshow(list2_im[u][0],cmap='gist_heat')
        plt.title('Difraccion con '+list_im[u][1]+' del Acero')

graf_all()

#Carga manual de los minimos de cada grafico
Yp_cobre=np.zeros((4, 2))
Yp_acero=np.zeros((5, 2))
cobre_minim_0=[-0.0229,-0.0154,-0.0077,0,0.0077,0.0152,0.0255,0.0297]
Yp_cobre[0, :]=[np.mean(np.diff(cobre_minim_0)), np.std(np.diff(cobre_minim_0))]
acero_minim_0=[-0.0342,-0.0272,-0.0182,-0.0095,0,0.0091,0.0181,0.0276]
Yp_acero[0, :]=[np.mean(np.diff(acero_minim_0)), np.std(np.diff(acero_minim_0))]
cobre_minim_1=[-.024,-.0194,-.01418,-.0099,-.005,0,.0048,.0091,.0138,.019,.0234,.0285]
Yp_cobre[1, :]=[np.mean(np.diff(cobre_minim_1)), np.std(np.diff(cobre_minim_1))]
acero_minim_1=[-.0293,-.0221,-.0146,-.0076,0,.0074,.0146,.0215]
Yp_acero[1, :]=[np.mean(np.diff(acero_minim_1)), np.std(np.diff(acero_minim_1))]
cobre_minim_2=[-.0213,-.0184,-.0155,-.0122,-.0092,-.006,-.0029,0,.0029,.006,.0091,.0121,.0151,.0185,.0215,.0245,.0275]
Yp_cobre[2, :]=[np.mean(np.diff(cobre_minim_2)), np.std(np.diff(cobre_minim_2))]
acero_minim_2=[-.0229,-.0179,-.0117,-.0062,0,.0055,.0114,.0168,.0227]
Yp_acero[2, :]=[np.mean(np.diff(acero_minim_2)), np.std(np.diff(acero_minim_2))]
cobre_minim_3=[-.019,-.0164,-.0136,-.0107,-.0081-.0056,-.003,0,.0027,.0057,.0082,.0109,.0137,.0163,.0191,.0217,.0246,.0274,.0298]
Yp_cobre[3, :]=[np.mean(np.diff(cobre_minim_3)), np.std(np.diff(cobre_minim_3))]
acero_minim_3=[-.0313,-.0265,-.0214,-.0163,-.0109,-.0056,0,.0052,.0105,.0158,.0207]
Yp_acero[3, :]=[np.mean(np.diff(acero_minim_3)), np.std(np.diff(acero_minim_3))]
acero_minim_4=[-.0253,-.0221,-.0186,-.015,-.0117,-.0076,-.0038,0,.0033,.0069,.0104,.0141,.0181,.0218,.0254]
Yp_acero[4, :]=[np.mean(np.diff(acero_minim_4)), np.std(np.diff(acero_minim_4))]

#Calculo de h con propagacion de errores
h_cobre=np.zeros((len(Yp_cobre[:,0]),2))
h_acero=np.zeros((len(Yp_acero[:,0]),2))
h_cobre[:,0]=1.494 * 670E-9 / Yp_cobre[:, 0]
h_cobre[:,1]=np.sqrt((670E-9 / Yp_cobre[:, 0]*0.001)**2+(1.494 * 670E-9 / Yp_cobre[:, 0]**2*Yp_cobre[:, 1])**2)
h_acero[:,0]=1.494 * 670E-9 / Yp_acero[:, 0]
h_acero[:,1]=np.sqrt((670E-9 / Yp_acero[:, 0]*0.001)**2+(1.494 * 670E-9 / Yp_acero[:, 0]**2*Yp_acero[:, 1])**2)
h_cobre[-1,1]=h_cobre[-1,1]/5

print('Apertura h del Cobre:')
print(h_cobre)
print('Apertura h del Acero:')
print(h_acero)

pesas_cobre=np.zeros((4,2))
pesas_acero=np.zeros((5,2))
pesas_cobre[:,0]=(np.array([0,0.00068,0.001743,0.002136])+0.013979)*9.807
pesas_cobre[:,1]=np.ones((4,))*0.00001*9.807
pesas_acero[:,0]=(np.array([0,0.000686,0.001743,0.002136,0.004729])+0.013979)*9.807
pesas_acero[:,1]=np.ones((5,))*0.00001*9.807

plt.figure()
plt.errorbar(pesas_cobre[:,0], h_cobre[:,0]*1E6,xerr=pesas_cobre[:,1],yerr=h_cobre[:,1]*1E6, fmt='s', label='Defleccion Cobre $h_c=D\lambda/<y_p>_{cobre}$')
plt.errorbar(pesas_acero[:,0], h_acero[:,0]*1E6,xerr=pesas_acero[:,1],yerr=h_acero[:,1]*1E6, fmt='d', label='Defleccion Acero $h_a=D\lambda/<y_p>_{acero}$')
plt.ylabel('Apertura h [$\mu m$]',fontsize=14)
plt.xlabel('Fuerza [$N$]',fontsize=14)
cob_coef=np.polyfit(pesas_cobre[:,0], h_cobre[:,0], 1,full=True)
ace_coef=np.polyfit(pesas_acero[:,0], h_acero[:,0], 1,full=True)
E_cobre=np.zeros((2,))
E_acero=np.zeros((2,))
E_cobre[0]=32*(0.5*0.468**2-0.468**3/3)/(np.pi*(0.00506**4))/cob_coef[0][0]
E_cobre[1]=np.sqrt((32*(0.468**2)/(np.pi*(0.00506**4))/cob_coef[0][0]*0.001)**2+
                   (32*(0.5*0.468*2-0.468**2)/(np.pi*(0.00506**4))/cob_coef[0][0]*0.001)**2+
                   (32*(0.5*0.468**2-0.468**3/3)/(np.pi*(0.00506**5))/cob_coef[0][0]*4*0.00002)**2+
                   (32*(0.5*0.468**2-0.468**3/3)/(np.pi*(0.00506**4))/cob_coef[0][0]**2*np.sqrt(cob_coef[1]/len(cob_coef[0])))**2)
E_acero[0]=32*(0.52*0.464**2-0.464**3/3)/(np.pi*(0.00572**4))/ace_coef[0][0]
E_acero[1]=np.sqrt((32*(0.464**2)/(np.pi*(0.00572**4))/ace_coef[0][0]*0.001)**2+
                   (32*(0.52*0.464*2-0.464**2)/(np.pi*(0.00572**4))/ace_coef[0][0]*0.001)**2+
                   (32*(0.52*0.464**2-0.464**3/3)/(np.pi*(0.00572**5))/ace_coef[0][0]*4*0.00002)**2+
                   (32*(0.52*0.464**2-0.464**3/3)/(np.pi*(0.00572**4))/ace_coef[0][0]**2*np.sqrt(ace_coef[1]/len(ace_coef[0])))**2)
print(f'E_c = {E_cobre[0]/1E9:.4G} +- {E_cobre[1]/1E9:.4G} GPa')
print(f'E_a = {E_acero[0]/1E9:.4G} +- {E_acero[1]/1E9:.4G} GPa')
plt.plot(pesas_cobre[:,0],(cob_coef[0][0]*pesas_cobre[:,0]+cob_coef[0][1])*1E6,label=f'Ajuste Cobre -> $E_c$ = {E_cobre[0]/1E9:.4G} $\pm$ {E_cobre[1]/1E9:.4G} GPa')
plt.plot(pesas_acero[:,0],(ace_coef[0][0]*pesas_acero[:,0]+ace_coef[0][1])*1E6,label=f'Ajuste Acero -> $E_a$ = {E_acero[0]/1E9:.4G} $\pm$ {E_acero[1]/1E9:.4G} GPa')
plt.legend(fontsize=10)
plt.grid()
plt.show()
