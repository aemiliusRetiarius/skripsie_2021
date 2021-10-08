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
import itertools

import matplotlib.pyplot as plt

import time

###############
##Globals

interconnections_list = []
interconnections_list.extend(range(5, 98, 2))
result_list = []


##############

def get_err(index, intercon):
    dist_df = gen_dist_df(98, intercon)
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

print(interconnections_list)
for interconnect in interconnections_list:


    inputs = [0, 1, 2, 3]
    outputs = pool.starmap(get_err, zip(inputs, itertools.repeat(interconnect)))
    #outputs2 = pool.starmap(get_err, zip(inputs, itertools.repeat(interconnect)))
    #result_list.append((sum(outputs) + sum(outputs2)) / 8)
    result_list.append(sum(outputs)/4)

print("--- %s seconds ---" % (time.time() - start_time))
print(result_list)
plt.plot(interconnections_list, result_list)
plt.show()


