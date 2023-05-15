import time
import cv2
import numpy as np
import matplotlib.pyplot as plt


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
            sorted(im1_order[j * row:(j + 1) * row,:], key=lambda m: [m[0], m[1]]))
    return im1_order2


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

def get_ims(row):
    plt.ion()
    hh=0
    global X1, X2
    cam = cv2.VideoCapture(2)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
    w=2560
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    h = 960
    cam.set(cv2.CAP_PROP_EXPOSURE, 150)
    rval, frame = cam.read()
    cv2.imshow(f'Modo Automatico de deteccion', frame)
    cv2.destroyAllWindows()
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    while True:
        global im1, im2
        rval, frame = cam.read()
        for k in range(2):
            (thresh , binaryIM) = cv2.threshold(frame[:,int(k*w/2):int((k+1)*w/2),2], 3, 255, cv2.THRESH_BINARY)
            output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
            (numLabels, labels, stats, centroids) = output
            image=frame[:,int(k*w/2):int((k+1)*w/2),:].copy()
            X1=np.array(np.zeros((2,1)))
            for i in range(1,numLabels):
                if stats[i,cv2.CC_STAT_AREA]>=45:
                    (cX, cY) = centroids[i]
                    cv2.circle(image,(int(cX), int(cY)), 2, (0, 255, 0), -1)
                    cv2.rectangle(image, (int(cX-10), int(cY-10)), (int(cX+10), int(cY+10)), (0, 255, 0), 2)
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
            if hh==0:
                fft=np.abs(np.fft.fft2(binaryIM))
                shift_log=np.log2(np.fft.fftshift(fft)+1)
                cv2.imshow(f'Camara {k}', rescale_frame(image,50))
        if cv2.waitKey(1) & 0xFF == ord('o'):
            hh=1
            cv2.destroyAllWindows()
            time.sleep(0.01)
        if im1.shape[0]==im2.shape[0] and hh==1:
            print('Dimention Ok')
            ptos=dots(im1,im2,60,4.3,int(w/2),h)
            ax.scatter(ptos[:, 0], ptos[:, 1], ptos[:, 2])
            axisEqual3D(ax)
            plt.show()
            plt.pause(0.0001)
            plt.cla()
        elif np.abs(im1.shape[0]-im2.shape[0])>0:
            print('Dimention Fail')
        if cv2.waitKey(1) & 0xFF == ord('s'):
            np.savetxt('dot3d_' + time.strftime('%Y%m%d',time.localtime()) + '.txt',ptos)
            break
    #cv2.destroyAllWindows()
    return ptos


ptos= get_ims(8)