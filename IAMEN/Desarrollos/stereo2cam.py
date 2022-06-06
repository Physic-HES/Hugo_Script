import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from lucam import Lucam


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

#Figura StereoVision:
#d,h,f_a,f_b=10,2,3.7,1.7
#C = np.array([d,h])
#Rho = np.array([2,15])
#F_a = np.array([0,f_a])
#F_b = np.array([0,f_b])
#fig, ax =plt.subplots()
#rho=plt.plot([0,Rho[0]],[0,Rho[1]],'-b',label=r'$\rho$')
#a = plt.plot([-C[0]/2,Rho[0]],[-C[1]/2,Rho[1]],'--g',label=r'$\vec{a}$')
#b = plt.plot([C[0]/2,Rho[0]],[C[1]/2,Rho[1]],'--g',label=r'$\vec{b}$')
#cam_a = plt.plot([-C[0]/2,-C[0]/2+F_a[0]],[-C[1]/2,-C[1]/2+F_a[1]],'-k',label='foco_a')
#cam_b = plt.plot([C[0]/2,C[0]/2+F_b[0]],[C[1]/2,C[1]/2+F_b[1]],'-k',label='foco_b')
#ax.set_aspect('equal')

#Lumenera Aqd
#plt.figure()
#camera = Lucam()
#image = camera.TakeSnapshot()
#plt.imshow(image)
#plt.show()

#figura 3d
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')
#ax.set_xlim3d(left=-7,right=7)
#ax.set_ylim3d(bottom=-1,top=30)
#ax.set_zlim3d(bottom=-1,top=2)
#set_axes_equal(ax)
#rho = ax.plot([0,Rho[0]],[0,Rho[1]],[0,Rho[2]],'-b',label=r'$\rho$')
#a = ax.plot([-c[0]/2,Rho[0]],[-c[1]/2,Rho[1]],[-c[2]/2,Rho[2]],'--g',label=r'$\vec{a}$')
#b = ax.plot([c[0]/2,Rho[0]],[c[1]/2,Rho[1]],[c[2]/2,Rho[2]],'--g',label=r'$\vec{b}$')

#Generic Simult cams:
import cv2
import threading

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
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
thread1 = camThread("Camera 1", 1)
thread2 = camThread("Camera 2", 2)
thread1.start()
thread2.start()

#plt.show()
