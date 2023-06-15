import numpy as np
import cv2
from scipy.interpolate import  griddata
import matplotlib.pyplot as plt
import time


class Mesh:
    def __init__(self,roi,step,box):
        self.roi=[np.array(roi[0]),
                  np.array(roi[1]),
                  np.array(roi[2]),
                  np.array(roi[3])]
        self.step=step
        self.box=box
        self.dot_x=range(self.roi[0][1], self.roi[3][1], self.step)
        self.dot_y=range(self.roi[0][0], self.roi[3][0], self.step)
        self.form=(len(self.dot_y),len(self.dot_x))
        h = 0
        for k in self.dot_y:
            for u in self.dot_x:
                if h == 0:
                    self.ptos_0 = np.array([k, u])
                else:
                    self.ptos_0 = np.vstack((self.ptos_0, np.array([k, u])))
                h += 1
        self.Def = np.zeros(self.ptos_0.shape)
        self.ptos = self.ptos_0.copy()
        self.im_x = np.zeros(self.form)
        self.im_y = np.zeros(self.form)
        self.im_xy = np.zeros(self.form)
        self.im_dx = np.zeros(self.form)
        self.im_dy = np.zeros(self.form)
        self.im_dxy = np.zeros(self.form)

    def update(self,Def):
        self.ptos += Def
        self.Def += Def
        h=0
        for k in range(self.im_x.shape[0]):
            for u in range(self.im_x.shape[1]):
                self.im_x[k, u] = self.Def[h, 1]
                self.im_y[k, u] = self.Def[h, 0]
                self.im_xy[k, u] = np.sqrt(self.Def[h, 1]**2+self.Def[h, 0]**2)
                h+=1
        self.im_dx = cv2.Sobel(self.im_x, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        self.im_dy = cv2.Sobel(self.im_y, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        self.im_dxy = cv2.add(self.im_dx,self.im_dy)

    def get_def(self,Im_old,Im_new):
        g=0
        for k in range(self.ptos_0.shape[0]):
            Old_set = Im_old[int(self.ptos[k,0]-self.box):int(self.ptos[k,0]+self.box),
                             int(self.ptos[k,1]-self.box):int(self.ptos[k,1]+self.box)]
            New_set = Im_new[int(self.ptos[k,0]-self.box):int(self.ptos[k,0]+self.box),
                             int(self.ptos[k,1]-self.box):int(self.ptos[k,1]+self.box)]
            mask = Old_set[int(self.box/4):int(self.box*3/4),int(self.box/4):int(self.box*3/4)]
            a,b,c,sub_int_def=cv2.minMaxLoc(cv2.matchTemplate(New_set,mask,cv2.TM_CCOEFF_NORMED))
            vecc=np.array([int(sub_int_def[1]-self.box/4),int(sub_int_def[0]-self.box/4)])
            if np.linalg.norm(vecc)>0:
                vec=vecc
            else:
                vec=np.array([int(0),int(0)])
            if g==0:
                Def=vec
            else:
                Def=np.vstack((Def,vec))
            g+=1
        self.update(Def)

    def get_lienso(self,Im,type='XY'):
        lienso = np.zeros((Im.shape[0],Im.shape[1]))
        dim=(self.roi[3][1]-self.roi[2][1],self.roi[2][0]-self.roi[0][0])
        if type=='X':
            rescale=cv2.resize(cv2.convertScaleAbs(self.im_x),dim, interpolation =cv2.INTER_CUBIC)
        elif type=='Y':
            rescale = cv2.resize(cv2.convertScaleAbs(self.im_y),dim, interpolation =cv2.INTER_CUBIC)
        elif type=='XY':
            rescale = cv2.resize(cv2.convertScaleAbs(self.im_xy),dim, interpolation =cv2.INTER_CUBIC)
        elif type=='dX':
            rescale = cv2.resize(cv2.convertScaleAbs(self.im_dx), dim, interpolation=cv2.INTER_CUBIC)
        elif type == 'dY':
            rescale = cv2.resize(cv2.convertScaleAbs(self.im_dy), dim, interpolation=cv2.INTER_CUBIC)
        elif type == 'dXY':
            rescale = cv2.resize(cv2.convertScaleAbs(self.im_dxy), dim, interpolation=cv2.INTER_CUBIC)
        lienso[self.roi[0][0]:self.roi[3][0],self.roi[0][1]:self.roi[3][1]]=rescale
        gridx,gridy=np.mgrid[0:lienso.shape[0]-1:lienso.shape[0]*1j,0:lienso.shape[1]-1:lienso.shape[1]*1j]
        gridz=(griddata(self.ptos,self.ptos_0,(gridx,gridy),method='linear')).astype('float32')
        lienso_def=cv2.remap(lienso,gridz[:,:,1],gridz[:,:,0],cv2.INTER_LINEAR)
        return lienso_def


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


#plt.ion()
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cam.set(cv2.CAP_PROP_EXPOSURE,-1)
rval,frame0=cam.read()
frame=np.zeros(frame0.shape)
frame0_BW=cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)
lowlim=100
uplim=255
(thresh, frame0_BW) = cv2.threshold(frame0_BW, lowlim, uplim, cv2.THRESH_BINARY)
margen=600
roi=[[int(margen/2),margen],[int(margen/2),frame0.shape[1]-margen],[frame0.shape[0]-int(margen/2),margen],[frame0.shape[0]-int(margen/2),frame0.shape[1]-margen]]
step=32
box=120
mesh=Mesh(roi,step,box)
print(f'Cantidad de puntos de seguimiento: {mesh.ptos.shape[0]}')
while rval:
    rval,frame=cam.read()
    frame_BW = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (thresh, frame_BW) = cv2.threshold(frame_BW, lowlim, uplim, cv2.THRESH_BINARY)
    mesh.get_def(frame0_BW,frame_BW)
    im_def_BW=(mesh.get_lienso(frame_BW,'XY')*5).astype('uint8')
    im_def=cv2.cvtColor(im_def_BW,cv2.COLOR_GRAY2BGR)
    im_def_cmap=cv2.applyColorMap(im_def, cv2.COLORMAP_TURBO)
    frame2=cv2.addWeighted(frame,0.5,im_def_cmap,0.5,0.0)
    for j in range(mesh.ptos.shape[0]):
        cv2.circle(frame2,(mesh.ptos[j,1],mesh.ptos[j,0]),2,(0,0,0),-1)
    cv2.imshow('def',rescale_frame(frame2,50))
    frame0_BW=frame_BW
    if cv2.waitKey(10) == 's':
        break