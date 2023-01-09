import cv2
import matplotlib.pyplot as plt

cam=cv2.VideoCapture(0)
print(cam)
rval, frame=cam.read()
plt.imshow(frame)
plt.show()
