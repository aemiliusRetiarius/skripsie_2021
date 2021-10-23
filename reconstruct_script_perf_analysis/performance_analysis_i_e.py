import numpy as np
import pandas as pd

import os
import sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df, encode_point

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reconstruct_script')
sys.path.insert(0, sibling_path)

from reconstruct_script import reconstruct

import multiprocessing as mp
import itertools

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm

import time

###############
##Globals

#intercon_axis = np.arange(5, 98, 2)
intercon_start = 1
intercon_end = 98
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

error_start = 0
error_end = 101
error_step = 4
error_axis = np.arange(error_start, error_end, error_step)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_err_0_101_edm_rel_1.mat")
##############

def get_err(index, intercon, error):
    dist_df = gen_dist_df(98, intercon, error_percent=error)
    err = reconstruct(dist_df, err_ord='edm_rel', parallel_num_str=str(index))
    return err

def get_avg_err(intercon, error):
    print("inter:", intercon, "err:", error)
    inputs = [0, 1, 2, 3]
    outputs = pool.starmap(get_err, zip(inputs, itertools.repeat(intercon), itertools.repeat(error)))
    #outputs2 = pool.starmap(get_err, zip(inputs, itertools.repeat(intercon), itertools.repeat(error)))
    #avg_err = (sum(outputs) + sum(outputs2)) / 8
    avg_err = (sum(outputs)) / 4

    return avg_err

def step_params(intercon_1_d, error_1_d):

    zs = np.zeros(len(intercon_1_d))

    for i in range(len(intercon_1_d)):
        
        zs[i] = get_avg_err(intercon_1_d[i], error_1_d[i])
        
    
    return zs

start_time = time.time()

X, Y = np.meshgrid(intercon_axis, error_axis)

pool = mp.Pool(processes=4)

zs = np.array(step_params(np.ravel(X), np.ravel(Y)))
Z = zs.reshape(X.shape)

print("--- %s seconds ---" % (time.time() - start_time))

scipy.io.savemat(target_path, dict(Z=Z))
#Z = scipy.io.loadmat(target_path)
#Z = Z['Z']



fig = plt.figure()
ax = plt.axes(projection="3d")
ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)



ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Record error %')
ax.set_zlabel('Relative error')

plt.show()