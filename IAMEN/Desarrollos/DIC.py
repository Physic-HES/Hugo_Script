import cv2
import threading
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft as spy
from scipy import signal as S
from scipy import interpolate as interp
import time

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

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

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID, cv2.CAP_DSHOW)
    cam.set(cv2.CAP_PROP_EXPOSURE, -4) #-4 es 80ms
    w = 752
    h = 480
    zona=48 #tamaño de zonas donde se correlaciona una porcion interior
    div=zona/3
    campo=50 #Cantidad de discretizaciones (discrt)
    print(f'Tamaño de camara: {w}x{h}')
    cam.set(3, w)
    cam.set(4, h)
    if cam.isOpened():  # try to get the first frame
        rval, frame_0 = cam.read()
    else:
        rval = False

    raw_in = 40
    col_in = 150
    discrt = 4
    rgy=range(int(raw_in+zona/2),int(raw_in+zona/2+campo*discrt),int(discrt))
    rgx=range(int(col_in+zona/2),int(col_in+zona/2+campo*discrt),int(discrt))
    map_def_x = np.zeros((len(rgy), len(rgx)))
    map_def_y = np.zeros((len(rgy), len(rgx)))
    map_def = np.zeros((len(rgy), len(rgx)))
    image_stres = np.zeros((h, w))
    while rval:
        rval, frame_ = cam.read()
        frame = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
        time.sleep(0.1)
        rval, frame2_ = cam.read()
        b,g,r=cv2.split(frame2_)
        frame2_RGB=cv2.merge((b,g,r))
        frame2 = cv2.cvtColor(frame2_, cv2.COLOR_BGR2GRAY)
        nn,kk=0,0
        for n in rgy:
            for k in rgx:
                sub_frame_0 = frame[int(n-zona/2):int(n+zona/2),int(k-zona/2):int(k+zona/2)]
                sub_frame_1 = frame2[int(n-zona/2):int(n+zona/2),int(k-zona/2):int(k+zona/2)]
                sub_frame = sub_frame_0[int(div):int(2*div), int(div):int(2*div)]
                a,b,c,sub_int_def=cv2.minMaxLoc(cv2.matchTemplate(sub_frame_1,sub_frame,cv2.TM_CCOEFF_NORMED))
                map_def_x[nn, kk]+=sub_int_def[0]-div
                map_def_y[nn, kk]+=sub_int_def[1]-div
                map_def[nn,kk]=np.sqrt(map_def_x[nn, kk]**2+map_def_y[nn, kk]**2)
                kk+=1
            nn+=1
            kk=0
        if discrt>1:
            mapa=cv2.resize(map_def,(int(campo*discrt),int(campo*discrt)), interpolation =cv2.INTER_AREA)
        else:
            mapa=map_def
        stress_x = (mapa[:-int(discrt),int(discrt):]-mapa[:-int(discrt),:-int(discrt)])/(2*discrt)
        stress_y = (mapa[int(discrt):,:-int(discrt)]-mapa[:-int(discrt),:-int(discrt)])/(2*discrt)
        #stress = np.where(stress_x+stress_y>=0,np.sqrt(stress_x**2+stress_y**2),0)
        #stress = np.where(stress_x+stress_y< 0, -np.sqrt(stress_x ** 2 + stress_y ** 2), stress)
        #stress-=np.min(stress)
        stress=np.sqrt(stress_x**2+stress_y**2)
        #stress=normalize(stress,0,255)
        image_stres[int(raw_in+zona/3+discrt/2):int(raw_in+zona/3+(campo-1)*discrt+discrt/2),
                        int(col_in+zona/3+discrt/2):int(col_in+zona/3+(campo-1)*discrt+discrt/2)]=5*mapa[:-int(discrt),:-int(discrt)]
        stress_color=cv2.applyColorMap(image_stres.astype('uint8'), cv2.COLORMAP_INFERNO)
        merge=cv2.add(frame2_RGB,stress_color)
        cv2.imshow(previewName,merge)
        key = cv2.waitKey(20)
        if key & 0xFF == ord('q'):  # exit on q
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 1", 1)
thread1.start()


