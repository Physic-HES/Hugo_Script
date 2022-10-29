import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np
import scipy.linalg
from scipy.spatial.transform import Rotation as R
import plotly.graph_objects as go

mplstyle.use('fast')

def plani(carp,arch):
    dots=pd.read_csv('C:/Users/laboratorio optica/Documents/Hugo/Alfonso/Planitud/'+carp+'/'+arch+'.asc',delimiter=' ')
    Az,El,Rho=(dots.values[:,4])*np.pi/180,(dots.values[:,5]-180)*np.pi/180,dots.values[:,6]
    XYZ=np.tile(np.c_[Rho],(1,3))*np.c_[np.sin(El)*np.cos(Az),-np.sin(El)*np.sin(Az),np.cos(El)]
    rango_util=np.abs(XYZ[:,2]+1.3)<15E-3
    XYZ=XYZ[rango_util] #exluir valores debajo de la mesa

    fig2 = plt.figure(figsize=(15,10))
    ax2 = fig2.add_subplot(projection='3d')
    ax2.scatter3D(XYZ[:,0],XYZ[:,1],XYZ[:,2],s=.05,c=(dots.values[rango_util,3]),cmap=plt.get_cmap('gray'))
    ax2.set_box_aspect((np.ptp(2*XYZ[:,0]), np.ptp(2*XYZ[:,1]), np.ptp(40*XYZ[:,2])))
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')

    A=np.c_[XYZ[:,0],XYZ[:,1],np.ones(XYZ.shape[0])]
    X,residual,_,_=scipy.linalg.lstsq(A,XYZ[:,2])
    r_x=R.from_euler('x',np.arctan(X[0]))  #ROTACION EN X
    r_y=R.from_euler('y',np.arctan(-X[1]))  #ROTACION EN Y
    dots_CG=XYZ[:,[0,1,2]]-np.tile(np.sum(XYZ[:,[0,1,2]],axis=0)/XYZ.shape[0],(XYZ.shape[0],1))
    DOT=(np.dot(r_y.as_matrix(),np.dot(r_x.as_matrix(),dots_CG.T))).T
    #DOT[:,2]=-DOT[:,2]
    DOT=DOT[np.abs(DOT[:,2]-DOT[:,2].mean())<2*np.std(DOT[:,2]),:] # excluir mayeres a 2 sigmas
    #colores_dot=dots.values[np.abs(DOT[:,2]-DOT[:,2].mean())<6*np.std(DOT[:,2]),5]

    fig3 = plt.figure(figsize=(15,10))
    ax3 = fig3.add_subplot(projection='3d')
    scatter3_plot=ax3.scatter3D(DOT[:,0],DOT[:,1],DOT[:,2],s=.05,c=(DOT[:,2]),cmap=plt.get_cmap('jet'))
    ax3.set_box_aspect((np.ptp(2*DOT[:,0]), np.ptp(2*DOT[:,1]), np.ptp(400*DOT[:,2])))
    ax3.set_xlabel('X')
    ax3.set_ylabel('Y')
    ax3.set_zlabel('Z')
    plt.colorbar(scatter3_plot)
    ax3.set_xlim([np.min(DOT[:,0]),np.max(DOT[:,0])])
    ax3.set_ylim([np.min(DOT[:, 1]), np.max(DOT[:, 1])])
    #ax3.view_init(azim=0,elev=90)
    plt.title(carp+'_'+arch)
    print(f'Tamaño de archivo: {dots.values.shape[0]} puntos')
    print(f'Tamaño de archivo filtrado: {DOT.shape[0]} puntos')
    print(f'Maxima desviacion: {1000*(np.max(DOT[:,2])-np.min(DOT[:,2])):2.2f} mm')

    #scatter_plot=go.Scatter3d(x=DOT[:,0].flatten(),y=DOT[:,1].flatten(),z=DOT[:,2].flatten(),mode='markers',
    #                          marker=dict(size=1,color=DOT[:,2].flatten(),colorscale='jet'))
    #layout=go.Layout(scene=dict(aspectratio=dict(x=5,y=8,z=2)))
    #fig=go.Figure(data=scatter_plot,layout=layout)
    #fig.show()

    #fig4 = plt.figure(figsize=(15,10))
    #ax4 = fig4.add_subplot(projection='3d')
    #scatter2_plot=ax4.scatter3D(dots.values[:,7],dots.values[:,8],dots.values[:,10]-dots.values[:,10].mean(),
    #                            s=0.5,c=(dots.values[:,10]-dots.values[:,10].mean()),cmap=plt.get_cmap('jet'))
    #ax4.set_box_aspect((np.ptp(1*dots.values[:,7]), np.ptp(1*dots.values[:,8]), np.ptp(100*(dots.values[:,10]-dots.values[:,10].mean()))))
    #ax4.set_xlabel(r'Azimut [$\theta$]')
    #ax4.set_ylabel(r'Elevation [$\phi$]')
    #ax4.set_zlabel(r'Distance [$\rho$]')
    #plt.colorbar(scatter2_plot)
    plt.show()


carp=input('Nombre de la carpeta de la medicion: ')
arch=input('Nombre del archivo de medicion: ')
plani(carp,arch)
