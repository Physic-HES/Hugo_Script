import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


def stereo_match(imgL, imgR):
    # disparity range is tuned for 'aloe' image pair
    window_size = 1
    min_disp = 3
    num_disp = 112 - min_disp #96
    stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                   numDisparities=num_disp,
                                   blockSize=1,
                                   P1=8 * 3 * window_size ** 2,
                                   P2=32 * 3 * window_size ** 2,
                                   disp12MaxDiff=1,
                                   uniquenessRatio=10,
                                   speckleWindowSize=100,
                                   speckleRange=32,
                                   )

    # print('computing disparity...')
    disp = stereo.compute(imgL, imgR).astype(np.float32) / 16.0

    # print('generating 3d point cloud...',)
    h, w = imgL.shape[:2]
    f = 0.8 * w  # guess for focal length
    Q = np.float32([[1, 0, 0, -0.5 * w],
                    [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
                    [0, 0, 0, -f],  # so that y-axis looks up
                    [0, 0, 1, 0]])
    points = cv2.reprojectImageTo3D(disp, Q)
    colors = cv2.cvtColor(imgL, cv2.COLOR_BGR2RGB)
    mask = disp > disp.min()
    out_points = points[mask]
    out_colors = colors[mask]
    #append_ply_array(out_points, out_colors)

    disparity_scaled = (disp - min_disp) / num_disp
    disparity_scaled += abs(np.amin(disparity_scaled))
    disparity_scaled /= np.amax(disparity_scaled)
    disparity_scaled[disparity_scaled < 0] = 0
    return disparity_scaled


cam = cv2.VideoCapture(2)
w,h=2560,960
cam.set(cv2.CAP_PROP_FRAME_WIDTH,w)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,h)
#stereo=cv2.StereoSGBM()
rval,frame=cam.read()
cv2.imshow('foto',frame)
cv2.destroyAllWindows()
time.sleep(0.01)
stereo = cv2.StereoBM_create(numDisparities=96, blockSize=11)
disparity = stereo.compute(frame[:,0:int(w/2),2],frame[:,int(w/2):w,2]).astype(np.float32)
plt.imshow(disparity)
plt.show()
#D=stereo_match(frame[:,0:int(w/2),:],frame[:,int(w/2):w,:])
#cv2.imshow('Depth',rescale_frame(D,50))
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#i=0
#dots=np.zeros((int(w/2*h),3))
#for x in range(int(w/2)):
#    for y in range(h):
#        dots[i,:]=[x,y,disparity[y,x]]
#        i+=1
#fig = plt.figure()
#ax = fig.add_subplot(projection='3d')
#plt.scatter(dots[:,0],dots[:,1],dots[:,2])
#plt.imshow(D)
#plt.show()


