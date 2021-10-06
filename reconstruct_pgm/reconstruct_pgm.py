import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

import subprocess
import os, sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import get_point_coords, gen_dist_df

program_path = './build/src/reconstruct_pgm'
priorPos_path = './Data/initpos10.csv'
dists_path = './Data/dists_inter_5_noise_1%.csv'
results_path = "./Data/result.csv"
subprocess.run([program_path, "--p", priorPos_path, "--d", dists_path, "--r", results_path, "-l", "0.8", "-t", "1"])

res_df = pd.read_csv(results_path, index_col=0)
print(res_df)
print(res_df.keys())
res = np.zeros((98,3))

for i in range(98):
    res[i,0] = res_df["x_pos"][i]
    res[i,1] = res_df["y_pos"][i]
    res[i,2] = res_df["z_pos"][i]

fig = plt.figure()
ax = plt.axes(projection="3d")

#x.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='hsv')
#plt.show()

true_points_full = get_point_coords().to_numpy()

true_points = true_points_full[:,1:4]
dif = res - true_points
print(np.linalg.norm(dif))
print((np.linalg.norm(dif)) / np.linalg.norm(true_points))

res_list = list(map(tuple, res))
alpha_shape = alsh.alphashape(res_list, 0.01)
ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
#plt.show()