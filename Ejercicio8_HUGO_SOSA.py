## EJERCICIO 7
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as npl
import imageio as img
from tqdm import tqdm

A = np.array([[1,2,3],[4,5,6]])
U,s,V = npl.svd(A)
S = np.zeros((A.shape[0], A.shape[1]))
S[:len(s), :len(s)] = np.diag(s)
A_ = np.dot(U,np.dot(S,V))
print(np.mean(A_-A))

image = img.imread('arbol.jpg',format='jpg')
