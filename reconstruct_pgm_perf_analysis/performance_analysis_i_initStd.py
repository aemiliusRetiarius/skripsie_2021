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

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import get_point_coords, gen_dist_df

###############
##Globals

#intercon_axis = np.arange(5, 98, 2)
intercon_start = 1
intercon_end = 98
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

initStd_start = 0
initStd_end = 101
initStd_step = 4
initStd_axis = np.arange(initStd_start, initStd_end, initStd_step)

target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "z_inter_1_98_init_std_0_101_rel_1.mat")
##############

