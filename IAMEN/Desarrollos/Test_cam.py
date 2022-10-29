import cv2
import numpy as np
from scipy import signal as S
import matplotlib.pyplot as plt

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_EXPOSURE,-4)
cam.set(3,2048)
cam.set(4,2048)
rval, frame = cam.read()
#frame = rescale_frame(frame, percent=25)
frame=cv2. cvtColor(frame, cv2. COLOR_BGR2GRAY)
tam_col=len(frame[0,:])
tam_raw=len(frame[:,0])
print([tam_raw,tam_col])
X,Y=np.meshgrid(np.arange(tam_col),np.arange(tam_raw))
mask=np.zeros((tam_raw,tam_col))
for k in range(tam_raw):
    for j in range(tam_col):
        if (k-(np.floor(tam_raw/2)-10))**2+(j-np.floor(tam_col/2))**2<35**2:
            mask[k,j]=1
#frame1 = rescale_frame(frame, percent=50)
#frame_autocorrel=S.correlate(frame,frame, mode='same', method='fft')
#plt.plot(frame_autocorrel[int(len(frame[:,0])/2),:])
#plt.imshow(frame_autocorrel/np.max(np.max(frame_autocorrel)))
#plt.imshow(frame)
#plt.show()
CCF=np.angle(np.fft.ifft2(np.conj(np.fft.fft2(mask*frame))*np.fft.fft2(mask*frame)))
print(np.argmax(CCF[int(tam_raw/2),970:1050]**2))
plt.plot(CCF[int(tam_raw/2),:])
plt.figure()
plt.imshow(frame)
plt.show()
#cv2.imshow('salida',np.abs(np.fft.ifft2(np.conj(np.fft.fft2(frame))*np.fft.fft2(frame)))/np.max(np.max(np.abs(np.fft.ifft2(np.conj(np.fft.fft2(frame))*np.fft.fft2(frame)))))*5)
#cv2.waitKey(0)
#cv2.destroyWindow('salida')
