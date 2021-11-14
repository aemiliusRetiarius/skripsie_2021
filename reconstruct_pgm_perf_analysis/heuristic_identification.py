import numpy as np
import pandas as pd
import scipy

import os
import sys
import scipy.io

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reconstruct_pgm')
sys.path.insert(0, sibling_path)

from reconstruct_pgm import reconstruct

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common_tools')
sys.path.insert(0, sibling_path)

from common_tools import heuristic_iden_reduction

import matplotlib.pyplot as plt

def get_normalized_error(old_dist, new_dist):
    return abs(new_dist - old_dist) / old_dist

index_list = []
old_error_list = []
full_less_error_list = []
half_less_error_list = []
quarter_less_error_list = []
error = 10
dists_path = './reconstruct_pgm/Data/working_dists'

fig = plt.figure()
ax = plt.axes()

for i in range(1, 62, 4): #1 62 4
    index_list.append(i)
    if i < 9:
        old_error_list.append(1.1)
        full_less_error_list.append(1.1)
        half_less_error_list.append(1.1)
        quarter_less_error_list.append(1.1)
        continue

    print("inter:", i)
    dist_df = gen_dist_df(98, i, noise_percent=20, error_percent=error, verbosity=0)

    old_error, res_points = reconstruct(dist_df, init_std=100, err_ord='edm_rel', ret_points=True, verbosity=1, pgm_max_iter=15)
    old_error_list.append(old_error)
    print("old errror:",old_error)

    full_less_df = heuristic_iden_reduction(dist_df.copy(deep=True), res_points, err_to_rem=error/100)
    full_less_error = reconstruct(full_less_df, init_std=100, err_ord='edm_rel', verbosity=0, pgm_max_iter=15)
    full_less_error_list.append(full_less_error)
    print("full reduced errror:",full_less_error)

    half_less_df = heuristic_iden_reduction(dist_df.copy(deep=True), res_points, err_to_rem=(error/100)*0.5)
    half_less_error = reconstruct(half_less_df, init_std=100, err_ord='edm_rel', verbosity=0, pgm_max_iter=15)
    half_less_error_list.append(half_less_error)
    print("half reduced errror:",half_less_error)

    quarter_less_df = heuristic_iden_reduction(dist_df.copy(deep=True), res_points, err_to_rem=(error/100)*0.25)
    quarter_less_error = reconstruct(quarter_less_df, init_std=100, err_ord='edm_rel', verbosity=0, pgm_max_iter=15)
    quarter_less_error_list.append(quarter_less_error)
    print("quarter reduced errror:",quarter_less_error)
    #plt.show()

old_error_array = np.array(old_error_list)
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_edm_rel_2.mat")
scipy.io.savemat(target_path, dict(old_error_array=old_error_array))
print(old_error_array)

full_less_error_array = np.array(full_less_error_list)
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_full_edm_rel_2.mat")
scipy.io.savemat(target_path, dict(full_less_error_array=full_less_error_array))
print(full_less_error_array)

half_less_error_array = np.array(half_less_error_list)
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_half_edm_rel_2.mat")
scipy.io.savemat(target_path, dict(half_less_error_array=half_less_error_array))
print(half_less_error_array)

quarter_less_error_array = np.array(quarter_less_error_list)
target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_noi_20_err_10_rem_quar_edm_rel_2.mat")
scipy.io.savemat(target_path, dict(quarter_less_error_array=quarter_less_error_array))
print(quarter_less_error_array)

plt.plot(index_list, old_error_list, color= 'red', label="Base Error")
plt.plot(index_list, full_less_error_list, color= 'navy', label="Full Removal")
plt.plot(index_list, half_less_error_list, color= 'royalblue', label="Half Removal")
plt.plot(index_list, quarter_less_error_list, color= 'lightsteelblue', label="Quarter Removal")
ax.set_ylim([0, 1.1])
plt.show()

