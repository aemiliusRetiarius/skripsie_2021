import numpy as np
import pandas as pd

import os
import sys

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm

intercon_start = 1
intercon_end = 62
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

fig = plt.figure()
ax = plt.axes()

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_edm_rel_1.mat")

Z = scipy.io.loadmat(target_path)
Z1 = Z['old_error_array']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_edm_rel_2.mat")

Z = scipy.io.loadmat(target_path)
Z2 = Z['old_error_array']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color= 'red', label="Base Error", linewidth=1)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_full_edm_rel_1.mat")

Z = scipy.io.loadmat(target_path)
Z1 = Z['full_less_error_array']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_full_edm_rel_2.mat")

Z = scipy.io.loadmat(target_path)
Z2 = Z['full_less_error_array']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color= 'navy', label="Full Removal", linewidth=1)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_half_edm_rel_1.mat")

Z = scipy.io.loadmat(target_path)
Z1 = Z['half_less_error_array']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_half_edm_rel_2.mat")

Z = scipy.io.loadmat(target_path)
Z2 = Z['half_less_error_array']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color= 'royalblue', label="Half Removal", linewidth=1)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_quar_edm_rel_1.mat")

Z = scipy.io.loadmat(target_path)
Z1 = Z['quarter_less_error_array']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_quar_edm_rel_2.mat")

Z = scipy.io.loadmat(target_path)
Z2 = Z['quarter_less_error_array']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color= 'slategray', label="Quarter Removal", linewidth=1)

plt.legend()
plt.grid()
ax.set_ylim([0, 1.1])
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/heu_line.png', bbox_inches='tight')
plt.show()

