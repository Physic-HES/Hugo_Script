import cv2
import numpy as np
import matplotlib.pyplot as plt

frame_0_c = cv2.imread('C:/Users/laboratorio optica/Documents/Hugo_Script/IAMEN/Desarrollos/frame_0.png')
frame_c = cv2.imread('C:/Users/laboratorio optica/Documents/Hugo_Script/IAMEN/Desarrollos/frame.png')
w,h=len(frame_c[0,:]),len(frame_c[:,0])
M=cv2.getRotationMatrix2D((w/2,h/2),1,1)
frame_0_c=cv2.warpAffine(frame_0_c,M,(w,h))
frame_c=cv2.warpAffine(frame_c,M,(w,h))
frame_0_c=cv2.cvtColor(frame_0_c,cv2.COLOR_RGB2GRAY)
frame_c=cv2.cvtColor(frame_c,cv2.COLOR_RGB2GRAY)
frame_0=np.asarray(frame_0_c,dtype=np.float64)
frame=np.asarray(frame_c,dtype=np.float64)
frame_0=frame_0-np.mean(frame_0)
frame=frame-np.mean(frame)

resta_fft=np.fft.fftshift(np.fft.fft2(np.abs(frame-frame_0)))

def normalize(arr, t_min, t_max):
    diff = t_max - t_min
    diff_arr = np.max(np.max(arr)) - np.min(np.min(arr))
    temp = (((arr - np.min(np.min(arr)))*diff)/diff_arr) + t_min
    return temp

D=0.477E6 #distancia total al objetivo en micrones
shift_obj=0.01E6 #distancia real que se corre la hoja milimetrada en micrones
mu=6 # tam de px en micrones
lamb=0.6328
alpha=np.arctan(shift_obj/D)/2
f_0 = np.sin(alpha) / lamb
corr_teo=f_0*mu*len(frame_0[0,:])/2
print(corr_teo)

X,Y=np.meshgrid(range(w),range(h))
escalon=X
escalon=np.where(np.abs(Y-h/2)>48.4363*1.44/1.98,0,1)
escalon=np.where(np.abs(X-w/2)<48.4363,escalon,0)
esc_elipse=X
esc_elipse=np.where(((X-w/2)/48.4363)**2+((Y-h/2)/(48.4363*1.44/1.98))**2<1,1,0)

escalon_fft=np.abs(np.fft.fftshift(np.fft.fft2(escalon)))
esc_elipse_fft=np.abs(np.fft.fftshift(np.fft.fft2(esc_elipse)))
imagen_filt=np.abs(np.fft.ifft2(np.fft.fftshift(esc_elipse*resta_fft)))
gauss=X
Rsq=(X-(w/2+corr_teo))**2+(Y-h/2)**2
R=corr_teo*1.5
c=corr_teo/1.25
gauss=np.where(Rsq<R**2,3E6*np.exp(-1/(2*c**2)*((X-(w/2-corr_teo))**2+(Y-h/2)**2)),0)
imagen_filt2=np.abs(np.fft.ifft2(np.fft.fftshift(gauss*resta_fft)))

plt.imshow(normalize(np.abs(frame-frame_0),0,10),vmax=6)
plt.figure()
plt.plot(np.abs(resta_fft)[int(h/2),:])
plt.plot([int(w/2-corr_teo),int(w/2+corr_teo)],np.abs(resta_fft)[int(h/2),[int(w/2-corr_teo),int(w/2+corr_teo)]],'.r', label='portadora teorica')
plt.figure()
plt.imshow(imagen_filt2)

# filtrado de la imagen de referencia
frame_0Vent = gauss * np.fft.fftshift(np.fft.fft2(frame_0))
frame_0filt = np.fft.ifft2(np.fft.fftshift(frame_0Vent))
fase_frame_0filt = np.angle(frame_0filt)

# filtrado de la imagen de actual
frame_Vent = gauss * np.fft.fftshift(np.fft.fft2(frame))
frame_filt = np.fft.ifft2(np.fft.fftshift(frame_Vent))
fase_frame_filt = np.angle(frame_filt)

# diferencia de fase y fase envuelta
diff_fase=fase_frame_filt-fase_frame_0filt
#diff_fase=normalize(np.angle(frame_filt/frame_0filt),-np.pi,np.pi)
diff_fase_wrap=np.unwrap(diff_fase)

plt.figure()
plt.imshow(diff_fase)
plt.show()

