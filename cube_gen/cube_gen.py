#TODO: change points per face to be dynamic
#TODO: fix noise handling
#TODO: encase pandas ops in cython for performance, https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html

import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import alphashape as alsh
from random import uniform, randrange

import os, sys
sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common_tools')
sys.path.insert(0, sibling_path)

from common_tools import check_reverse, distance, enforce_connections

# Front Face: (5x5)
# 21--25
# |   |
# 1 --5
#
# Rear Face: (5x5)
# 46--50
# |   |
# 26--30
#
# Left Face: (5x3)
#
# 63--65
# |   |
# 51--53
#
# Right Face: (5x3)
#
# 78--80
# |   |
# 66--68
#
# Top Face: (3x3)
#
# 87--89
# |   |
# 81--83
#
# Bottom Face: (3x3)
#
# 96--98
# |   |
# 90--92

def encode_point (a):
    
    #############
    if a < 1 or a > 98:
        raise("Invalid value to be encoded: " + str(a))
    #############

    #define x, y and z for face origins. F,B,L,R,T,B
    up = 100 # upper limit
    low = 0 #lower limit
    interval = (up - low) / 4 # 5-1
    origins = np.array([[low,   up,     low,           up,             low + interval, low + interval  ],
                        [low,   up,     up - interval, low + interval, low + interval, up - interval   ],
                        [low,   low,    low,           low,            up,             low             ]])

    if(a >= 90): #bottom face
        origin = origins[:,5][:,np.newaxis]
        a = a - 90
        offset = np.array([ [a % 3], [-(a // 3)], [0] ])*interval
        encoded_point = origin + offset

        return encoded_point

    elif(a >= 81): #top face
        origin = origins[:,4][:,np.newaxis]
        a = a - 81
        offset = np.array([ [a % 3], [a // 3], [0] ])*interval
        encoded_point = origin + offset

        return encoded_point

    elif(a >= 66): #right face
        origin = origins[:,3][:,np.newaxis]
        a = a - 66
        offset = np.array([ [0], [a % 3], [a // 3] ])*interval
        encoded_point = origin + offset

        return encoded_point

    elif(a >= 51): #left face
        origin = origins[:,2][:,np.newaxis]
        a = a - 51
        offset = np.array([ [0], [-(a % 3)], [a // 3] ])*interval
        encoded_point = origin + offset

        return encoded_point

    elif(a >= 26): #back face
        origin = origins[:,1][:,np.newaxis]
        a = a - 26
        offset = np.array([ [-(a % 5)], [0], [a // 5] ])*interval
        encoded_point = origin + offset

        return encoded_point

    else:          #front face
        origin = origins[:,0][:,np.newaxis]
        a = a - 1
        offset = np.array([ [a % 5], [0], [a // 5] ])*interval
        encoded_point = origin + offset

        return encoded_point

def iterate_connections(cons):
    return cons + 1

def gen_dist_df(num_points, req_cons, noise_percent=0, error_percent=0, verbosity=0, enforce_cons=False):

    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print("Generating distance list...")

    con_data = {'point': list(range(1, num_points+1)), 'cons': [0]*num_points}
    con_df = pd.DataFrame(data=con_data)

    dist_df = pd.DataFrame(columns=['source', 'target'])

    for con_index in range(num_points):
        if verbosity > 1: print('Source point:', con_index+1)

        condition_1 = con_df.index != con_index
        condition_2 = con_df['cons'] < req_cons
        condition_3 = con_df['point'].apply(check_reverse, args=((con_index+1), dist_df,))
        
        valid_subset = con_df[condition_1 & condition_2 & (~condition_3)]
        missing_cons = req_cons - con_df.iloc[con_index].cons

        
        missing_cons = int(min(missing_cons, len(valid_subset.index)))
        chosen_targets = valid_subset.sample(n = missing_cons)
        if verbosity > 2: print("Chosen targets:", chosen_targets)
        chosen_targets['cons'] = chosen_targets['cons'].apply(iterate_connections)
        con_df.iloc[con_index].cons = con_df.iloc[con_index].cons+ missing_cons
        con_df.update(chosen_targets)

        append_df = chosen_targets['point'].to_frame()
        
        append_df.rename(columns= {'point':'target'}, inplace=True)
        append_df['source'] = con_index+1
        dist_df = dist_df.append(append_df, ignore_index=True)
        

    if enforce_cons: dist_df = enforce_connections(dist_df, num_points, req_cons, verbosity=verbosity)
    dist_df = dist_df.sort_values(['source', 'target'], ascending=[True, True])
    dist_df = dist_df.astype(int)
    dist_df['dist'] = dist_df.apply(lambda row: distance(encode_point(row.source), encode_point(row.target), noise_percent, verbosity), axis=1)
    dist_df['changed'] = False
    
    error_num = int(len(dist_df.index)*(error_percent/100))
    if verbosity > 0: print("Total number of records: ", int(len(dist_df.index)))
    
    max_dist = dist_df['dist'].max()
    min_dist = dist_df['dist'].min()
    max_index = int(max(dist_df['source'].max(), dist_df['target'].max()))
    min_index = int(min(dist_df['source'].min(), dist_df['target'].min()))
    
    if verbosity > 1: print("Index max:", max_index, "min:", min_index)
    if verbosity > 1: print("Distance max:", max_dist, "min:", min_dist)

    for _ in range(error_num):
        
        condition = dist_df['changed'] == False
        sample = dist_df[condition].sample(n=1)
        if verbosity > 2: print('Index of record changed:', sample.index.item())
        col_to_change = randrange(0,3)

        if col_to_change == 0:
            
            if verbosity > 3: print('Old source:', int(sample['source']))
            new_source = randrange(min_index, max_index + 1)
            sample.source = new_source
            sample.changed = True
            dist_df.update(sample)
            if verbosity > 3: print('New source:', new_source)

        elif col_to_change == 1:
            
            if verbosity > 3: print('Old target:', int(sample['source']))
            new_target = randrange(min_index, max_index + 1)
            sample.target = new_target
            sample.changed = True
            dist_df.update(sample)
            if verbosity > 3: print('New target:', new_target)

        else:
            
            if verbosity > 3: print('Old distance: ', float(sample['dist']))
            new_dist = uniform(min_dist, max_dist)
            sample.dist = new_dist
            sample.changed = True
            dist_df.update(sample)
            if verbosity > 3: print('New distance: ', float(new_dist))

    if verbosity > 0 and error_num > 0: print("Number of records changed: ", error_num)

    if enforce_cons: dist_df = enforce_connections(dist_df, num_points, req_cons, post_error=True, noise_percent=noise_percent ,verbosity=verbosity)
    dist_df = dist_df.sort_values(['source', 'target'], ascending=[True, True])

    dist_df['tol'] = dist_df.apply(lambda row: row.dist*(noise_percent/100)* 0.28571428, axis=1)

    # reorder colums to ensure compatibility with C++ script
    dist_df = dist_df[["source","target","dist","tol","changed"]]
    return dist_df

def get_point_coords(noise_std_dev=0):
    points_df = pd.DataFrame(columns=['point_id','x_pos', 'y_pos','z_pos','x_tol','y_tol','z_tol'])
    for i in range(98):
        
        
        point = encode_point(i+1)
        x_pos = np.random.normal(point[0,0], noise_std_dev)
        y_pos = np.random.normal(point[1,0], noise_std_dev)
        z_pos = np.random.normal(point[2,0], noise_std_dev)
        point_df = pd.DataFrame([[i+1,x_pos,y_pos,z_pos,noise_std_dev,noise_std_dev,noise_std_dev]],columns=['point_id','x_pos', 'y_pos','z_pos','x_tol','y_tol','z_tol'])
        points_df = points_df.append(point_df, ignore_index=True)

    return points_df

def get_true_points_array(num_points=98):
    for i in range(num_points):
        true_point = encode_point(i+1)
        if i == 0:
            true_points = true_point
        else:
            true_points = np.hstack((true_points, true_point))
    true_points = true_points.T
    return true_points
    

if(__name__ == '__main__'):
    #df = gen_dist_df(98, 5, verbosity=3, noise_percent=0, enforce_cons=True)
    #df.to_csv('dists_inter_5_noise_1%.csv')
    #print(distance(1,37,0))
    #print(encode_point(5))
    #print(encode_point(21))
    #print(encode_point(30))
    #get_point_coords(noise_std_dev=50).to_csv('init_pos_std_50.csv')
    #df.to_csv('dists_TEST.csv')
    #print(df)
    res = get_true_points_array()
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    point_nums = np.arange(1, 99)
    #p = ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=point_nums, cmap='viridis')
    
    res_list = list(map(tuple, res))
    alpha_shape = alsh.alphashape(res_list, 0.01)
    ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap='viridis')
    
    ax.set_xlim([-10, 110])
    ax.set_ylim([-10, 110])
    ax.set_zlim([-10, 110])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    #fig.colorbar(p, label='Point Number')
    ax.view_init(elev=20, azim=-80)
    plt.show()
    pass