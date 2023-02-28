import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

def get_ims():
    global X1
    print('Seleccione forma de deteccion de puntos:')
    det=int(input('1) Automatica\n2) Manual\n'))
    for k in range(2):
        cam = cv2.VideoCapture(2)
        cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        cam.set(cv2.CAP_PROP_EXPOSURE, -.48)
        if det==1:
            while True:
                global im1, im2
                rval, frame = cam.read()
                (thresh , binaryIM) = cv2.threshold(frame[:,:,2], 45, 255, cv2.THRESH_BINARY)
                output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
                (numLabels, labels, stats, centroids) = output
                image=frame.copy()
                h=0
                for i in range(0,numLabels):
                    if stats[i,cv2.CC_STAT_AREA]>=20:
                        (cX, cY) = centroids[i]
                        cv2.circle(image,(int(cX), int(cY)), 2, (0, 0, 255), -1)
                        if h==0:
                            X1=np.array([cX,cY])
                        else:
                            X1=np.c_[X1,np.array([cX,cY])]
                    h+=1
                if k == 0:
                    im1 = X1.T.copy()
                elif k == 1:
                    im2 = X1.T.copy()
                cv2.imshow(f'Modo Automatico de deteccion - Foto {k}', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
            cam.release()
        elif det==2:
            clicks=[]
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
                cv2.imshow(f'Modo Manual de deteccion - Foto {k}', frame)
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
        cam = cv2.VideoCapture(0)
        rval, frame = cam.read()
        cam.release()
        clicks=[]
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
            cv2.imshow(f'Modo Manual de deteccion - Foto {k}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        if k == 0:
            im1 = X1.T.copy()
            d_p=np.double(input('cuanto se corrió?: '))
        elif k == 1:
            im2 = X1.T.copy()
    f=(im2[0,1]*d_p-im1[0,1]*d)/(im2[0,1]-im1[0,1])
    return f

def dots(X1,X2,d,f,w,h):
    x1 = (X1[:, 0] - w/2)*3E-3
    y1 = (X1[:, 1] - h / 2) * 3E-3
    x2 = (X2[:, 0] - w/2)*3E-3
    y2 = (X2[:, 1] - h / 2) * 3E-3
    r_xy=np.multiply(np.c_[d/(x1-x2),d/(x1-x2)],np.c_[(x1+x2)/2,f*np.ones(x1.shape)])
    r_z=-.5*(y1*np.sqrt(((r_xy[:,0]+d/2)**2+r_xy[:,1]**2)/(x1**2+f**2))+
            y2*np.sqrt(((r_xy[:,0]-d/2)**2+r_xy[:,1]**2)/(x2**2+f**2)))
    return np.c_[r_xy,r_z]


def plot_ptos(ptos):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(ptos[:,0],ptos[:,1],ptos[:,2])
    ax.set_zlim3d(np.min([0,np.min(ptos[:,2])])*1.1,np.max([0,np.max(ptos[:,2])])*1.1)
    ax.set_ylim3d(np.min([0,np.min(ptos[:,1])])*1.1,np.max([0,np.max(ptos[:,1])])*1.1)
    ax.set_xlim3d(np.min([0,np.min(ptos[:,0])])*1.1,np.max([0,np.max(ptos[:,0])])*1.1)
    ax.set_box_aspect([1,1,1])
    plt.show()

#f=calib(260)
#print(f)
im1,im2,w,h=get_ims()
#print(im1)
ptos=dots(im1,im2,25,5,w,h)
plot_ptos(ptos)

