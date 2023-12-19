import matplotlib.pyplot as plt
import numpy as np
import cv2

im_=cv2.imread('/home/hp1opticaiamend/Documents/fotogrametria/tubos_nelson/2.jpg') #Importar imagen
im=cv2.cvtColor(im_,cv2.COLOR_BGR2GRAY) # Convertir a escala de grises
im=cv2.blur(im,(2,2)) #Suavizado Blur con kernel 2x2
X,Y=np.meshgrid(range(im.shape[1]),range(im.shape[0])) #Generacion de Coordenadas X e Y
blanco=np.ones_like(im)*255 #Creando imagen en blanco
im_mask=np.where(np.abs(np.sqrt((X-im.shape[1]/2+10)**2+(Y-im.shape[0]/2)**2)-170)<15,im,0) # Creando mascara tipo anillo de 15 pixeles de ancho y 170 pixeles de radio
ret,thresh1 = cv2.threshold(im_mask,np.max(im_mask)/1.5,255,cv2.THRESH_BINARY) # Binarizacion por encima de 2/3 de la maxima intensidad

## Proceso de filtrado de anillo y sus contornos
kernel = np.ones((2,2),np.uint8)
opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel) #reduccion de ruido blanco
dilation = cv2.dilate(np.roll(opening, (-1, -1), axis=(1, 0)),kernel,iterations = 1) # Engrosado de trazos
closing = cv2.morphologyEx(np.roll(dilation, (-1, -1), axis=(1, 0)), cv2.MORPH_CLOSE, kernel) # conversion a simplemente conexo
edge=cv2.Canny(np.roll(closing, (-1, -1), axis=(1, 0)),100,255) #deteccion de bordes
contours,hierarchy=cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #obtencion de contornos
area=np.zeros(len(contours)) # inicializacion de areas
for j in range(len(contours)):
    area[j] = cv2.contourArea(contours[j]) #obtener el area de cada contorno oncontrado
ind_area=np.argsort(area) # ordenar areas de menor a mayor
cv2.drawContours(im_, contours, -1, (0,0,255), 1) #dibujar contornos sobre la imagen original
im_ceros=np.zeros_like(im_)
cv2.drawContours(im_ceros, contours, -1, (255,0,0), 1) #dibujar contornos sobre una imagen en negro
pts=np.nonzero(im_ceros) # obtener las coordenadas en pixeles del contorno dibujado sobre la imagen negra

## separar esos puntos en coordenadas x e y
Pts_x=np.zeros((len(pts[0]),1))
Pts_y=np.zeros((len(pts[0]),1))
Pts_x[:,0]=pts[1]
Pts_y[:,0]=pts[0]
cv2.imshow('prueba',im_) # mostrar imagen original con el contorno dibujado
plt.imshow(im_)

## Obtencion de parametros por cuadrados minimos para la elipse
## que mejor ajuste los puntos de contorno encontrados
A = np.hstack([Pts_x**2, Pts_x * Pts_y, Pts_y**2, Pts_x, Pts_y])
b = np.ones_like(Pts_x)
x = np.linalg.lstsq(A, b)[0].squeeze()
Z_coord = x[0] * X ** 2 + x[1] * X * Y + x[2] * Y**2 + x[3] * X + x[4] * Y
plt.contour(X, Y, Z_coord, levels=[1], colors=('r'), linewidths=1) # graficar la elipse encontrada
plt.show()

