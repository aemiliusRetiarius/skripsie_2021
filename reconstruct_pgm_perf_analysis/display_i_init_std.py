import numpy as np
import pandas as pd

import os

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm

intercon_start = 1
intercon_end = 26
intercon_step = 1
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

initStd_start =  1#0
initStd_end = 202 #101
initStd_step = 10
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

X, Y = np.meshgrid(intercon_axis,initStd_axis)
####################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_26_init_std_1_202_1%n_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

fig1 = plt.figure()
ax1 = fig1.add_subplot(2,2,1,projection="3d")
ax1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax1.set_xlabel('Interconnection')
ax1.set_ylabel('Initial position std dev.')
ax1.set_zlabel('Relative error (1% noise)')
################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_26_init_std_1_202_5%n_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

ax2 = fig1.add_subplot(2,2,2,projection="3d")
ax2.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax2.set_xlabel('Interconnection')
ax2.set_ylabel('Initial position std dev.')
ax2.set_zlabel('Relative error (5% noise)')
################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_26_init_std_1_202_10%n_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

ax3 = fig1.add_subplot(2,2,3,projection="3d")
ax3.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax3.set_xlabel('Interconnection')
ax3.set_ylabel('Initial position std dev.')
ax3.set_zlabel('Relative error (10% noise)')
################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_26_init_std_1_202_20%n_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

ax4 = fig1.add_subplot(2,2,4,projection="3d")
ax4.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax4.set_xlabel('Interconnection')
ax4.set_ylabel('Initial position std dev.')
ax4.set_zlabel('Relative error (20% noise)')
################
# error start
####################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_26_init_std_1_202_1%n_1%e_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

fig2 = plt.figure()
ax2_1 = fig2.add_subplot(1,2,1,projection="3d")
ax2_1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax2_1.set_xlabel('Interconnection')
ax2_1.set_ylabel('Initial position std dev.')
ax2_1.set_zlabel('Relative error (1% noise, 1% record err)')
################
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_26_init_std_1_202_1%n_5%e_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

ax2_1 = fig2.add_subplot(1,2,2,projection="3d")
ax2_1.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax2_1.set_xlabel('Interconnection')
ax2_1.set_ylabel('Initial position std dev.')
ax2_1.set_zlabel('Relative error (1% noise, 5% record err)')
################

plt.show()