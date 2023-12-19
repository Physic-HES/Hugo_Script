import time
import cv2
import numpy as np
import matplotlib.pyplot as plt


def guardar(event):
    if event.key == 'g':
        np.savetxt('dot3d_' + time.strftime('%Y%m%d',time.localtime()) + '.txt',ptos,delimiter='\t')
        exit()

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)


def ordenar(dot_des):
    dot2 = dot_des[np.argsort(dot_des[:, 1]), :]
    k = 0
    val = np.diff(dot2[:, 1]) > 2 * np.mean(np.diff(dot2[:, 1]))
    for i in range(val.shape[0]):
        if val[i]:
            dot2[k:i + 1, :] = dot2[np.argsort(dot2[k:i + 1, 0]) + k, :]
            k = i + 1
    dot2[k:, :] = dot2[np.argsort(dot2[k:, 0]) + k, :]
    return dot2


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


def dots(X1,X2,d,f,w,h):
    x1 = (X1[:, 0] - w/2)*3E-3
    y1 = (X1[:, 1] - h / 2) * 3E-3
    x2 = (X2[:, 0] - w/2)*3E-3
    y2 = (X2[:, 1] - h / 2) * 3E-3
    r_xy=np.multiply(np.c_[d/(x1-x2),d/(x1-x2)],np.c_[(x1+x2)/2,f*np.ones(x1.shape)])
    r_z=-.5*(y1*np.sqrt(((r_xy[:,0]+d/2)**2+r_xy[:,1]**2)/(x1**2+f**2))+
            y2*np.sqrt(((r_xy[:,0]-d/2)**2+r_xy[:,1]**2)/(x2**2+f**2)))
    dat=np.c_[r_xy,r_z]
    return dat


def plot_ptos(ptos):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(ptos[:,0],ptos[:,1],ptos[:,2])
    axisEqual3D(ax)
    plt.show()

def get_ims():
    plt.ion()
    global X1, X2
    cam = cv2.VideoCapture(2)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    w=2560
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    h = 960
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
    cam.set(cv2.CAP_PROP_EXPOSURE, 140)
    rval, frame = cam.read()
    cv2.imshow(f'Modo Automatico de deteccion', frame)
    cv2.destroyAllWindows()
    fig = plt.figure()
    ax = plt.subplot2grid((2,3),(0,1),colspan=2,rowspan=2,projection='3d')
    axL = plt.subplot2grid((2,3),(0,0))
    axR = plt.subplot2grid((2,3),(1,0))
    step=time.time()
    while True:
        global im1, im2, ptos
        rval, frame = cam.read()
        for k in range(2):
            red_image=frame[:,int(k*w/2):int((k+1)*w/2),2]
            (thresh , binaryIM) = cv2.threshold(red_image, int(0.40*np.max(red_image)), 255, cv2.THRESH_BINARY)
            output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
            (numLabels, labels, stats, centroids) = output
            image=frame[:,int(k*w/2):int((k+1)*w/2),:].copy()
            X1=np.array(np.zeros((2,1)))
            for i in range(1,numLabels):
                if stats[i,cv2.CC_STAT_AREA]>=int(0.75*np.mean(stats[1:,cv2.CC_STAT_AREA])):
                    (cX, cY) = centroids[i]
                    cv2.circle(image,(int(cX), int(cY)), 2, (0, 255, 0), -1)
                    cv2.rectangle(image, (int(cX-10), int(cY-10)), (int(cX+10), int(cY+10)), (0, 255, 0), 2)
                    if X1.shape==(2,1):
                        X1=np.array([cX,cY])
                    else:
                        X1=np.c_[X1,np.array([cX,cY])]
            if k == 0:
                im1 = X1.T.copy()
                im1=ordenar(im1)
                axL.imshow(cv2.cvtColor(rescale_frame(image, 20),cv2.COLOR_BGR2RGB))
                axL.axis('off')
                axL.set_title('Left')
            elif k == 1:
                im2 = X1.T.copy()
                im2=ordenar(im2)
                axR.imshow(cv2.cvtColor(rescale_frame(image, 20),cv2.COLOR_BGR2RGB))
                axR.axis('off')
                axR.set_title('Right')
        if im1.shape[0]==im2.shape[0]:
            ptos=dots(im1,im2,60,4.3,int(w/2),h)
            ax.scatter(ptos[:, 0], ptos[:, 1], ptos[:, 2])
            ax.set_xlim([np.min(ptos[:,0])-10,np.max(ptos[:,0])+10])
            ax.set_ylim([150, 250])
            ax.set_zlim([np.min(ptos[:, 2]) - 10, np.max(ptos[:, 2]) + 10])
            ax.set_title('3D Reconstruction')
            ax.set_xlabel('Eje X [mm]')
            ax.set_ylabel('Eje Y [mm]')
            ax.set_zlabel('Eje z [mm]')
            axisEqual3D(ax)
            plt.show()
            plt.pause(0.0000001)
            ax.cla()
            axL.cla()
            axR.cla()
            print(f'Dimention Ok at {1/(time.time()-step):3.3} Hz of Sample Rate')
        elif np.abs(im1.shape[0]-im2.shape[0])>0:
            print('Dimention is Fail')
        fig.canvas.mpl_connect('key_press_event',guardar)
        step=time.time()

get_ims()