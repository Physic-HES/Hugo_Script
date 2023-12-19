import matplotlib.pyplot as plt
import numpy as np

Cloud=np.loadtxt('/home/hp1opticaiamend/Documents/Placas Carem/Export/Prueba para placa.asc',delimiter=' ')
#print(np.argwhere(Cloud[:,1]<10).T[0])
rango_util=Cloud[:,0]>0
Cloud2=Cloud[rango_util]
rango_util=Cloud2[:,1]>0
Cloud3=Cloud2[rango_util]
#rango_util=np.abs(Cloud3[:,2]-6.885)<0.005
#Cloud4=Cloud3[rango_util]
Cloud4=Cloud3
fig = plt.figure()
ax2 = fig.add_subplot(projection='3d')
ax2.scatter3D(Cloud4[:,0],Cloud4[:,1],Cloud4[:,2],s=0.5,c=Cloud4[:,3])
ax2.set_box_aspect((np.ptp(2*Cloud4[:,0]), np.ptp(2*Cloud4[:,1]), np.ptp(2*Cloud4[:,2])))
plt.show()
