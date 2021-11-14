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
initStd_end = 202 #101
initStd_step = 10
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

X, Y = np.meshgrid(intercon_axis,initStd_axis)
####################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_1_202_10_1%n_0%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
print(Z.shape)
print(X.shape)
print(Y.shape)

fig = plt.figure()
ax = plt.axes()
colors = plt.cm.jet(np.linspace(0,0.5,20))
cmap= matplotlib.colors.ListedColormap(colors)
norm= matplotlib.colors.Normalize(vmin=0,vmax=200)

for i in range(20):
    
    zs = Z[i, :]
    if(i % 1 == 0):
        plt.plot(intercon_axis, zs, color=colors[i], linewidth=0.75)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_1")

Z_b1 = scipy.io.loadmat(target_path)
Z_b1 = Z_b1['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_2")

Z_b2 = scipy.io.loadmat(target_path)
Z_b2 = Z_b2['Z']

Z_b = (Z_b1.T + Z_b2.T)/2

plt.plot(intercon_axis, Z_b, color="red", linewidth=1, label="Random Initialisation")

ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
              label='Prior Position Std. Dev. from True Position')
plt.legend()
plt.grid()
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_noi_low_line', bbox_inches='tight')

Z[Z>(1.1)] = 1.1

fig1 = plt.figure()
ax1 = plt.axes(projection="3d")
ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax1.set_xlabel('Interconnection')
ax1.set_ylabel('Prior Position Std. Dev.')
ax1.set_zlabel('Relative EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_noi_low_surf', bbox_inches='tight')

##################################################

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_1_202_10_20%n_0%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
print(Z.shape)
print(X.shape)
print(Y.shape)

fig = plt.figure()
ax = plt.axes()
colors = plt.cm.jet(np.linspace(0,0.5,20))
cmap= matplotlib.colors.ListedColormap(colors)
norm= matplotlib.colors.Normalize(vmin=0,vmax=200)

for i in range(20):
    
    zs = Z[i, :]
    if(i % 1 == 0):
        plt.plot(intercon_axis, zs, color=colors[i], linewidth=0.75)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_20%n_0%e_edm_rel_1")

Z_b1 = scipy.io.loadmat(target_path)
Z_b1 = Z_b1['Z']

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_2")

#Z_b2 = scipy.io.loadmat(target_path)
#Z_b2 = Z_b2['Z']

Z_b = Z_b1.T#(Z_b1.T + Z_b2.T)/2

plt.plot(intercon_axis, Z_b, color="red", linewidth=1, label="Random Initialisation")

ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
              label='Prior Position Std. Dev. from True Position')
plt.legend()
plt.grid()
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_noi_high_line', bbox_inches='tight')

Z[Z>(1.1)] = 1.1

fig1 = plt.figure()
ax1 = plt.axes(projection="3d")
ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax1.set_xlabel('Interconnection')
ax1.set_ylabel('Prior Position Std. Dev.')
ax1.set_zlabel('Relative EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_noi_high_surf', bbox_inches='tight')

##################################################

initStd_start =  1#0
initStd_end = 101 #101
initStd_step = 4
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

X, Y = np.meshgrid(intercon_axis,initStd_axis)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_100_noi_1_101_4_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
print(Z.shape)
print(X.shape)
print(Y.shape)

fig = plt.figure()
ax = plt.axes()
colors = plt.cm.jet(np.linspace(0,0.5,25))
cmap= matplotlib.colors.ListedColormap(colors)
norm= matplotlib.colors.Normalize(vmin=0,vmax=100)

for i in range(20):
    
    zs = Z[i, :]
    if(i % 1 == 0):
        plt.plot(intercon_axis, zs, color=colors[i], linewidth=0.75)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_20%n_0%e_edm_rel_1")

Z_b1 = scipy.io.loadmat(target_path)
Z_b1 = Z_b1['Z']

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_2")

#Z_b2 = scipy.io.loadmat(target_path)
#Z_b2 = Z_b2['Z']

Z_b = Z_b1.T#(Z_b1.T + Z_b2.T)/2

#plt.plot(intercon_axis, Z_b, color="red", linewidth=1, label="Random Initialisation")

ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
              label='Measurement Noise %')
plt.grid()
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_noi_line_std', bbox_inches='tight')

Z[Z>(1.1)] = 1.1

fig1 = plt.figure()
ax1 = plt.axes(projection="3d")
ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax1.set_xlabel('Interconnection')
ax1.set_ylabel('Measurement Noise %')
ax1.set_zlabel('Relative EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_noi_surf_std', bbox_inches='tight')

##################################################

initStd_start =  1#0
initStd_end = 101 #101
initStd_step = 4
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

X, Y = np.meshgrid(intercon_axis,initStd_axis)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_100_err_1_101_4_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
print(Z.shape)
print(X.shape)
print(Y.shape)

fig = plt.figure()
ax = plt.axes()
colors = plt.cm.jet(np.linspace(0,0.5,25))
cmap= matplotlib.colors.ListedColormap(colors)
norm= matplotlib.colors.Normalize(vmin=0,vmax=100)

for i in range(20):
    
    zs = Z[i, :]
    if(i % 1 == 0):
        plt.plot(intercon_axis, zs, color=colors[i], linewidth=0.75)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_20%n_0%e_edm_rel_1")

Z_b1 = scipy.io.loadmat(target_path)
Z_b1 = Z_b1['Z']

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_2")

#Z_b2 = scipy.io.loadmat(target_path)
#Z_b2 = Z_b2['Z']

Z_b = Z_b1.T#(Z_b1.T + Z_b2.T)/2

#plt.plot(intercon_axis, Z_b, color="red", linewidth=1, label="Random Initialisation")

ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
              label='Record Error %')
plt.grid()
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_err_line_std', bbox_inches='tight')

Z[Z>(1.1)] = 1.1

fig1 = plt.figure()
ax1 = plt.axes(projection="3d")
ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax1.set_xlabel('Interconnection')
ax1.set_ylabel('Record Error %')
ax1.set_zlabel('Relative EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/inter_err_surf_std', bbox_inches='tight')