import sys
import time
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def guardar(event):
    if event.key == 'g':
        np.savetxt('desp_miniprob_1.txt', np.c_[np.array(tiem) - tiem[0], np.array(desp)])
        exit()


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


#cam=cv2.VideoCapture(2)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH,2080)
#w=1920
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT,980)
#h=1080
#cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
#cam.set(cv2.CAP_PROP_EXPOSURE, 8200)
#cam.set(cv2.CAP_PROP_FPS,10)
#print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(cam.get(cv2.CAP_PROP_FRAME_WIDTH)))
#print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#print("CAP_PROP_FPS : '{}'".format(cam.get(cv2.CAP_PROP_FPS)))
#print("CAP_PROP_EXPOSURE : '{}'".format(cam.get(cv2.CAP_PROP_EXPOSURE)))
#print("CAP_PROP_POS_MSEC : '{}'".format(cam.get(cv2.CAP_PROP_POS_MSEC)))
#print("CAP_PROP_FRAME_COUNT  : '{}'".format(cam.get(cv2.CAP_PROP_FRAME_COUNT)))
#print("CAP_PROP_BRIGHTNESS : '{}'".format(cam.get(cv2.CAP_PROP_BRIGHTNESS)))
#print("CAP_PROP_CONTRAST : '{}'".format(cam.get(cv2.CAP_PROP_CONTRAST)))
#print("CAP_PROP_SATURATION : '{}'".format(cam.get(cv2.CAP_PROP_SATURATION)))
#print("CAP_PROP_HUE : '{}'".format(cam.get(cv2.CAP_PROP_HUE)))
#print("CAP_PROP_GAIN  : '{}'".format(cam.get(cv2.CAP_PROP_GAIN)))
#print("CAP_PROP_CONVERT_RGB : '{}'".format(cam.get(cv2.CAP_PROP_CONVERT_RGB)))
#rval, frame=cam.read()
os.system(
        '/home/hp1opticaiamend/Downloads/lumenera_camera_sdk_linux_v2_4_10_for_64bit_x86_systems/lucam-sdk-2.4.10.169/examples/takeAPicture/takeAPicture')
frame = cv2.imread(
        '/home/hp1opticaiamend/PycharmProjects/Hugo_Script/IAMEN/Desarrollos/Estereoscopia/ELP_cams/captured_image.bmp')
desp=[]
tiem=[]
pixini=805
w,h=frame.shape[1],frame.shape[0]
cv2.imshow('elp_260',rescale_frame(frame,50))
cv2.destroyAllWindows()
plt.ion()
fig, ax =plt.subplots(1,2)
while True:
    os.system(
        '/home/hp1opticaiamend/Downloads/lumenera_camera_sdk_linux_v2_4_10_for_64bit_x86_systems/lucam-sdk-2.4.10.169/examples/takeAPicture/takeAPicture')
    frame = cv2.imread(
        '/home/hp1opticaiamend/PycharmProjects/Hugo_Script/IAMEN/Desarrollos/Estereoscopia/ELP_cams/captured_image.bmp')
    #rval, frame = cam.read()
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_inv=255-frame2
    (thresh, binaryIM) = cv2.threshold(frame_inv, 200, 255, cv2.THRESH_BINARY)
    output = cv2.connectedComponentsWithStats(binaryIM, 3, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    image = frame.copy()
    X1 = np.array(np.zeros((2, 1)))
    for i in range(1, numLabels):
        if stats[i, cv2.CC_STAT_AREA] >= 510 and stats[i, cv2.CC_STAT_AREA] >= 5010:
            (cX, cY) = centroids[i]
            if np.abs(cX-w/2)<=2*w/3 and np.abs(cY-h/2)<=h/8:
                cv2.circle(image, (int(cX), int(cY)), 3, (0, 255, 0), -1)
                cv2.rectangle(image, (int(cX - 20), int(cY - 20)), (int(cX + 20), int(cY + 20)), (0, 255, 0), 3)
                cv2.rectangle(image, (int(w/6), int(3*h/8)), (int(5/6*w), int(5/8*h)), (0, 0, 255), 2)
                if X1.shape == (2, 1):
                    X1 = np.array([cX, cY])
                else:
                    X1 = np.c_[X1, np.array([cX, cY])]
    X1=X1.T
    #print(f'Distancia [micrones]: {2800/pixini*np.linalg.norm(X1[1]-X1[0])}')
    desp.append(2800/pixini*np.linalg.norm(X1[1]-X1[0]))
    tiem.append(time.time())
    time.sleep(0.01)
    ax[0].imshow(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    ax[1].grid()
    ax[1].plot(np.array(tiem)-tiem[0],np.array(desp))
    ax[1].set_xlabel('Tiempo [$s$]')
    ax[1].set_ylabel(r'Desplazamiento [$\mu m$]')
    plt.show()
    plt.pause(0.0001)
    ax[0].cla()
    ax[1].cla()
    fig.canvas.mpl_connect('key_press_event',guardar)


