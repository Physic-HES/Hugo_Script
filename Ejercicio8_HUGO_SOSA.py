## EJERCICIO 8
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as npl
import imageio as img
from tqdm import tqdm

A = np.array([[1,2,3],[4,5,6]])
def recons_svd(A):
    U,s,V = npl.svd(A)
    S = np.zeros((A.shape[0], A.shape[1]))
    S[:len(s), :len(s)] = np.diag(s)
    A_ = np.dot(U,np.dot(S,V))
    return(A_)

A_=recons_svd(A)
print(np.mean(A_-A))

image = img.imread('arbol.jpg',format='jpg')
def a_grises(image,r,g):
    R = image[:,:,0] # Matriz de rojos
    G = image[:,:,1] # Matriz de grises
    B = image[:,:,2] # Matriz de azules
    gris = 1/3*(r*R+g*G+(1-(g+r))*B)
    return(gris)

plt.figure(1)
plt.title('Imagen Original')
plt.imshow(image)

r=g=1/3
imagen_gris=a_grises(image,r,g)
plt.figure(2)
plt.title(r'Escala de grises con r=%1.2f, g=%1.2f y b=%1.2f'%(r,g,1-(r+g)))
plt.imshow(imagen_gris,cmap='gray',vmin=0,vmax=255)
plt.savefig('ejemplo1_en_escala_de_grises.jpg')

r=0.3
g=0.59
imagen_gris=a_grises(image,r,g)
plt.figure(3)
plt.title(r'Escala de grises con r=%1.2f, g=%1.2f y b=%1.2f'%(r,g,1-(r+g)))
plt.imshow(imagen_gris,cmap='gray',vmin=0,vmax=255)
plt.savefig('ejemplo2_en_escala_de_grises.jpg')

r=g=1/3
imagen_gris=a_grises(image,r,g)
imagen_gris_SVD=recons_svd(imagen_gris)
plt.figure(4)
plt.title(r'Equivalente SVD en gris (r=%1.2f, g=%1.2f y b=%1.2f)'%(r,g,1-(r+g)))
plt.imshow(imagen_gris,cmap='gray',vmin=0,vmax=255)
plt.savefig('ejemplo3_en_escala_de_grises.jpg')

#no hay diferencia visible entre la reconstruccion SVD y la imagen original en gris con ponderado uniforme

def reduce_svd(A,p):
    U,s,V = npl.svd(A)
    n_elementos = int(p*len(s))
    s[-n_elementos:] = 0
    S = np.zeros((A.shape[0], A.shape[1]))
    S[:len(s), :len(s)] = np.diag(s)
    A_ = np.dot(U,np.dot(S,V))
    return(A_)

r=g=1/3
imagen_gris=a_grises(image,r,g)
redu=0.9
imagen_reducSVD=reduce_svd(imagen_gris,redu)
plt.figure(5)
plt.title(r'Reconstruccion SVD %1.2f%% en gris (r=%1.2f, g=%1.2f y b=%1.2f)'%((1-redu)*100,r,g,1-(r+g)))
plt.imshow(imagen_gris,cmap='gray',vmin=0,vmax=255)
plt.savefig('ejemplo4_en_escala_de_grises.jpg')

p_=np.arange(0.01,1+0.01,0.01)
imagenes = ['arbol.jpg','cuadrado.jpg','fractal.jpg','mona_lisa.jpg','poligono.jpeg']
plt.figure(6)
for j in np.arange(0,5):
    error = []
    if j<4:
        image = img.imread(imagenes[j], format='jpg')
    else:
        image = img.imread(imagenes[j], format='jpeg')
    r = g = 1 / 3
    imagen_gris = a_grises(image, r, g)
    pbar = tqdm(total=len(p_), desc='Calculando error por reduccion SVD de '+imagenes[j])
    for p in p_:
        image_ = reduce_svd(imagen_gris,p)
        error.append(np.mean(np.abs(image_-imagen_gris))/np.mean(imagen_gris))
        pbar.update(1)
    pbar.close()
    plt.plot(p_, np.array(error),label=imagenes[j])
plt.title('Error entre la imagen original y su reduccion por SVD')
plt.xlabel('Reduccion de autovalores [%]')
plt.ylabel('Error relativo')
plt.savefig('Error_reducSVD.jpg')
plt.legend()
plt.show()

