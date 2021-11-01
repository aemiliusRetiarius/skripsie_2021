import numpy as np
import pandas as pd

import os
import sys

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm

intercon_start = 1
intercon_end = 98
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

error_start = 0
error_end = 101
error_step = 4
error_axis = np.arange(error_start, error_end, error_step)

X, Y = np.meshgrid(intercon_axis, error_axis)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_4_noi_0_101_4_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z1 = Z['Z']

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_4_err_0_101_4_rel_2")

#Z = scipy.io.loadmat(target_path)
#Z2 = Z['Z']

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_4_err_0_101_4_rel_3")

#Z = scipy.io.loadmat(target_path)
#Z3 = Z['Z']

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_4_err_0_101_4_rel_4")

#Z = scipy.io.loadmat(target_path)
#Z4 = Z['Z']
Z = Z1
#Z = (Z1 + Z2 + Z3 + Z4)/4

Z[Z>(1.1)] = 1.1
print(Z) 

fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

ax.set_zlim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Record error %')
ax.set_zlabel('Relative error')

plt.show()

#target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_4_noi_0_101_4_rel_1")

#Z = scipy.io.loadmat(target_path)
#Z1 = Z['Z']

#Z = (Z1)/1

#fig = plt.figure()
#ax = plt.axes(projection="3d")
#ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)

#ax.set_xlabel('Interconnection')
#ax.set_ylabel('3.5 sigma noise %')
#ax.set_zlabel('Relative error')

#plt.show()