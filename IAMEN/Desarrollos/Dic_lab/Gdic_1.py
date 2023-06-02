import numpy as np
import matplotlib.pyplot as plt
import cv2
import time


class Mesh:
    def __init__(self,roi,step):
        self.roi=[np.array(roi[0]),
                  np.array(roi[1]),
                  np.array(roi[2]),
                  np.array(roi[3])]
        self.step=step
        self.dot_x=range(self.roi[0][1], self.roi[3][1], self.step)
        self.dot_y=range(self.roi[0][0], self.roi[3][0], self.step)
        self.form=(len(self.dot_y),len(self.dot_x))
        h = 0
        for k in self.dot_y:
            for u in self.dot_x:
                if h == 0:
                    self.ptos = np.array([k, u])
                else:
                    self.ptos = np.vstack((self.ptos, np.array([k, u])))
                h += 1
        self.Def = np.zeros(self.ptos.shape)
        self.im_x = np.zeros(self.form)
        self.im_y = np.zeros(self.form)
        self.im_xy = np.zeros(self.form)

    def update(self,Def):
        self.ptos += Def
        self.Def += Def
        h=0
        for k in range(self.im_x.shape[0]):
            for u in range(self.im_x.shape[1]):
                self.im_x[k, u] = Def[h,0]
                self.im_y[k, u] = Def[h, 1]
                self.im_xy[k, u] = np.sqrt(Def[h, 0]**2+Def[h, 1]**2)
                h+=1




roi=[[10,10],[10,1000],[500,10],[500,1000]]
step=23
mesh1=Mesh(roi,step)
ptos0,Def0=mesh1.ptos,mesh1.Def
im0=np.zeros((510,1010,3))
for j in range(ptos0.shape[0]):
    cv2.circle(im0,(ptos0[j,:][1],ptos0[j,:][0]),1,(0,255,0),-1)

im_=mesh1.im_x
print()
cv2.imshow('Mesh',im_)
cv2.waitKey(0)