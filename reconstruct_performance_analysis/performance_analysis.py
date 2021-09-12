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

import matplotlib.pyplot as plt

#error_array = np.zeros((1, 10))
noise_array = np.array([1, 5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 49, 54, 59, 63, 68, 72, 77, 81, 86, 90])
error_array = np.zeros((1,21))
noise_array = noise_array[np.newaxis, :]
print(error_array.shape)
print(noise_array.shape)
for i in range(21):
    print("iter:", i)
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = reconstruct(dist_df, verbosity=1, err_ord='rel')
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = (error_array[0,i] + reconstruct(dist_df, verbosity=1, err_ord='rel'))
    dist_df = gen_dist_df(98, noise_array[0,i], verbosity=1)
    error_array[0,i] = error_array[0,i] /8
    print("filled error array")

print(error_array)
plt.plot(noise_array[0,:], error_array[0,:])
plt.show()