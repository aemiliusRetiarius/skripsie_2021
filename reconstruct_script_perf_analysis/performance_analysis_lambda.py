import numpy as np

import fileinput
import sys, os
import re

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reconstruct_script')
sys.path.insert(0, sibling_path)

from reconstruct_script import reconstruct

import multiprocessing as mp
import itertools

import matplotlib.pyplot as plt

def replaceAll(file,searchExp,replaceExp):
    with open (file, 'r' ) as f:
        content = f.read()
        content_new = re.sub(searchExp, replaceExp, content, flags = re.M)
    with open(file, 'w') as f:
        f.write(content_new)

def get_avg_err(intercon, new_lambda):
    print("inter:", intercon, "lambda:", new_lambda)
    inputs = [0, 1, 2, 3]
    outputs = pool.starmap(get_err, zip(inputs, itertools.repeat(intercon), itertools.repeat(new_lambda)))
    #outputs2 = pool.starmap(get_err, zip(inputs, itertools.repeat(intercon), itertools.repeat(error)))
    #avg_err = (sum(outputs) + sum(outputs2)) / 8
    avg_err = (sum(outputs)) / 4

    return avg_err

def get_err(index, intercon, new_lambda):
    dist_df = gen_dist_df(98, intercon)
    new_string = "lambda = "+str(new_lambda)+";"
    replaceAll((connector_path+str(index)+".m"),"lambda\s=\s.*;",new_string)
    err = reconstruct(dist_df, err_ord='edm_rel', parallel_num_str=str(index))
    return err



connector_path = "./reconstruct_script/Connectors/matlab_connector"

pool = mp.Pool(processes=4)

intercon_start = 1
intercon_end = 62 #62
intercon_step = 4
intercon_axis = np.arange(intercon_start, intercon_end, intercon_step)

fig = plt.figure()
ax = plt.axes()

#new_lambdas = [0.5, 0.8, 1, 5, 10, 100]
new_lambdas = [0.8, 1, 1.25, 1.5, 2, 5, 10, 20]

for new_lambda in new_lambdas:
    
    zs = np.zeros(len(intercon_axis))

    for i in range(len(intercon_axis)):
        
        zs[i] = get_avg_err(intercon_axis[i], new_lambda)
        
    plt.plot(intercon_axis, zs, label="lambda: "+str(new_lambda))

ax.set_ylim([0, 1.1])
ax.set_xlabel('Interconnection')
ax.set_ylabel('Relative EDM Error')

plt.legend()
plt.show()