## EJERCICIO 6
## HUGO SOSA
## LU 205/07.

import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as npl
from tqdm import tqdm


def jacobi(A,b,x0,max_iter,tol):
    D = np.diag(np.diag(A))
    L = np.tril(A,-1)
    U = np.triu(A,1)
    M = D
    N = U + L
    B = -np.dot(npl.inv(M),N)
    C = npl.inv(M)
    xN = x0
    resto = npl.norm(xN-np.dot(npl.inv(A),b))
    iter = 0
    while resto>tol and iter<=max_iter:
        xN = np.dot(B,xN)+np.dot(C,b)
        iter = iter + 1
        resto = npl.norm(xN-np.dot(npl.inv(A),b))
        if iter == max_iter:
            print('Max_iter reached')
    return ([xN, iter, resto])


def gauss_seidel(A,b,x0,max_iter,tol):
    D = np.diag(np.diag(A))
    L = np.tril(A,-1)
    U = np.triu(A,1)
    M = D + U
    N = L
    B = -np.dot(npl.inv(M),N)
    C = npl.inv(M)
    xN = x0
    resto = npl.norm(xN-np.dot(npl.inv(A),b))
    iter = 0
    while resto>tol and iter<=max_iter:
        xN = np.dot(B,xN)+np.dot(C,b)
        iter = iter + 1
        resto = npl.norm(xN-np.dot(npl.inv(A),b))
        if iter == max_iter:
            print('Max_iter reached')
    return ([xN, iter, resto])


A1 = np.array([[1,0],[0,2]])
A2 = np.array([[1,1],[0,2]])
b = np.transpose(np.array([[1,1]]))
x1=np.dot(npl.inv(A1),b)
x2=np.dot(npl.inv(A2),b)

J_sol1 = jacobi(A1,b,np.random.rand(2,1),1E2,1E-6)
J_sol2 = jacobi(A2,b,np.random.rand(2,1),1E2,1E-6)
print(' ')
print('Método Jacobi:')
print(r'Sol exacta para A1: [%g,%g]'%(x1[0],x1[1]))
print(r'Sol del método: [%g,%g], iter: %g, err: %e'%(J_sol1[0][0],J_sol1[0][1],J_sol1[1],J_sol1[2]))
print(r'Sol exacta para A2: [%g,%g]'%(x2[0],x2[1]))
print(r'Sol del método: [%g,%g], iter: %g, err: %e'%(J_sol2[0][0],J_sol2[0][1],J_sol2[1],J_sol2[2]))

GS_sol1 = gauss_seidel(A1,b,np.random.rand(2,1),1E2,1E-6)
GS_sol2 = gauss_seidel(A2,b,np.random.rand(2,1),1E2,1E-6)
print(' ')
print('Método Gauss-Seidel:')
print(r'Sol exacta para A1: [%g,%g]'%(x1[0],x1[1]))
print(r'Sol del método: [%g,%g], iter: %g, err: %e'%(GS_sol1[0][0],GS_sol1[0][1],GS_sol1[1],GS_sol1[2]))
print(r'Sol exacta para A2: [%g,%g]'%(x2[0],x2[1]))
print(r'Sol del método: [%g,%g], iter: %g, err: %e'%(GS_sol2[0][0],GS_sol2[0][1],GS_sol2[1],GS_sol2[2]))
print(' ')

def matriz_y_vector(n):
    A = np.random.rand(n, n)
    while npl.det(A)==0:
        A = np.random.rand(n, n)
    b = np.random.rand(n, 1)
    return ([A,b])


trials_J = []
trials_GS = []
Ntrials = 10**4
trials = 0
x0 = np.transpose(np.array([[0,0,0]]))
max_iter = 10**6
tol = 10**-5
pbar = tqdm(total=Ntrials, desc='Random matrix test for the Jacobi and Gauss-Seidel methods')
while trials < Ntrials:
    Ab = matriz_y_vector(3)
    A = Ab[0]
    b = Ab[1]
    rGS = gauss_seidel(A,b,x0,max_iter,tol)
    rJ = jacobi(A,b,x0,max_iter,tol)
    trials_J.append(rJ[1])
    trials_GS.append(rGS[1])
    trials = trials + 1
    pbar.update(1)
pbar.close()
plt.scatter(trials_J,trials_GS)
plt.ylabel('Gauss-Seidel')
plt.xlabel('Jacobi')
plt.yscale('log')
plt.xscale('log')
plt.show()

method=['Jacobi','Gauss-Seidel']
a,b=np.array(trials_J),np.array(trials_GS)
des=[np.sum(a-b<0),np.sum(a-b>0)]
print(' ')
print('El método más efectivo es: ')
print(eval(r'method[%i]'%np.argmax(des))+r', con menor coste iterativo en un %3.2f %% de los casos'%(np.float(np.max(des))/Ntrials*100))

