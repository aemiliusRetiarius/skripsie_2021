import numpy as np
import pandas as pd

import os

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors

intercon_start = 1
intercon_end = 62
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

initStd_start =  0#0
initStd_end = 101 #101
initStd_step = 4
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

X, Y = np.meshgrid(intercon_axis,initStd_axis)
####################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_noi_1_101_4_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
print(Z.shape)
print(X.shape)
print(Y.shape)

fig = plt.figure()
ax = plt.axes()
colors = plt.cm.jet(np.linspace(0,0.5,26))
cmap= matplotlib.colors.ListedColormap(colors)
norm= matplotlib.colors.Normalize(vmin=0,vmax=100)

for i in range(26):
    
    zs = Z[i, :]
    if(i % 1 == 0):
        plt.plot(intercon_axis, zs, color=colors[i], alpha=(1-0.025*i), linewidth=0.75)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_1")

Z_b1 = scipy.io.loadmat(target_path)
Z_b1 = Z_b1['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_2")

Z_b2 = scipy.io.loadmat(target_path)
Z_b2 = Z_b2['Z']

Z_b = (Z_b1.T + Z_b2.T)/2

#plt.plot(intercon_axis, Z_b, color="red", linewidth=1, label="Random Initialisation")

ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
              label='Measurement Noise %')
#plt.legend()
plt.grid()
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/init_rand_noise_line', bbox_inches='tight')

Z[Z>(1.1)] = 1.1

fig1 = plt.figure()
ax1 = plt.axes(projection="3d")
ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax1.set_xlabel('Interconnection')
ax1.set_ylabel('Measurement Noise %')
ax1.set_zlabel('Realtive EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/init_rand_noise_surf', bbox_inches='tight')
