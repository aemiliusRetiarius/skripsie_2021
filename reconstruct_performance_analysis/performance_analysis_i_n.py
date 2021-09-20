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
intercon_start = 93
intercon_end = 98
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

error_start = 80
error_end = 161
error_step = 4
error_axis = np.arange(error_start, error_end, error_step)

noise_start = 0
noise_end = 101
noise_step = 4
noise_axis = np.arange(noise_start, noise_end, noise_step)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z.mat")
##############

def get_err(index, intercon, error):
    dist_df = gen_dist_df(98, intercon, noise_percent=error)
    err = reconstruct(dist_df, err_ord='rel', parallel_num_str=str(index))
    return err

def get_avg_err(intercon, error):
    print("inter:", intercon, "noise:", error)
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




ax.set_xlabel('Interconnection')
ax.set_ylabel('3.5 sigma noise %')
ax.set_zlabel('Relative error')

plt.show()