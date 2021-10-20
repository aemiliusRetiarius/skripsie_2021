#TODO: add function to observe dimensions from file 

from math import dist
import numpy as np
import pandas as pd

from sklearn.metrics import euclidean_distances

import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

import subprocess
import os, sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import get_point_coords, gen_dist_df

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common_tools')
sys.path.insert(0, sibling_path)

from common_tools import correct_df, get_uniform_point_coords

def get_normalized_error(old_dist, new_dist):
    return abs(new_dist - old_dist) / old_dist

program_path = './build/src/reconstruct_pgm'

priorPos_path = './Data/Ditch/working_init_pos.csv'
dists_path = './Data/Ditch/distance_measurements.csv'
results_path = "./Data/Ditch/result.csv"

#pos_df = get_point_coords(1)
pos_df = get_uniform_point_coords(46, 10)

#Ditch

pos_df.iloc[0,1] = 0
pos_df.iloc[0,2] = 0
pos_df.iloc[0,3] = 0
pos_df.iloc[0,4] = 0
pos_df.iloc[0,5] = 0
pos_df.iloc[0,6] = 0

pos_df.iloc[1,1] = 0
pos_df.iloc[1,3] = 0

pos_df.iloc[2,3] = 0
pos_df.iloc[2,6] = 0

pos_df.iloc[3,3] = 0
pos_df.iloc[3,6] = 0

pos_df.iloc[4,3] = 0
pos_df.iloc[4,6] = 0

pos_df.iloc[5,3] = 0
pos_df.iloc[5,6] = 0

pos_df.iloc[6,3] = 0
pos_df.iloc[6,6] = 0

#/Ditch

# point1
#pos_df.iloc[0,1] = 0
#pos_df.iloc[0,2] = 0
#pos_df.iloc[0,3] = 0
#pos_df.iloc[0,4] = 0
#pos_df.iloc[0,5] = 0
#pos_df.iloc[0,6] = 0
# point5
#pos_df.iloc[4,1] = 100
#pos_df.iloc[4,2] = 0 #
#pos_df.iloc[4,3] = 0 #
#pos_df.iloc[4,4] = 0
#pos_df.iloc[4,5] = 0 #
#pos_df.iloc[4,6] = 0 #
# point21
#pos_df.iloc[20,1] = 0 #
#pos_df.iloc[20,2] = 0 #
#pos_df.iloc[20,3] = 100
#pos_df.iloc[20,4] = 0 #
#pos_df.iloc[20,5] = 0 #
#pos_df.iloc[20,6] = 0
# point30
#pos_df.iloc[29,1] = 0 #
#pos_df.iloc[29,2] = 100
#pos_df.iloc[29,3] = 0 #
#pos_df.iloc[29,4] = 0 #
#pos_df.iloc[29,5] = 0
#pos_df.iloc[29,6] = 0 #


pos_df.to_csv(priorPos_path)

#dist_df = pd.read_csv('./Data/Ditch/distance_measurements_raw.csv', index_col=0)
 
#dist_df = gen_dist_df(98, 20, 1, 0, 1, True)
#dist_df.to_csv(dists_path)

dist_df = pd.read_csv(dists_path, index_col=0)
dist_df = correct_df(dist_df, verbosity=2)
dist_df.to_csv(dists_path)

status = subprocess.run([program_path, "--p", priorPos_path, "--d", dists_path, "--r", results_path, "-l", "0.8", "-t", "20", "-i", "60", "-f","true"])
print("status code: ",status.returncode) # will return -6 if cov underflows

res_df = pd.read_csv(results_path, index_col=0)
res = np.zeros((46,3))

for i in range(46):
    res[i,0] = res_df["x_pos"][i]
    res[i,1] = res_df["y_pos"][i]
    res[i,2] = res_df["z_pos"][i]

#fig1 = plt.figure()
#ax1 = plt.axes(projection="3d")

true_points_full = pd.read_csv('./Data/Ditch/positions_guessed.csv')
#print(true_points_full)

true_points = true_points_full.to_numpy()[:,1:4]

#initPos = pos_df.to_numpy()[:,1:4]
#ax1.scatter3D(initPos[:, 0], initPos[:, 1], initPos[:, 2], c=initPos[:, 2], cmap='hsv')
#plt.show()

fig = plt.figure()
ax = plt.axes(projection="3d")

ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='Blues')
ax.scatter3D(true_points[:, 0], true_points[:, 1], true_points[:, 2], c=true_points[:, 2], cmap='Reds')
plt.show()

#dist_df['new_dist'] = dist_df.apply(lambda row: (np.linalg.norm(res[(int(row['source']) -1), :]- res[(int(row['target'])) -1, :])), axis=1)
#dist_df['normalized_error'] = dist_df.apply(lambda row: get_normalized_error(row['dist'], row['new_dist']), axis=1)
#dist_df.sort_values(by='normalized_error', ascending=False, inplace=True)
#dist_df.reset_index(inplace=True, drop=True)

#print('wrong record perc:', dist_df['changed'].value_counts(normalize=True) * 100)
#test_df = dist_df[dist_df.index < len(dist_df.index)*0.01]
#print('wrong perc in upper 1 perc:', test_df['changed'].value_counts(normalize=True) * 100)

#dist_df = dist_df.iloc[int(len(dist_df.index)*0.02): , :]
#dist_df = dist_df.sort_values(['source', 'target'], ascending=[True, True])

#true_points_full = get_point_coords().to_numpy()

#true_points = true_points_full[:,1:4]

# added init error
#print("init error: ",(np.linalg.norm(true_points-initPos)) / np.linalg.norm(true_points))

#true_edm = euclidean_distances(true_points)
#res_edm = euclidean_distances(res)
#print("edm error: ",(np.linalg.norm(true_edm-res_edm)) / np.linalg.norm(true_edm))

#res_list = list(map(tuple, res))
#alpha_shape = alsh.alphashape(res_list, 0.01)
#ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
#plt.show()

trans = np.zeros((3,3))
trans = np.dot(np.linalg.pinv(res), true_points)
res = res - res[0, :]
res = np.dot(res, trans)
print(trans)

dif = res - true_points
print("rotated error: ",(np.linalg.norm(dif)) / np.linalg.norm(true_points))

#res_list = list(map(tuple, res))
#alpha_shape = alsh.alphashape(res_list, 0.01)
#ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
#plt.show()

#dist_df.drop(['new_dist','normalized_error'], inplace=True, axis=1)
#dist_df.to_csv(dists_path)
