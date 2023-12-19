import cv2
import matplotlib.pyplot as plt
import numpy as np

# Parametros de la Camara
W,H=1248,960 # Ancho y Alto de la Imagen
Grano=5 # Tamaño de grano Imax/8


X,Y=np.meshgrid(range(W),range(H)) # Matrices X e Y de Pixeles
Fas=2*np.pi*np.random.random(X.shape) # Fasores Aleatorios
c=333/Grano # Apertura de filtro Pupila en pixeles
P=np.exp(-1/(2*c**2)*((X-W/2)**2+(Y-H/2)**2)) # Filtro Pupila
#P=np.where(np.sqrt((X-W/2)**2+(Y-H/2)**2)<c,1,0)
Speak=np.abs(np.fft.ifft2(P*np.fft.fft2(Fas)))**2
#for j in range(2):
#    Fas = 2 * np.pi * np.random.random(X.shape)
#    Speak+=np.abs(np.fft.ifft2(P*np.fft.fft2(Fas)))*255 # Generacion de Speckle By Goodman

ret,thresh1 = cv2.threshold(Speak,np.max(Speak)/8,255,cv2.THRESH_BINARY)
edge=cv2.Canny(thresh1.astype('uint8'),1,255)
contours,hierarchy=cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
area=np.zeros(len(contours))
for j in range(len(contours)):
    area[j] = cv2.contourArea(contours[j])
print([Grano, np.mean(2*np.sqrt(area/np.pi)), np.std(2*np.sqrt(area/np.pi))])
cv2.imshow('Speckle',thresh1)
#cv2.waitKey()
cv2.destroyAllWindows()
plt.imshow(Speak,cmap='gray')
plt.show()


