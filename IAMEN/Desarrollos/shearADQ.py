#Generic Simult cams:
import cv2
import threading
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as spy
from scipy import signal as S


def interes(im):
    tam_col = len(im[0, :])
    tam_raw = len(im[:, 0])
    X, Y = np.meshgrid(np.arange(tam_col), np.arange(tam_raw))
    Z = (X-(tam_col/2-40))**2+(Y-(tam_raw/2))**2
    R = 75/100*tam_raw/2
    vent_interes = np.where(Z < R**2, 1, 0)
    return vent_interes


def vent(im,corr):
    tam_col = len(im[0, :])
    tam_raw = len(im[:, 0])
    X, Y = np.meshgrid(np.arange(tam_col), np.arange(tam_raw))
    a = tam_col / 2
    b = tam_raw / 2
    c2=100/3
    gauss = np.exp(-1 / 2 * (((X - (a + corr + 4)) / (1.75 * c2)) ** 2 + ((Y - b) / c2) ** 2))
    gauss = np.where(((X - (a + corr + 4)) / (1.75 * (c2 * 1.5))) ** 2 + ((Y - b) / (c2 * 1.5)) ** 2 < 1, gauss, 0)
    return gauss

def shift(im_ref):
    im_ref_=im_ref-np.mean(im_ref)
    R = S.correlate(im_ref_, im_ref_, mode='same', method='fft')
    R = R - np.min(np.min(R))
    R = R / np.max(np.max(R))
    difR = np.abs(np.diff(np.diff(R)))
    difR = difR / np.max(np.max(difR))
    prom = np.mean(((difR ** 2 + difR[::-1] ** 2) / 2) ** 2, axis=0)
    prom = prom[int(len(im_ref[0,:])/2-1):]
    mask2 = np.ones(np.shape(prom))
    mask2[0:int(12/1024*len(im_ref[0,:]))] = 0
    if np.isnan(np.argmax(prom*mask2)-1):
        ret=44
    else:
        ret=np.argmax(prom*mask2)-1
    return ret

def port(im0):
    R=spy.fftshift(spy.fft2(np.abs(im0)))
    R=np.abs(R)
    difR = np.abs(np.diff(np.diff(R)))
    difR = difR / np.max(np.max(difR))
    prom = np.mean(((difR ** 2 + difR[::-1] ** 2) / 2) ** 2, axis=0)
    prom = prom[int(len(R[0,:])/2-1):]
    mask2 = np.ones(np.shape(prom))
    mask2[0:int(76/742*len(R[0,:]))] = 0
    if np.isnan(np.argmax(prom*mask2)+2) or np.argmax(prom*mask2)+2<25:
        ret=30
    else:
        ret=np.argmax(prom*mask2)+2
    return ret

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# explicit function to normalize array
def normalize(arr, t_min, t_max):
    diff = t_max - t_min
    diff_arr = np.max(np.max(arr)) - np.min(np.min(arr))
    temp = (((arr - np.min(np.min(arr)))*diff)/diff_arr) + t_min
    return temp

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

#HACER UNA FUNCION CALIBRECION:
    #D=0.477E6 #distancia total al objetivo en micrones <--- PONER VALOR CORRECTO
    #shift_ref=shift(frame_0) #numero de pixeles de shift en imagen de referencia
    #shift_ref=62
    #print(r'shift_ref: %g'%shift_ref)
    #shift_obj=0.01E6 #distancia real que se corre la hoja milimetrada en micrones
    #mu=6 # tam de px en micrones
    #foco_cam=shift_ref*mu*D/shift_obj
    # CALIBRACION


def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_EXPOSURE, -5)
    w = 2048
    h = 2048
    print(f'Tamaño de camara: {w}x{h}')
    cam.set(3, w)
    cam.set(4, h)
    rec=[int(h/2-768/2),int(h/2+768/2),int(w/2-1024/2),int(w/2+1024/2)]
    if cam.isOpened():  # try to get the first frame
        rval, frame_0 = cam.read()
        g,b,r=cv2.split(frame_0)
        frame_0=r
        frame_0=np.asarray(frame_0,dtype=np.float64)
        frame_0=frame_0[rec[0]:rec[1],rec[2]:rec[3]]
    else:
        rval = False

    lamb=0.6328
    D = 0.477E6
    shift_obj = 0.01E6
    mu = 6
    # hACER FUNCION VENTANA CON ESTO
    alpha=np.arctan(shift_obj/D)
    f_0 = np.sin(alpha) / lamb
    corr_teo=len(frame_0[0,:])/2+f_0*len(frame_0[0,:])*mu
    corr=port(frame_0)
    print(f'alpha: {alpha}')
    print(f'f_0 [1/micron]: {f_0}')
    print(f'Periodo de portadora en pixeles: {1/(f_0*mu)}')
    print(f'pixeles corridos teorico: {corr_teo}')
    print(f'pixeles corridos en la practica: {corr}')

    while rval:
        rval, frame = cam.read()
        g, b, r = cv2.split(frame)
        frame = r
        frame=np.asarray(frame,dtype=np.float64)
        frame = frame[rec[0]: rec[1], rec[2]: rec[3]]
        corr = port(frame)
        gauss = vent(frame,corr)

        # filtrado de la imagen de referencia
        frame_0Vent = gauss * spy.fftshift(spy.fft2(frame_0))
        frame_0filt = spy.ifft2(spy.ifftshift(frame_0Vent))
        fase_frame_0filt = np.angle(frame_0filt)

        # filtrado de la imagen de actual
        frame_Vent = gauss * spy.fftshift(spy.fft2(frame))
        frame_filt = spy.ifft2(spy.ifftshift(frame_Vent))
        fase_frame_filt = np.angle(frame_filt)

        # diferencia de fase y fase desenvuelta
        diff_fase=fase_frame_filt-fase_frame_0filt
        diff_fase=(diff_fase+np.pi)%(2*np.pi)
        diff_fase_unwrap=np.unwrap(diff_fase)

        # imagenes para plotear
        res=normalize(np.abs(frame-frame_0),0,1)
        frame_filt = np.abs(spy.ifft2(spy.ifftshift(gauss * spy.fftshift(spy.fft2(frame)))))
        transfft2=np.abs(spy.fftshift(spy.fft2(frame)))
        transfft = normalize(np.log2(transfft2 + 1), 0, 1)
        mask=normalize(np.log2(gauss+1),0,1)
        superp=cv2.merge((transfft,transfft,mask))
        unwrapped=normalize(diff_fase_unwrap,0,1)
        cap=normalize(frame,0,1)

        # plot
        cv2.imshow(previewName, cap)
        cv2.imshow('Resta', res)
        cv2.imshow('Transformada y mascara de la imagen deformada', superp)
        cv2.imshow('Imagen con carga filt',normalize(frame_filt,0,1))
        cv2.imshow('Fase envuelta', normalize(diff_fase,0,1))
        cv2.imshow('Fase desenvuelta',unwrapped)
        key = cv2.waitKey(20)
        if key & 0xFF == ord('q'):  # exit on q
            plt.imsave('frame_0.png',frame_0)
            plt.imsave('frame.png', frame)
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 1", 1)
thread1.start()