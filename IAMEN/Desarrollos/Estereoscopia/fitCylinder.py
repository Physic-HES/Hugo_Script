import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt


def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

def cylinderFitting(xyz,p,th):

    """
    This is a fitting for a vertical cylinder fitting
    Reference:
    http://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XXXIX-B5/169/2012/isprsarchives-XXXIX-B5-169-2012.pdf

    xyz is a matrix contain at least 5 rows, and each row stores x y z of a cylindrical surface
    p is initial values of the parameter;
    p[0] = Xc, x coordinate of the cylinder centre
    P[1] = Yc, y coordinate of the cylinder centre
    P[2] = alpha, rotation angle (radian) about the x-axis
    P[3] = beta, rotation angle (radian) about the y-axis
    P[4] = r, radius of the cylinder

    th, threshold for the convergence of the least squares

    """
    x = xyz[:,0]
    y = xyz[:,1]
    z = xyz[:,2]

    fitfunc = lambda p, x, y, z: (- np.cos(p[3])*(p[0] - x) - z*np.cos(p[2])*np.sin(p[3]) - np.sin(p[2])*np.sin(p[3])*(p[1] - y))**2 + (z*np.sin(p[2]) - np.cos(p[2])*(p[1] - y))**2 #fit function
    errfunc = lambda p, x, y, z: fitfunc(p, x, y, z) - p[4]**2 #error function

    est_p , success = leastsq(errfunc, p, args=(x, y, z), maxfev=1000)

    return est_p, [np.abs(est_p[4]),np.std(np.sqrt(np.abs(fitfunc(est_p,x,y,z)))-np.abs(est_p[4]))]

if __name__=="__main__":

    np.set_printoptions(suppress=True)
    xyz = np.loadtxt('dot3d_20231003124153.txt')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2])
    axisEqual3D(ax)
    plt.show()
    #print xyz
    print("Initial Parameters: ")
    p = np.array([20,440,0,0,173.5])
    print(p)
    print(" ")

    print("Performing Cylinder Fitting ... ")
    est_p , std =  cylinderFitting(xyz,p,0.00001)
    print("Fitting Done!")
    print(" ")


    print("Estimated Parameters: ")
    print(est_p)
    print(std)