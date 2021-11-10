import numpy as np
import pandas as pd

import subprocess
import os, sys
import multiprocessing as mp
import itertools

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

import time

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import get_point_coords, gen_dist_df, get_true_points_array

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common_tools')
sys.path.insert(0, sibling_path)

from common_tools import get_rot_matrix

from sklearn.metrics import euclidean_distances

###############
##Globals

#intercon_axis = np.arange(5, 98, 2)
intercon_start = 1
intercon_end = 62
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

initStd_start =  1#1
initStd_end = 202 #101
initStd_step = 10
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_62_4_init_std_1_202_10_0%n_0%e_edm_rel_1.mat")

program_path = './reconstruct_pgm/build/src/reconstruct_pgm'

priorPos_path = './reconstruct_pgm/Data/working_init_pos'
dists_path = './reconstruct_pgm/Data/working_dists'
results_path = "./reconstruct_pgm/Data/result"
##############

def observe_positions(pos_df):
    pos_df.iloc[0,1] = 0
    pos_df.iloc[0,2] = 0
    pos_df.iloc[0,3] = 0
    pos_df.iloc[0,4] = 0
    pos_df.iloc[0,5] = 0
    pos_df.iloc[0,6] = 0
    # point5
    pos_df.iloc[4,1] = 100
    pos_df.iloc[4,2] = 0 #
    pos_df.iloc[4,3] = 0 #
    pos_df.iloc[4,4] = 0
    pos_df.iloc[4,5] = 0 #
    pos_df.iloc[4,6] = 0 #
    # point21
    pos_df.iloc[20,1] = 0 #
    pos_df.iloc[20,2] = 0 #
    pos_df.iloc[20,3] = 100
    pos_df.iloc[20,4] = 0 #
    pos_df.iloc[20,5] = 0 #
    pos_df.iloc[20,6] = 0
    # point30
    pos_df.iloc[29,1] = 0 #
    pos_df.iloc[29,2] = 100
    pos_df.iloc[29,3] = 0 #
    pos_df.iloc[29,4] = 0 #
    pos_df.iloc[29,5] = 0
    pos_df.iloc[29,6] = 0 #

    return pos_df

def get_err(index):
    print("index:",index)
    return_code = -1
    lambda_fac = 0.8
    iter = 25
    tol = 296

    while return_code != 0:
        
        status = subprocess.run([program_path+str(index), "--p", priorPos_path+str(index)+'.csv', "--d", dists_path+str(index)+'.csv', "--r", results_path+str(index)+'.csv', 
        "-l", str(lambda_fac), "-t", str(tol), "-i", str(iter), "-f","true"])
        return_code = status.returncode
        iter = iter - 5

    res_df = pd.read_csv(results_path+str(index)+'.csv', index_col=0)
    res = np.zeros((98,3))

    for i in range(98):
        res[i,0] = res_df["x_pos"][i]
        res[i,1] = res_df["y_pos"][i]
        res[i,2] = res_df["z_pos"][i]

    #true_points_full = get_point_coords().to_numpy()
    #true_points = true_points_full[:,1:4]
    true_points = get_true_points_array(98)
    #trans = np.zeros((3,3))
    #trans = np.dot(np.linalg.pinv(res), true_points)
    #res = res - res[0, :]
    #res = np.dot(res, trans)

    res = res - res[0,:]

    true_points_subset = np.vstack((true_points[0,:],true_points[4,:],true_points[20,:],true_points[29,:]))
    res_subset = np.vstack((res[0,:],res[4,:],res[20,:],res[29,:]))

    trans, householder_flag, householder = get_rot_matrix(res_subset, true_points_subset)
    if householder_flag : res = np.dot(res, householder)
    
    res = trans[0].apply(res)

    true_edm = euclidean_distances(true_points)
    res_edm = euclidean_distances(res)

    dif = res_edm - true_edm
    err = (np.linalg.norm(dif)) / np.linalg.norm(true_edm)

    return err

def create_csv_files(index, intercon, std_dev):
    print("making file:",index)
    pos_df = pd.DataFrame()
    pos_df = get_point_coords(std_dev)
    pos_df = observe_positions(pos_df)
    pos_df.to_csv(priorPos_path+str(index)+'.csv')

    dist_df = gen_dist_df(98, intercon, enforce_cons=True, noise_percent=1, error_percent=0)
    dist_df.to_csv(dists_path+str(index)+'.csv')
    return


def get_avg_err(intercon, std_dev):
    print("inter:", intercon, "std_dev:", std_dev)
    inputs = [0, 1, 2, 3]

    for index in inputs: #have to make individually, pool is making identical csv files
        create_csv_files(index, intercon, std_dev)

    #pool.starmap(create_csv_files, zip(inputs, itertools.repeat(intercon), itertools.repeat(std_dev)))
    outputs = pool.starmap(get_err, zip(inputs))
    #outputs2 = pool.starmap(get_err, zip(inputs, itertools.repeat(intercon), itertools.repeat(error)))
    #avg_err = (sum(outputs) + sum(outputs2)) / 8
    print(outputs)
    avg_err = (sum(outputs)) / 4
    print("avg_error:", avg_err)
    return avg_err

def step_params(intercon_1_d, error_1_d):

    zs = np.zeros(len(intercon_1_d))

    for i in range(len(intercon_1_d)):
        
        zs[i] = get_avg_err(intercon_1_d[i], error_1_d[i])
        
    
    return zs


start_time = time.time()

X, Y = np.meshgrid(intercon_axis,initStd_axis)

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
ax.set_ylabel('Initial position std dev.')
ax.set_zlabel('Relative error')

plt.show()