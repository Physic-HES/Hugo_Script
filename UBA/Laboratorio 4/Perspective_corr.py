import cv2
import numpy as np

pts=np.zeros((4,2),np.int)
count=0

def get_mouse(event,x,y,flags,params):
    global count
    if event == cv2.EVENT_LBUTTONDOWN:
        pts[count]=x,y
        count+=1

def cargar_fotos(name):
    im=cv2.imread('C:/Users/laboratorio optica/Documents/Hugo/labo4/'+name+'.jpeg')
    return im

name='Acero_10126mgr'
img=cargar_fotos(name)
scale=3
while True:
    im_w,im_h=len(img[0,:,0]),len(img[:,0,0])
    w,h=300,650
    if count==4:
        pts1=np.float32([scale*pts[0],scale*pts[1],scale*pts[2],scale*pts[3]])
        pts2=np.float32([[0,0],[w,0],[0,h],[w,h]])
        M=cv2.getPerspectiveTransform(pts1,pts2)
        im_out=cv2.warpPerspective(img,M,(w,h))
        cv2.destroyWindow('Original')
        cv2.imshow('Corregido',im_out[:,:,2])
        cv2.imwrite(name+'_C.png',im_out)
        break

    img_=cv2.resize(img, (int(im_w/scale),int(im_h/scale)), interpolation =cv2.INTER_AREA)
    cv2.imshow('Original',img_)
    cv2.setMouseCallback('Original',get_mouse)
    cv2.waitKey(1)

cv2.waitKey(0)
cv2.destroyWindow('Corregido')

