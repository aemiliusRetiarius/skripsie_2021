from matplotlib.pyplot import get
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

import matlab.engine

import multiprocessing as mp

import time

###############
##Globals

interconnections = [30, 40, 50, 60]


##############

def double(index):
    return interconnections[index]*2

def get_err(index):
    dist_df = gen_dist_df(98, interconnections[index])
    err = reconstruct(dist_df, err_ord='rel', parallel_num_str=str(index))
    return err

start_time = time.time()
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#eng0 = matlab.engine.start_matlab()
#eng0.addpath(root, nargout= 0 )
#eng0.addpath(os.path.join(root, "reconstruct_script"), nargout= 0)
#eng0.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Connectors"), nargout= 0 )
#eng0.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Data"), nargout= 0 )

#eng1 = matlab.engine.start_matlab()
#eng1.addpath(root, nargout= 0 )
#eng1.addpath(os.path.join(root, "reconstruct_script"), nargout= 0)
#eng1.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Connectors"), nargout= 0 )
#eng1.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Data"), nargout= 0 )

#eng2 = matlab.engine.start_matlab()
#eng2.addpath(root, nargout= 0 )
#eng2.addpath(os.path.join(root, "reconstruct_script"), nargout= 0)
#eng2.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Connectors"), nargout= 0 )
#eng2.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Data"), nargout= 0 )

#eng3 = matlab.engine.start_matlab()
#eng3.addpath(root, nargout= 0 )
#eng3.addpath(os.path.join(root, "reconstruct_script"), nargout= 0)
#eng3.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Connectors"), nargout= 0 )
#eng3.addpath(os.path.join(os.path.join(root, "reconstruct_script"), "Data"), nargout= 0 )

#eng_list = [eng0, eng1, eng2, eng3]

pool = mp.Pool(processes=4)
inputs = [0, 1, 2, 3]
outputs = pool.map(get_err, inputs)

print(outputs)

print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
print(get_err(0))
print(get_err(1))
print(get_err(2))
print(get_err(3))

print("--- %s seconds ---" % (time.time() - start_time))