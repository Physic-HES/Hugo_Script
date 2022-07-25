import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

alpha=0.5
n=2 #submultiplo de muestreo
cR=6/alpha*(2*n)-(2*n-1) #Ciclos reales de oscilacion de la pieza
f_e=800 #Frecuencia de excitacion (= frecuencia modal)
f_o=(1/(2*n)-alpha*4/((8*n)**2-1))*f_e
t=np.linspace(0,1,50000)*cR/f_e
obt=signal.square(2 * np.pi * f_o * t,duty=1/64)+2.25
osc=np.cos(2*np.pi*f_e*t)
osc_m=np.cos(2*np.pi*4*(f_e/(2*n)-f_o)*t+2*64/(f_e))
plt.plot(t,osc,label='Oscilacion real de la pieza')
plt.plot(t[obt-1.25>0],osc[obt-1.25>0],'.',label='Iluminacion')
plt.plot(t,obt,label='Obturacion del laser')
plt.plot(t,osc_m,label='Oscilacion medida')
plt.legend()
print([f_o,f_e,2*np.pi*f_e/(2*n)*alpha/2/500])
plt.figure()
N=np.arange(1,10)
plt.plot(N,40/(1/(2*N)-4*alpha/((8*N)**2-1)),label='Camaras a 40 FPS')
plt.plot(N,60/(1/(2*N)-4*alpha/((8*N)**2-1)),label='Camaras a 60 FPS')
plt.plot(N,90/(1/(2*N)-4*alpha/((8*N)**2-1)),label='Camaras a 90 FPS')
plt.legend()
plt.xlabel('Sub-múltiplo [n]')
plt.ylabel(r'Frecuencia modal máxima $f_e$ [Hz]')
plt.grid()
plt.figure()
px=np.linspace(0,0.014,100)
py=np.ones(100)
pxy_a=np.vstack((px-0.014*1.25-0.014/2,py)).T
pxy_b=np.vstack((px+0.014*1.25-0.014/2,py)).T
fa=[-0.014*1.25,1-2*0.014]
fb=[0.014*1.25,1-2*0.014]
Vpx_a=pxy_a-fa
Vpx_b=pxy_b-fb
x=np.linspace(-(0.014*1.25+0.014/2),0.014*1.25+0.014/2,50)
for j in Vpx_a[:,1]/Vpx_a[:,0]:
    ya=j*(x-fa[0])+fa[1]
    plt.plot(x,ya,'-g',linewidth='0.5')
for j in Vpx_b[:,1]/Vpx_b[:,0]:
    yb=j*(x-fb[0])+fb[1]
    plt.plot(x,yb,'-g',linewidth='0.5')
plt.plot(pxy_a[:,0],pxy_a[:,1],'-r')
plt.plot(pxy_b[:,0],pxy_b[:,1],'-r')
plt.ylim([1-2*0.014,1.2])
plt.xlim([-(0.014*1.25+0.014/2),(0.014*1.25+0.014/2)])
plt.show()