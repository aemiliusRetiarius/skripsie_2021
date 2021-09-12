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

import matplotlib.pyplot as plt

def get_normalized_error(old_dist, new_dist):
    return abs(new_dist - old_dist) / old_dist

index_list = []
old_error_list = []
less_error_list = []
error_list = []

for i in range(46, 98, 3):
    index_list.append(i)
    dist_df = gen_dist_df(98, i, error_percent=15, verbosity=1)

    old_error, res_points = reconstruct(dist_df, err_ord='rel', ret_points=True, verbosity=1)

    dist_df['new_dist'] = dist_df.apply(lambda row: (np.linalg.norm(res_points[(int(row['source']) -1), :]- res_points[(int(row['target'])) -1, :])), axis=1)
    dist_df['normalized_error'] = dist_df.apply(lambda row: get_normalized_error(row['dist'], row['new_dist']), axis=1)
    dist_df.sort_values(by='normalized_error', ascending=False, inplace=True)
    #dist_df.reset_index(drop=True, inplace=True)
    #print(dist_df.head)
    dist_df.reset_index(inplace=True, drop=True)
    print("error:", old_error)
    print('wrong record perc:', dist_df['changed'].value_counts(normalize=True) * 100)
    test_df = dist_df[dist_df.index < len(dist_df.index)*0.15]
    print('wrong perc in upper 15 perc:', test_df['changed'].value_counts(normalize=True) * 100)
    #dist_df['normalized_error'].plot()
    #plt.show()
    old_error_list.append(old_error)

    less_dist_df = dist_df.copy()
    less_dist_df = less_dist_df[dist_df.index >= len(dist_df.index)*0.075]
    less_dist_df.drop(columns=['new_dist', 'normalized_error'], inplace=True)
    rel_error, res_points = reconstruct(less_dist_df, err_ord='rel', ret_points=True, verbosity=1)
    less_dist_df['new_dist'] = less_dist_df.apply(lambda row: (np.linalg.norm(res_points[(int(row['source']) -1), :]- res_points[(int(row['target'])) -1, :])), axis=1)
    less_dist_df['normalized_error'] = less_dist_df.apply(lambda row: get_normalized_error(row['dist'], row['new_dist']), axis=1)
    less_dist_df.sort_values(by='normalized_error', ascending=False, inplace=True)
    less_dist_df.reset_index(inplace=True , drop=True)
    print("error:", rel_error)
    print('wrong record perc:', less_dist_df['changed'].value_counts(normalize=True) * 100)
    #dist_df['normalized_error'].plot()
    less_error_list.append(rel_error)

    dist_df = dist_df[dist_df.index >= len(dist_df.index)*0.15]
    dist_df.drop(columns=['new_dist', 'normalized_error'], inplace=True)
    rel_error, res_points = reconstruct(dist_df, err_ord='rel', ret_points=True, verbosity=1)
    dist_df['new_dist'] = dist_df.apply(lambda row: (np.linalg.norm(res_points[(int(row['source']) -1), :]- res_points[(int(row['target'])) -1, :])), axis=1)
    dist_df['normalized_error'] = dist_df.apply(lambda row: get_normalized_error(row['dist'], row['new_dist']), axis=1)
    dist_df.sort_values(by='normalized_error', ascending=False, inplace=True)
    dist_df.reset_index(inplace=True , drop=True)
    print("error:", rel_error)
    print('wrong record perc:', dist_df['changed'].value_counts(normalize=True) * 100)
    #dist_df['normalized_error'].plot()
    error_list.append(rel_error)

    #plt.show()

plt.plot(index_list, old_error_list, color= 'olive')
plt.plot(index_list, less_error_list, color= 'red')
plt.plot(index_list, error_list)
plt.show()