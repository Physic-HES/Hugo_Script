import cv2
import numpy as np
from scipy import signal as S
import matplotlib.pyplot as plt

def shift(im_ref):
    im_ref_=im_ref-np.mean(im_ref)
    R = S.correlate(im_ref_, im_ref_, mode='same', method='fft')
    R = R - np.min(np.min(R))
    R = R / np.max(np.max(R))
    difR = np.abs(np.diff(np.diff(R)))
    difR = difR / np.max(np.max(difR))
    prom = np.mean(((difR ** 2 + difR[::-1] ** 2) / 2) ** 2, axis=0)
    prom = prom[1023:]
    mask2 = np.ones(np.shape(prom))
    mask2[0:12] = 0
    return np.argmax(prom*mask2)-1


path_IM='C:/Users/laboratorio optica/Documents/Hugo/shearography/calib/'
file='corr_1cm.bmp'
IM = plt.imread(path_IM+file)
gray = frame=cv2. cvtColor(IM, cv2. COLOR_BGR2GRAY)
gray_=gray-np.mean(gray)
R=S.correlate(gray_,gray_,mode='same',method='fft')
#tam_col=len(gray_[0,:])
#tam_raw=len(gray_[:,0])
#X,Y=np.meshgrid(np.arange(tam_col),np.arange(tam_raw))
#mask=1-np.exp(-1/(2*5)*((X-1024)**2+(Y-1024)**2))
R=R-np.min(np.min(R))
R=R/np.max(np.max(R))
difR=np.abs(np.diff(np.diff(R)))
difR=difR/np.max(np.max(difR))
#R_=R1*mask
plt.imshow(np.log((difR**2+difR[::-1]**2)/2+1),vmax=0.01)
plt.figure()
prom=np.mean(((difR**2+difR[::-1]**2)/2)**2,axis=0)
prom=prom[1023:]
mask2=np.ones(np.shape(prom))
mask2[0:12]=0
plt.plot(prom*mask2)
print(shift(gray))
plt.show()

