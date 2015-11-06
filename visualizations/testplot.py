from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = Axes3D(fig)

Z = np.array([[-1.045, 2.0, 3.5, -4.890],
              [-5.678, 3.2, 2.89, 5.78]])

X = np.zeros_like(Z)
X[1,:] = 1
Y = np.zeros_like(Z)
Y[:,1] = 1
Y[:,2] = 2
Y[:,3] = 3

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
        linewidth=0, antialiased=False)
ax.set_zlim3d(-10.0, 10.0)

ax.w_zaxis.set_major_locator(LinearLocator(10))
ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

m = cm.ScalarMappable(cmap=cm.jet)
m.set_array(Z)
fig.colorbar(m)

plt.show()