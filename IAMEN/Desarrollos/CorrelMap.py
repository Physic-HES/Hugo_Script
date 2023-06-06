import cv2
import  numpy as np

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

cam=cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cam.set(cv2.CAP_PROP_EXPOSURE,-1)
print(cam)
rval, frame0=cam.read()
frame0_BW=cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)
(thresh, frame0) = cv2.threshold(frame0_BW, 10, 255, cv2.THRESH_BINARY)
while rval:
    rval, frame=cam.read()
    frame_BW = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (thresh, frame_BW) = cv2.threshold(frame_BW, 10, 255, cv2.THRESH_BINARY)
    cross = np.fft.fftshift(np.fft.fft2(frame_BW)/np.abs(np.fft.fft2(frame_BW))*np.conjugate(np.fft.fft2(frame0_BW))/np.abs(np.fft.fft2(frame0_BW)))
    map = np.arctan2(np.imag(cross),np.real(cross))
    map = map-np.min(map)
    map = (map*255/np.max(map)).astype('uint8')
    map_BGR = cv2.cvtColor(map,cv2.COLOR_GRAY2BGR)
    map_turbo=cv2.applyColorMap(map_BGR, cv2.COLORMAP_TURBO)
    cv2.imshow('camara',rescale_frame(map_turbo,50))
    if cv2.waitKey(10) == 's':
        break
