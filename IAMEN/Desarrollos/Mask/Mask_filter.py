import numpy as np
import matplotlib.pyplot as plt
import cv2

def normalize(arr, t_min, t_max):
    diff = t_max - t_min
    diff_arr = np.max(np.max(arr)) - np.min(np.min(arr))
    temp = (((arr - np.min(np.min(arr)))*diff)/diff_arr) + t_min
    return temp

A=plt.imread('/home/hp1opticaiamend/Documents/Macks/A-Negra.jpg')
Cartel=plt.imread('/home/hp1opticaiamend/Documents/Macks/Cartel.png')
C=plt.imread('/home/hp1opticaiamend/Documents/Macks/C3.jpg')
A=cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
C=cv2.cvtColor(C, cv2.COLOR_BGR2GRAY)
C_=cv2.resize(C, (1200,1200), interpolation =cv2.INTER_AREA)
cv2.imshow('cartel',C_)
cv2.destroyAllWindows()
det=np.abs(np.fft.ifft2(np.fft.ifftshift(np.abs(np.fft.fftshift(np.fft.fft2(255-A)))*np.fft.fftshift(np.fft.fft2(C_)))))
det=1-normalize(det,0,1)
plt.imshow(det)
plt.figure()
P=np.where(det==np.max(det))
print(P)
plt.imshow(C_)
plt.plot(P[1],P[0],'.')
plt.show()
