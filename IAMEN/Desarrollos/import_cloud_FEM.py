import matplotlib.pyplot as plt
import meshio
import numpy as np
import scipy.interpolate as S


def importFEM(filename,H,W):
    mesh=meshio.read(filename)
    data=mesh.points+mesh.point_data['Displacement']
    data=data[data[:,2]>36.95,:]
    X,Y=np.meshgrid(np.linspace(np.min(data[:,0]),np.max(data[:,0]),H),
                    np.linspace(np.min(data[:,1]),np.max(data[:,1]),W),indexing='ij')
    points=np.zeros((len(data[:,2]),2))
    points[:,0]=data[:,0]
    points[:,1]=data[:,1]
    return S.griddata(points,data[:,2],(X,Y),method='nearest')
