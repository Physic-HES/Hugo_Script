import numpy as np
from scipy import linalg as LA
from fractions import Fraction


def GS(A):
    dim=np.shape(A)
    Q=np.zeros(dim)
    R=np.identity(3)
    for j in np.arange(dim[1]):
        Q[:,j]=A[:,j]
    for j in np.arange(0,dim[1]-1):
        for i in np.arange(j+1,dim[1]):
            R[j, i] = np.dot(A[:, i], Q[:, j])/(LA.norm(Q[:, j]))**2
            Q[:, i] = Q[:, i] - R[j, i] * Q[:, j]
    return [Q,R]


def Hh(A):
    dim=np.shape(A)
    Ap=np.zeros(dim)
    H=np.identity(dim[1])
    for j in np.arange(dim[1]):
        Ap[:,j]=A[:,j]
    for j in np.arange(dim[1]-1):
        v = np.zeros(dim[0],)
        Ap=np.dot(H,Ap)
        Q=LA.inv(H)
        v[j]=Ap[j,j]+np.sign(Ap[j,j])*LA.norm(Ap[:,j])
        v[j+1:]=Ap[j+1:,j]
        v=v[np.newaxis]
        H=np.identity(dim[1])-2/np.dot(v,v)*np.dot(v.T,v)
        Q=np.dot(Q,LA.inv(H))
        R=Ap
    return [Q,R]


A=np.array([[1,1,0],[1,0,1],[0,1,1]])
sol=GS(A)
print('Q(GS):')
print(sol[0])
print('R(GS):')
print(sol[1])

sol2=Hh(A)
print('Q(Hh):')
print(sol2[0])
print('R(Hh):')
print(sol2[1])
print(np.dot(sol2[0],sol2[1]))