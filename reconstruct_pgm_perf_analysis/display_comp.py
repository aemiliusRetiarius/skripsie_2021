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

fig = plt.figure()
ax = plt.axes()

target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reconstruct_script_perf_analysis/Data", "z_inter_1_62_noi_1_err_0_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
Z = Z.T

plt.plot(intercon_axis, Z, color="orange", label="Det. Algo.")

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z1 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_1%n_0%e_edm_rel_2")

Z = scipy.io.loadmat(target_path)
Z2 = Z['Z']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color="red", label="Prob. Algo. Random Init.")

colors = plt.cm.jet(np.linspace(0,0.5,20))

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_1_202_10_1%n_0%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']

zs = Z[20, :]
plt.plot(intercon_axis, zs, color=colors[0], label="Prob. Algo. Init. Std. Dev. = 200")
zs = Z[10, :]
plt.plot(intercon_axis, zs, color=colors[9], label="Prob. Algo. Init. Std. Dev. = 100")
zs = Z[5, :]
plt.plot(intercon_axis, zs, color=colors[19], label="Prob. Algo. Init. Std. Dev. = 50")

ax.set_ylim([0, 1.1])
plt.grid()
plt.legend()
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/comp_low', bbox_inches='tight')

#######################

fig = plt.figure()
ax = plt.axes()

target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reconstruct_script_perf_analysis/Data", "z_inter_1_62_noi_5_err_1_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
Z = Z.T

plt.plot(intercon_axis, Z, color="orange", label="Det. Algo.")

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_5%n_1%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z1 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_rand_100_5%n_1%e_edm_rel_2")

Z = scipy.io.loadmat(target_path)
Z2 = Z['Z']
Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color="red", label="Prob. Algo. Random Init.")

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_200_5%n_1%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z1 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_200_5%n_1%e_edm_rel_2")

Z = scipy.io.loadmat(target_path)
Z2 = Z['Z']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color=colors[0], label="Prob. Algo. Init. Std. Dev. = 200")

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_100_5%n_1%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z1 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_100_5%n_1%e_edm_rel_2")

Z = scipy.io.loadmat(target_path)
Z2 = Z['Z']

Z = (Z1.T + Z2.T)/2

plt.plot(intercon_axis, Z, color=colors[9], label="Prob. Algo. Init. Std. Dev. = 100")

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_50_5%n_1%e_edm_rel_1")

Z = scipy.io.loadmat(target_path)
Z1 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_50_5%n_1%e_edm_rel_2")

Z = scipy.io.loadmat(target_path)
Z2 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_50_5%n_1%e_edm_rel_3")

Z = scipy.io.loadmat(target_path)
Z3 = Z['Z']

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_50_5%n_1%e_edm_rel_3")

Z = scipy.io.loadmat(target_path)
Z4 = Z['Z']

Z = (Z1.T + Z2.T + Z3.T + Z4.T)/4

plt.plot(intercon_axis, Z, color=colors[19], label="Prob. Algo. Init. Std. Dev. = 50")

ax.set_ylim([0, 1.1])
plt.grid()
plt.legend()
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')
plt.savefig('./reconstruct_pgm_perf_analysis/Figures/comp_high', bbox_inches='tight')
