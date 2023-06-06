import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

cam=cv2.VideoCapture(2)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cam.set(cv2.CAP_PROP_EXPOSURE,-1)
print(cam)
rval, frame=cam.read()
while rval:
    rval, frame=cam.read()
    cv2.imshow('camara',rescale_frame(frame,50))
    if cv2.waitKey(10) == 's':
        break
