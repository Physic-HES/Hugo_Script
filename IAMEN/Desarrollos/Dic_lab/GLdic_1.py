import numpy as np
import cv2
from scipy.interpolate import  griddata
import matplotlib.pyplot as plt
import time
import os
from tqdm import tqdm
import imageio

def get_DyDp(forma,P_new,P_old,k):
    P_old=np.c_[P_old[:,1],P_old[:,0]]
    P_new=np.c_[P_new[:,1],P_new[:,0]]
    old_pts=np.array([P_old[k-forma[1]-1,:],P_old[k-forma[1],:],P_old[k-1,:]]).astype('float32')
    new_pts=np.array([P_new[k-forma[1]-1,:],P_new[k-forma[1],:],P_new[k-1,:]]).astype('float32')
    M1=cv2.getAffineTransform(old_pts,new_pts)
    old_pts=np.array([P_old[k,:],P_old[k-forma[1],:],P_old[k-1,:]]).astype('float32')
    new_pts=np.array([P_new[k,:],P_new[k-forma[1],:],P_new[k-1,:]]).astype('float32')
    M2=cv2.getAffineTransform(old_pts,new_pts)
    M=(M1+M2)/2
    D=M[:,2].T
    dudx=np.array(M[0,0])
    dudy=np.array(M[0,1])
    dvdx=np.array(M[1,0])
    dvdy=np.array(M[1,1])
    Dp=np.array([dudx,dudy,dvdx,dvdy])
    P=np.concatenate((D,Dp))
    return P

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
        self.ptos = self.ptos.astype('float64')
        self.im_x = np.zeros(self.form)
        self.im_y = np.zeros(self.form)
        self.im_xy = np.zeros(self.form)
        self.im_dudx = np.zeros((self.form[0]-1,self.form[1]-1))
        self.im_dudy = np.zeros((self.form[0]-1,self.form[1]-1))
        self.im_dvdx = np.zeros((self.form[0]-1,self.form[1]-1))
        self.im_dvdy = np.zeros((self.form[0]-1,self.form[1]-1))
        self.GetExtens = 0
        self.extens_dots = []
        self.extens_desp = []
        self.extens_strain = []
        self.type_def = 'Y'


    def get_def(self,Im_old,Im_new):
        old_ptos=self.ptos_0.copy()
        new_ptos=self.ptos.copy()
        dots=self.ptos.astype('int')
        pbar = tqdm(total=self.ptos_0.shape[0], desc=f'Correlacionando mascaras de {self.box/3:.0}x{self.box/3:.0}...')
        for n in range(self.form[1]):
            Old_set = Im_old[int(dots[n,0]-self.box):int(dots[n,0]+self.box),
                             int(dots[n,1]-self.box):int(dots[n,1]+self.box)]
            New_set = Im_new[int(dots[n,0]-self.box):int(dots[n,0]+self.box),
                             int(dots[n,1]-self.box):int(dots[n,1]+self.box)]
            mask = Old_set[int(self.box/4):int(self.box*3/4),int(self.box/4):int(self.box*3/4)]
            a,b,c,sub_int_def=cv2.minMaxLoc(cv2.matchTemplate(New_set,mask,cv2.TM_CCOEFF_NORMED))
            vecc=np.array([int(sub_int_def[1]-self.box/4),int(sub_int_def[0]-self.box/4)])
            if np.linalg.norm(vecc)>0:
                vec=vecc
            else:
                vec=np.array([0,0])
            new_ptos[n,:]+=vec
            self.Def[n,:]=vec
            self.im_x[0,n]+=vec[1]
            self.im_y[0,n]+=vec[0]
            self.im_xy[0,n]+=np.sqrt(vec[0]**2+vec[1]**2)
            pbar.update(1)
        for k in range(1,self.form[0]):
            Old_set = Im_old[int(dots[k*self.form[1],0]-self.box):int(dots[k*self.form[1],0]+self.box),
                             int(dots[k*self.form[1],1]-self.box):int(dots[k*self.form[1],1]+self.box)]
            New_set = Im_new[int(dots[k*self.form[1],0]-self.box):int(dots[k*self.form[1],0]+self.box),
                             int(dots[k*self.form[1],1]-self.box):int(dots[k*self.form[1],1]+self.box)]
            mask = Old_set[int(self.box/4):int(self.box*3/4),int(self.box/4):int(self.box*3/4)]
            a,b,c,sub_int_def=cv2.minMaxLoc(cv2.matchTemplate(New_set,mask,cv2.TM_CCOEFF_NORMED))
            vecc=np.array([int(sub_int_def[1]-self.box/4),int(sub_int_def[0]-self.box/4)])
            if np.linalg.norm(vecc)>0:
                vec=vecc
            else:
                vec=np.array([0,0])
            new_ptos[k*self.form[1],:]+=vec
            self.Def[k*self.form[1],:]=vec
            self.im_x[k,0]+=vec[1]
            self.im_y[k,0]+=vec[0]
            self.im_xy[k,0]+=np.sqrt(vec[0]**2+vec[1]**2)
            pbar.update(1)
        for k in range(1,self.form[0]):
            for n in range(1,self.form[1]):
                Old_set = Im_old[int(dots[k*self.form[1]+n,0]-self.box):int(dots[k*self.form[1]+n,0]+self.box),
                                int(dots[k*self.form[1]+n,1]-self.box):int(dots[k*self.form[1]+n,1]+self.box)]
                New_set = Im_new[int(dots[k*self.form[1]+n,0]-self.box):int(dots[k*self.form[1]+n,0]+self.box),
                                int(dots[k*self.form[1]+n,1]-self.box):int(dots[k*self.form[1]+n,1]+self.box)]
                mask = Old_set[int(self.box/4):int(self.box*3/4),int(self.box/4):int(self.box*3/4)]
                a,b,c,sub_int_def=cv2.minMaxLoc(cv2.matchTemplate(New_set,mask,cv2.TM_CCOEFF_NORMED))
                vecc=np.array([int(sub_int_def[1]-self.box/4),int(sub_int_def[0]-self.box/4)])
                if np.linalg.norm(vecc)>0:
                    vec=vecc
                else:
                    vec=np.array([0,0])
                new_ptos[k*self.form[1]+n,:]+=vec
                self.Def[k*self.form[1]+n,:]=vec
                P=get_DyDp(self.form,new_ptos,old_ptos,k*self.form[1]+n)
                # UPDATE IMAGES
                self.im_x[k,n]+=vec[1]
                self.im_y[k,n]+=vec[0]
                self.im_xy[k,n]+=np.sqrt(vec[0]**2+vec[1]**2)
                self.im_dudx[k-1,n-1]=(P[2]-1)/self.step
                self.im_dudy[k-1,n-1]=(P[4])/self.step
                self.im_dvdx[k-1,n-1]=(P[3])/self.step
                self.im_dvdy[k-1,n-1]=(P[5]-1)/self.step
                pbar.update(1)
        self.ptos += self.Def

    def get_lienso(self,Im,s,type_def='Y'):
        self.type_def = type_def
        lienso = np.zeros((Im.shape[0],Im.shape[1]))
        dim=(self.roi[3][1]-self.roi[2][1],self.roi[2][0]-self.roi[0][0])
        self.E_xx=1/2*(2*self.im_dudx+self.im_dudx**2+self.im_dudy**2)
        self.E_yy=1/2*(2*self.im_dvdy+self.im_dvdx**2+self.im_dvdy**2)
        self.E_xy=1/2*(self.im_dudy+self.im_dvdx+self.im_dudx*self.im_dudy+self.im_dvdx*self.im_dvdy)
        if type_def=='X':
            rescale=cv2.resize(self.im_x,dim, interpolation =cv2.INTER_CUBIC)
        elif type_def=='Y':
            rescale = cv2.resize(self.im_y,dim, interpolation =cv2.INTER_CUBIC)
        elif type_def=='XY':
            rescale = cv2.resize(self.im_xy,dim, interpolation =cv2.INTER_CUBIC)
        elif type_def=='E_XX':
            rescale = cv2.resize(self.E_xx, dim, interpolation=cv2.INTER_CUBIC)
        elif type_def == 'E_YY':
            rescale = cv2.resize(self.E_yy, dim, interpolation=cv2.INTER_CUBIC)
        elif type_def == 'E_XY':
            rescale = cv2.resize(self.E_xy, dim, interpolation=cv2.INTER_CUBIC)
        lienso[self.roi[0][0]:self.roi[3][0],self.roi[0][1]:self.roi[3][1]]=rescale
        lienso2=cv2.applyColorMap(cv2.cvtColor(cv2.convertScaleAbs(255/2+lienso*s),cv2.COLOR_GRAY2BGR),cv2.COLORMAP_JET)
        if self.GetExtens == 1:
            l = 0
            rescaleX,rescaleY=np.zeros_like(lienso),np.zeros_like(lienso)
            rescaleX[self.roi[0][0]:self.roi[3][0],self.roi[0][1]:self.roi[3][1]] = cv2.resize(self.im_x,dim, interpolation =cv2.INTER_CUBIC)
            rescaleY[self.roi[0][0]:self.roi[3][0],self.roi[0][1]:self.roi[3][1]] = cv2.resize(self.im_y,dim, interpolation =cv2.INTER_CUBIC)
            puntos_mov=[]
            for puntos in self.extens_dots:
                puntos_mov.append(np.array([puntos[0,:],puntos[1,:]]))
                cv2.line(lienso2,(int(puntos[0,1]),int(puntos[0,0])),(int(puntos[1,1]),int(puntos[1,0])),(0,0,255),2)
                cv2.circle(lienso2,(int(puntos[0,1]),int(puntos[0,0])),3,(255,0,0),-1)
                cv2.circle(lienso2,(int(puntos[1,1]),int(puntos[1,0])),3,(255,0,0),-1)
                delta=np.array([np.array([rescaleY[int(puntos[0,0]),int(puntos[0,1])],rescaleX[int(puntos[0,0]),int(puntos[0,1])]]),
                                np.array([rescaleY[int(puntos[1,0]),int(puntos[1,1])],rescaleX[int(puntos[1,0]),int(puntos[1,1])]])])
                puntos_mov[l]+=delta
                self.extens_strain[l]=(np.linalg.norm(puntos_mov[l][0,:]-puntos_mov[l][1,:])-np.linalg.norm(puntos[0,:]-puntos[1,:]))/np.linalg.norm(puntos[0,:]-puntos[1,:])
                self.extens_desp[l]=np.linalg.norm(puntos_mov[l][0,:]-puntos_mov[l][1,:])
                print(f' StranGage {l+1:.0f}: {1E4*self.extens_strain[l]:6.0f} microStrain [ {self.extens_desp[l]:.2f} px ]')
                l+=1
        lienso2[:self.roi[0][0],:,:]=0
        lienso2[self.roi[3][0]:,:,:]=0
        lienso2[:,:self.roi[0][1],:]=0
        lienso2[:,self.roi[3][1]:,:]=0
        x,y=np.meshgrid(range(lienso.shape[1]),range(lienso.shape[0]))
        map_x = griddata(self.ptos, self.ptos_0[:, 0], (y, x), method='cubic')
        map_y = griddata(self.ptos, self.ptos_0[:, 1], (y, x), method='cubic')
        lienso_def=cv2.remap(lienso2,map_y.astype('float32'),map_x.astype('float32'),cv2.INTER_LINEAR)
        return lienso_def
    
    def Extensometro(self,pt1,pt2):
        self.GetExtens = 1
        self.extens_dots.append(np.array([pt1,pt2]).astype('float64'))
        self.extens_desp.append(np.linalg.norm(np.array(pt1)-np.array(pt2)))
        self.extens_strain.append(0)


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def listar_imagenes_tif(carpeta):
    imagenes_tif = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.tif'):
            imagenes_tif.append(archivo)
    return imagenes_tif


class medi:
    def __init__(self,corners,step,box):
        self.ROI=[[corners[0][0],corners[0][1]],[corners[0][0],corners[1][1]],[corners[1][0],corners[0][1]],[corners[1][0],corners[1][1]]]
        self.step=step
        self.box=box
        self.mesh=Mesh(self.ROI,self.step,self.box)
        self.Ext_strain=[]
        self.Ext_desp=[]
        self.Test_Name='Test'
        self.Test_Num=0

    def cam(self,num,s,type_def='E_YY',grid='no',gif='no'):
        cam=cv2.VideoCapture(num)
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        cam.set(cv2.CAP_PROP_EXPOSURE,-1)
        rval,frame0=cam.read()
        frame=np.zeros(frame0.shape)
        frame0_BW=cv2.cvtColor(frame0,cv2.COLOR_BGR2GRAY)
        print(f'Cantidad de puntos de seguimiento: {self.mesh.ptos.shape[0]}')
        imgif=[]
        if self.mesh.GetExtens == 1:
            for k in range(len(self.mesh.extens_strain)):
                self.Ext_strain.append([])
                self.Ext_desp.append([])
        while rval:
            rval,frame=cam.read()
            frame_BW = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.mesh.get_def(frame0_BW,frame_BW)
            im_def_=self.mesh.get_lienso(frame_BW,s,type_def)
            frame2=cv2.addWeighted(frame,0.5,im_def_.astype('uint8'),0.5,0.0)
            if grid=='si':
                for j in range(self.mesh.ptos.shape[0]):
                    cv2.circle(frame2,(self.mesh.ptos[j,1].astype(int),self.mesh.ptos[j,0].astype(int)),2,(0,0,0),-1)
            cv2.imshow(self.Test_Name,rescale_frame(frame2,75))
            imgif.append(rescale_frame(cv2.cvtColor(frame2,cv2.COLOR_BGR2RGB),75))
            frame0_BW=frame_BW
            if self.mesh.GetExtens == 1:
                for k in range(len(self.Ext_strain)):
                    self.Ext_strain[k].append(1E2*self.mesh.extens_strain[k])
                    self.Ext_desp[k].append(self.mesh.extens_desp[k])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        if gif=='si':
            imageio.mimwrite(self.Test_Name+f'_{self.Test_Num}.gif', imgif, 'GIF', duration=1)
        cv2.destroyAllWindows()
        if self.mesh.GetExtens == 1:
            datos=np.zeros((len(self.Ext_strain[0]),len(self.Ext_strain)))
            for k in range(len(self.Ext_strain)):
                plt.plot(np.array(self.Ext_strain[k]),label=f'Strain Gages {k+1:.0f}')
                datos[:,k]=self.Ext_strain[k]
            np.savetxt(self.Test_Name+f'_{self.Test_Num}.txt',datos,delimiter='\t')
            plt.xlabel('Iteracion [n]')
            plt.ylabel('Deformacion relativa [%]')
            plt.legend()
            plt.show()
        self.Test_Num+=1

    def imag(self,path,type_def,s,grid='no',gif='no'):
        imag_tif=listar_imagenes_tif(path)
        imgif=[]
        img0 = cv2.imread(path+imag_tif[0], cv2.IMREAD_UNCHANGED)
        if self.mesh.GetExtens == 1:
            for k in range(len(self.mesh.extens_strain)):
                self.Ext_strain.append([])
                self.Ext_desp.append([])
        for k in range(len(imag_tif)-1):
            img1 = cv2.imread(path+imag_tif[k+1], cv2.IMREAD_UNCHANGED)
            self.mesh.get_def(img0,img1)
            im_def_=self.mesh.get_lienso(img1,s,type_def)
            frame=cv2.addWeighted(cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR),0.5,im_def_.astype('uint8'),0.5,0.0)
            if grid=='si':
                for j in range(self.mesh.ptos.shape[0]):
                    cv2.circle(frame,(self.mesh.ptos[j,1].astype(int),self.mesh.ptos[j,0].astype(int)),2,(150,30,127),-1)
            cv2.imshow(self.Test_Name,rescale_frame(frame,75))
            img0=img1
            if self.mesh.GetExtens == 1:
                for k in range(len(self.Ext_strain)):
                    self.Ext_strain[k].append(1E2*self.mesh.extens_strain[k])
                    self.Ext_desp[k].append(self.mesh.extens_desp[k])
            cv2.waitKey(0)
            imgif.append(rescale_frame(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),75))
        if gif=='si':
            imageio.mimwrite(self.Test_Name+f'_{self.Test_Num}.gif', imgif, 'GIF', duration=1)
        cv2.destroyAllWindows()
        if self.mesh.GetExtens == 1:
            datos=np.zeros((len(self.Ext_strain[0]),len(self.Ext_strain)))
            for k in range(len(self.Ext_strain)):
                plt.plot(np.array(self.Ext_strain[k]),label=f'Strain Gages {k+1:.0f}')
                datos[:,k]=self.Ext_strain[k]
            np.savetxt(self.Test_Name+f'_{self.Test_Num}.txt',datos,delimiter='\t')
            plt.xlabel('Iteracion [n]')
            plt.ylabel('Deformacion relativa [%]')
            plt.legend()
            plt.show()
        self.Test_Num+=1
    
    def Name(self,nombre):
        self.Test_Name=nombre

    def Calib_cam(self,num):
        cam=cv2.VideoCapture(num)
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        cam.set(cv2.CAP_PROP_EXPOSURE,-1)
        rval,_=cam.read()
        while rval:
            rval,frame=cam.read()
            frame_BW = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow(self.Test_Name,rescale_frame(frame_BW,75))
            frame_BW_fft=np.log(np.abs(np.fft.fftshift(np.fft.fft2(frame_BW)))/(frame_BW.shape[0]*frame_BW.shape[1])+1)
            cv2.imshow(self.Test_Name+'_FFT',rescale_frame(frame_BW_fft,75))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

#medicion=medi([[380,250],[1050,850]],40,100)
#medicion.mesh.Extensometro([650,550],[650,650])
#medicion.mesh.Extensometro([550,650],[650,650])
#medicion.imag('C:\\Users\\user\\Documents\\Lineas de Trabajo Interno\\DIC\\Sample13\\','E_XY',20000,'si')

#medicion=medi([[180,550],[920,760]],40,60)
#medicion.mesh.Extensometro([540,650],[580,650])
#medicion.imag('C:\\Users\\user\\Downloads\\al-tensile-2d\\al-tensile-2d\\','E_YY',5000)

medicion=medi([[180,450],[850,1150]],40,100)
medicion.Name('Prueba con Camara')
#medicion.Calib_cam(0)
medicion.mesh.Extensometro([550,650],[550,750])
medicion.cam(0,5000,'E_XX','si')
