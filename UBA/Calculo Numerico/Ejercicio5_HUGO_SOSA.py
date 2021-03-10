## EJERCICIO 5
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
import imageio


def matriz_evolucion(N,k,h):
    A = np.zeros((N, N))
    np.fill_diagonal(A, 2*(1 - (k/h)**2))
    np.fill_diagonal(A[1:N, :N - 1], (k/h)**2)
    np.fill_diagonal(A[:N - 1, 1:N], (k/h)**2)
    return(A)


def f_x(X,I_):
    x = X
    fun = ['np.sin(x)','np.sin(2*x)','np.piecewise(x,x>=np.pi/3,[1,0])-np.piecewise(x,x>=2*np.pi/3,[1,0])','0*x']
    f = eval(fun[I_-1])
    return(f)  # f es la condicion inicia u(x,t=0)


def g_x(X,I_):
    x = X
    fun = ['0*x', '0*x', '0*x', 'np.piecewise(x,x>=np.pi/100,[1,0])-np.piecewise(x,x>=2*np.pi/100,[1,0])']
    g = eval(fun[I_-1])
    return(g)  # g es la condicion inicial du/dt(x,t=0)


def cumple_contorno(solucion,contornos):
    solucion[0] = contornos[0]
    solucion[-1] = contornos[1]
    return(solucion)  # Retorno solucion con los valores cambiados en los contornos


def gen_condicion_inicial(N,f_x,g_x,k,h,contornos,I_):
    x = np.transpose(np.arange(0,h*(N-1)+h,h))
    u_ = f_x(x,I_)
    u = f_x(x,I_) + k*g_x(x,I_)
    u = cumple_contorno(u,contornos)
    u_ = cumple_contorno(u_, contornos)
    return([np.array(u),np.array(u_)]) # Retorna una lista con las dos condiciones iniciales
    

def paso_integracion(u,u_,contornos,A): # Esta vez, ya vamos a tomar como construida la matriz
    uN = np.dot(A,u) - u_
    uN = cumple_contorno(uN,contornos)
    return(uN) #empleando u y u_, además de la matriz, verifico que se cumpla la condicion de contorno y calculo uN


def integra(condicion_inicial,contornos,k,h,t0,T):
    t = [t0, t0 + k]
    sol = []
    A = matriz_evolucion(len(condicion_inicial[0]),k,h)
    sol.append(condicion_inicial[1])
    sol.append(condicion_inicial[0])
    while t[-1] <= T:
        sol.append(paso_integracion(sol[-1],sol[-2],contornos,A))
        t.append(t[-1]+k)
    solucion = sol
    return([t,solucion]) # Realiza una y otra vez los pasos de integracion


# Ahora evaluamos condiciones iniciales y valores de contorno    
contornos = [0.0,0.0] # 0 en ambos extremos
N = 100 # Cantidad de pasos en la linea
h = np.pi/(N-1) # Paso espacial, notar el N-1. Prueben sacar el -1 a ver que pasa
k = h**2/10 # Paso temporal
T = 8 # Tiempo final
t0 = 0 # tiempo inicial
I_ = np.arange(1,5)


# Primero armemos una función que arme una imagen
def grafica_t(soluciones, indice,k,h,j):
    plt.clf()     # borramos lo que hubiera antes en la figura
    x = np.arange(len(soluciones[1][indice]))*h # Genero una tira de valores x
    u = soluciones[1][indice] # agarro la solución indicada
    t = indice*k # Calculo el tiempo
    # grafico la curva en ese tiempo
    plt.plot (x,u,label='t='+str(np.round(t,4)))
    if j<4:
        plt.ylim(-1.5,1.5) # Para que se vea toda la soguita
    else:
        plt.ylim(-0.1, 0.1)  # Para que se vea toda la soguita
    plt.legend()


# Y ahora armamos una función que nos haga un videito o un gif
def video_evolucion(soluciones, nombre_video,k,h,j):
    lista_fotos =[] # aca voy a ir guardando las fotos
    for i in range ( len(soluciones[0])):
        if i %500==0: # esto es para guardar 1 de cada 500 fotos y sea menos pesado el giff. Si se les corta el guardado de imagen en repl, prueben aumentar este numero
            grafica_t(soluciones, i, k, h,j)
            plt.savefig(nombre_video + '.png')
            lista_fotos.append(imageio.imread(nombre_video + '.png'))
            print (str(i) + ' de '+ str(len(soluciones[0])) + ' fotos guardadas')
    imageio.mimsave(nombre_video + '.gif', lista_fotos) # funcion que crea el video
    print('Gif Guardado')


for j in I_:
    #INTEGRAMOS
    condicion_inicial = gen_condicion_inicial(N,f_x,g_x,k,h,contornos,j)
    soluciones = integra(condicion_inicial,contornos,k,h,t0,T)
    u = soluciones[1] # Acá debería tener todas las soluciones, un array por cada tiempo
    t = soluciones[0] # Acá tenemos los tiempos
    # GRAFICAMOS
    plt.clf()
    plt.plot(np.arange(0, N * h, h), u[0])  # Miremos una solucion
    plt.savefig(r'condicion_inicial_%g.png' % j)
    video_evolucion(soluciones,r'gif_ondas_CI%g'%j,k,h,j)
