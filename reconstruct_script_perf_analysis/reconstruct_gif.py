import numpy as np
import pandas as pd

import os
import sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reconstruct_script')
sys.path.insert(0, sibling_path)

from reconstruct_script import reconstruct

import multiprocessing as mp
import itertools

import scipy.io
import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

import time


intercon_start = 1
intercon_end = 98 #98
intercon_step = 1
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_1_edm_rel")

Z = scipy.io.loadmat(target_path)
Z = Z['Z']
Z = Z.T

X = intercon_axis.reshape(Z.shape)

fig1 = plt.figure(figsize=(12.8, 4.8))
ax1 = fig1.add_subplot(1,2,1)
ax2 = fig1.add_subplot(1,2,2, projection="3d")

for i in range(97):
    
    ax1.plot([X[i], X[i]], [0, 2.55], linestyle='dotted', color='black', alpha=0.6)
    ax1.annotate("err ="+str(Z[i]), (65, 2.6), ha='left')

    ax1.plot(X, Z)
    ax1.set_xlabel("Interconnection")
    ax1.set_ylabel("Relative EDM Error")

    dist_df = gen_dist_df(98, int(X[i]), verbosity=1)
    res = reconstruct(dist_df, ret_points=True, verbosity=1)
    res_list = list(map(tuple, res))
    alpha_shape = alsh.alphashape(res_list, 0.01)
    ax2.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
    ax2.set_xlim([-20, 120])
    ax2.set_ylim([-20, 120])
    ax2.set_zlim([-20, 120])

    #plt.show()
    fig1.savefig('./reconstruct_script_perf_analysis/Figures/error_gif/error_gif'+str(i)+'.png')
    ax1.cla()
    ax2.cla()
    print("FRAME:",i)