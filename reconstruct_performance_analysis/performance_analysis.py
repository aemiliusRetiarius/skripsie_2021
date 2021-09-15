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

import matplotlib.pyplot as plt
import time

###############
##Globals

#intercon_axis = np.arange(5, 98, 2)
intercon_start = 91
intercon_end = 98
intercon_step = 2
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

error_start = 0
error_end = 21
error_step = 10
error_axis = np.arange(error_start, error_end, error_step)

noise_start = 0
noise_end = 51
noise_step = 5
noise_axis = np.arange(noise_start, noise_end, noise_step)
##############
