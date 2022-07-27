import cv2
import numpy as np
import matplotlib.pyplot as plt

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
rval, frame = cam.read()
b,g,r=cv2.split(frame)
plt.imshow(r, cmap='gray')
print(rval)
plt.show()
