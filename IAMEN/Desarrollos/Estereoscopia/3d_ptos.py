import cv2
import numpy as np
import matplotlib.pyplot as plt

def dots(X1,X2,d,f,w):
    x1 = X1[:, 0] - w
    x2 = X2[:, 0] - w
    r_xy=d/(x1-x2)*np.array([(x1+x2)/2,f*np.ones((x1.shape[0],1))])
