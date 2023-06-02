import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from tqdm import tqdm
import time

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

def ordenar(im,row):
    im1_order = np.array(sorted(im, key=lambda m: [m[1], m[0]]))
    im1_order2 = np.zeros(im1_order.shape)
    for j in range(row):
        im1_order2[j * row:(j + 1) * row, :] = np.array(
            sorted(im1_order[j * row:(j + 1) * row, :], key=lambda m: [m[0], m[1]]))
    return im1_order2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

def get_ims(row):
    global X1
    print('Seleccione automatica de puntos:')
    for k in range(2):
        #cam = cv2.VideoCapture(2)
        #cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        #cam.set(cv2.CAP_PROP_EXPOSURE, -.48)
        while True:
            global im1, im2
            os.system('/home/hp1opticaiamend/Downloads/lumenera_camera_sdk_linux_v2_4_10_for_64bit_x86_systems/lucam-sdk-2.4.10.169/examples/takeAPicture/takeAPicture')
            frame = cv2.imread('/home/hp1opticaiamend/PycharmProjects/Hugo_Script/IAMEN/Desarrollos/Estereoscopia/captured_image.bmp')
            (thresh , binaryIM) = cv2.threshold(frame[:,:,2], 100, 255, cv2.THRESH_BINARY)
            output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
            (numLabels, labels, stats, centroids) = output
            image=frame.copy()
            X1=np.array(np.zeros((2,1)))
            for i in range(1,numLabels):
                if stats[i,cv2.CC_STAT_AREA]>=160:
                    (cX, cY) = centroids[i]
                    cv2.circle(image,(int(cX), int(cY)), 1, (0, 255, 0), -1)
                    cv2.rectangle(image, (int(cX-20), int(cY-20)), (int(cX+20), int(cY+20)), (0, 255, 0), 1)
                    if X1.shape==(2,1):
                        X1=np.array([cX,cY])
                    else:
                        X1=np.c_[X1,np.array([cX,cY])]
            if k == 0:
                im1 = X1.T.copy()
                im1=ordenar(im1,row)
            elif k == 1:
                im2 = X1.T.copy()
                im2=ordenar(im2,row)
            cv2.imshow(f'Modo Automatico de deteccion - Foto {k}', rescale_frame(image,percent=25))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        #cam.release()
    return im1, im2, frame.shape[1], frame.shape[0]


def get_ims_m():
    global X1
    print('Seleccione manual de puntos:')
    for k in range(2):
        clicks=[]
        os.system(
            '/home/hp1opticaiamend/Downloads/lumenera_camera_sdk_linux_v2_4_10_for_64bit_x86_systems/lucam-sdk-2.4.10.169/examples/takeAPicture/takeAPicture')
        frame = cv2.imread(
            '/home/hp1opticaiamend/PycharmProjects/Hugo_Script/IAMEN/Desarrollos/Estereoscopia/captured_image.bmp')
        def draw_circle(event, x, y, flags, param):
            global mouseX, mouseY, X1
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                mouseX, mouseY = x, y
                clicks.append([mouseX, mouseY])
                if len(clicks)==1:
                    X1 = np.array(clicks[0])
                elif len(clicks)>1:
                    X1=np.c_[X1,np.array(clicks[-1])]
        cv2.namedWindow(f'Modo Manual de deteccion - Foto {k}')
        cv2.setMouseCallback(f'Modo Manual de deteccion - Foto {k}', draw_circle)
        while True:
            cv2.imshow(f'Modo Manual de deteccion - Foto {k}', rescale_frame(frame,percent=25))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        if k == 0:
            im1 = X1.T.copy()
        elif k == 1:
            im2 = X1.T.copy()
    return im1, im2, frame.shape[1], frame.shape[0]


def calib(d):
    for k in range(2):
        def draw_circle(event, x, y, flags, param):
            global mouseX, mouseY, X1, clicks
            clicks=[]
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)
                mouseX, mouseY = x, y
                clicks.append([mouseX, mouseY])
                if len(clicks)==1:
                    X1 = np.array(clicks[0])
                elif len(clicks)>1:
                    X1=np.c_[X1,np.array(clicks[-1])]
                print(X1)
        while True:
            global w,h
            cv2.namedWindow(f'Modo Manual de deteccion - Foto {k}')
            cv2.setMouseCallback(f'Modo Manual de deteccion - Foto {k}', draw_circle)
            os.system(
                '/home/hp1opticaiamend/Downloads/lumenera_camera_sdk_linux_v2_4_10_for_64bit_x86_systems/lucam-sdk-2.4.10.169/examples/takeAPicture/takeAPicture')
            frame = cv2.imread(
                '/home/hp1opticaiamend/PycharmProjects/Hugo_Script/IAMEN/Desarrollos/Estereoscopia/captured_image.bmp')
            h=frame.shape[0]
            cv2.imshow(f'Modo Manual de deteccion - Foto {k}', rescale_frame(frame,percent=25))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        if k == 0:
            im1 = X1.T.copy()
            print(im1)
            d_p=np.double(input('cuanto se corrió?: '))
        elif k == 1:
            im2 = X1.T.copy()
            print(im2)
    f=((h/2-im2[1])*(d_p+d)-(h/2-im1[1])*d)/(im2[1]-im1[1])
    return f

def dots(X1,X2,d,f,w,h):
    x1 = (X1[:, 0] - w/2)*3E-3
    y1 = (X1[:, 1] - h / 2) * 3E-3
    x2 = (X2[:, 0] - w/2)*3E-3
    y2 = (X2[:, 1] - h / 2) * 3E-3
    r_xy=np.multiply(np.c_[d/(x1-x2),d/(x1-x2)],np.c_[(x1+x2)/2,f*np.ones(x1.shape)])
    r_z=-.5*(y1*np.sqrt(((r_xy[:,0]+d/2)**2+r_xy[:,1]**2)/(x1**2+f**2))+
            y2*np.sqrt(((r_xy[:,0]-d/2)**2+r_xy[:,1]**2)/(x2**2+f**2)))
    dat=np.c_[r_xy,r_z]
    file=f'Medicion_{dat.shape[0]}ptos2.txt'
    np.savetxt(file,dat,delimiter='\t')
    return dat, file


def plot_ptos(ptos):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(ptos[:,0],ptos[:,1],ptos[:,2])
    #ax.set_zlim3d(np.min([0,np.min(ptos[:,2])])*1.1,np.max([0,np.max(ptos[:,2])])*1.1)
    #ax.set_ylim3d(np.min([0,np.min(ptos[:,1])])*1.1,np.max([0,np.max(ptos[:,1])])*1.1)
    #ax.set_xlim3d(np.min([0,np.min(ptos[:,0])])*1.1,np.max([0,np.max(ptos[:,0])])*1.1)
    axisEqual3D(ax)
    plt.show()

def abrir(path):
    med1 = pd.read_csv(path, delimiter='\t',header=None).values
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_box_aspect(aspect=(1, 1, 1))
    ax.scatter(med1[:, 0], med1[:, 1], med1[:, 2])
    #ax.set_zlim3d(np.min([0, np.min(med1[:, 2])]) * 1.1, np.max([0, np.max(med1[:, 2])]) * 1.1)
    #ax.set_ylim3d(np.min([0, np.min(med1[:, 1])]) * 1.1, np.max([0, np.max(med1[:, 1])]) * 1.1)
    #ax.set_xlim3d(np.min([0, np.min(med1[:, 0])]) * 1.1, np.max([0, np.max(med1[:, 0])]) * 1.1)
    #ax.set_aspect('equal')
    axisEqual3D(ax)
    plt.show()

#f=calib(350)
#print(f)
im1,im2,w,h=get_ims(8)
print([im1.shape,im2.shape])
ptos, file=dots(im1,im2,23,13,w,h)
print('La medicion se guardo como: '+file)
plot_ptos(ptos)
#abrir('/home/hp1opticaiamend/PycharmProjects/Hugo_Script/IAMEN/Desarrollos/Estereoscopia/Medicion_65ptos2.txt')


