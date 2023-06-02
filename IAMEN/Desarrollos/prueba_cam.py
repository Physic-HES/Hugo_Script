import cv2

cam=cv2.VideoCapture(2)
print(cam)
rval, frame=cam.read()
cv2.imshow('lumenera',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
