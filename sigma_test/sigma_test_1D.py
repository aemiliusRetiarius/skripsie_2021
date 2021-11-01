import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D

mean = np.array([0,-4])
cov = np.array([[5, 5], [5, 6]])

distr = multivariate_normal(cov = cov, mean = mean)
# Generating a meshgrid complacent with
# the 3-sigma boundary
mean_1, mean_2 = mean[0], mean[1]
sigma_1, sigma_2 = cov[0,0], cov[1,1]
     
x = np.linspace(-10, 10, num=100)
y = np.linspace(-10, 10, num=100)
X, Y = np.meshgrid(x,y)
     
# Generating the density function
# for each point in the meshgrid
Z = np.zeros(X.shape)
plane = np.zeros(X.shape)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i,j] = distr.pdf([X[i,j], Y[i,j]])

for i in range(81):
    # Create plane
    y_p = 10-i*0.25
    x_p = np.linspace(-10,10,500)
    z_p = np.linspace(0,0.07,500)
    X_p, Z_p = np.meshgrid(x_p, z_p)

    # Finding closest idx values of Y mesh to y_p
    tol = 1e-4
    idy_y_p = (np.where(y < y_p+tol) and np.where(y > y_p-tol))[0][0]
    # Select the corresponding values of X, Y, Z (carefully switch X and Y)
    x_c, y_c, z_c = X[idy_y_p], Y[idy_y_p], Z[idy_y_p]

    # Create plane, useless
    x_p2 = 3.5
    y_p2 = np.linspace(-10,10,500)
    z_p2 = np.linspace(0,0.07,500)
    Y_p2, Z_p2 = np.meshgrid(y_p2, z_p2)

    # Plot
    fig = plt.figure(figsize=plt.figaspect(1))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='coolwarm',linewidth=0,zorder=10, alpha=1)
    ax.plot_surface(X_p, y_p, Z_p, cmap='viridis',linewidth=0, alpha=0.4,zorder=5)
    #ax.plot_surface(x_p2, Y_p2, Z_p2, color='b',linewidth=0, alpha=0.5,zorder=5)
    ax.plot(x_c,y_c,z_c,zorder=10)

    ax.view_init(elev=20, azim=-70)

    #plt.tight_layout()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig('./sigma_test/Figures/hyper_gif/hyper_gif'+str(i)+'.png', bbox_inches='tight')
    print(i)
    #plt.show()
    #10 by 10