#TODO: change points per face to be dynamic
#TODO: fix noise handling
#TODO: sort chosen targets
#TODO: ensure min connection num is satisfied
#TODO: encase pandas ops in cython for performance, https://pandas.pydata.org/pandas-docs/stable/user_guide/enhancingperf.html

import numpy as np
import pandas as pd
import math
from random import uniform, randrange


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

def distance(a, b, percentage, verbosity=0):
    dist = np.linalg.norm(encode_point(a)-encode_point(b))
    if verbosity > 3: print("clean ", dist)
    dist = np.random.normal(dist, dist * percentage/100 * 0.28571428)
    if verbosity > 3: print("noisy ", dist)
    return dist

def check_reverse(target, source, dist_df):
    if ((dist_df['target'] == source) & (dist_df['source'] == target)).any():
        return True
    else:
        return False

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
    dist_df['dist'] = dist_df.apply(lambda row: distance(row.source, row.target, noise_percent, verbosity), axis=1)
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
    
    dist_df['tol'] = dist_df.apply(lambda row: row.dist*(noise_percent/100), axis=1)

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

def get_uniform_point_coords(init_cube_length=100):
    points_df = pd.DataFrame(columns=['point_id','x_pos', 'y_pos','z_pos','x_tol','y_tol','z_tol'])
    
    for i in range(98):

        x_pos = np.random.uniform(0, init_cube_length)
        y_pos = np.random.uniform(0, init_cube_length)
        z_pos = np.random.uniform(0, init_cube_length)
        std_dev = math.sqrt(3*(init_cube_length*init_cube_length)) / 3.5 # check 3.5 -> 3
        point_df = pd.DataFrame([[i+1,x_pos,y_pos,z_pos,std_dev,std_dev,std_dev]],columns=['point_id','x_pos', 'y_pos','z_pos','x_tol','y_tol','z_tol'])
        points_df = points_df.append(point_df, ignore_index=True)

    return points_df

def enforce_connections(dist_df, num_points, req_cons, verbosity=0):

    for i in range(98):
        
        condition_1 = dist_df.source == i+1
        condition_2 = dist_df.target == i+1

        point_cons = len(dist_df[condition_1 | condition_2].index)
        if verbosity > 3: print("Point number ", i+1, " cons: ", point_cons)
        for j in range(req_cons-point_cons):    
            if point_cons < req_cons:
                
                if verbosity > 2: print("Point number ", i+1, "cons: ",point_cons+j, " < ", req_cons ," ,adding con") 

                rand_target = randrange(1,num_points)
                while(rand_target == i+1 or check_reverse(rand_target, i+1, dist_df) or check_reverse(i+1, rand_target, dist_df)):
                    rand_target = randrange(1,num_points)
                if verbosity > 2: print("New target: ", rand_target)

                append_df = pd.DataFrame([[i+1, rand_target]], columns=['source', 'target'])
                dist_df = dist_df.append(append_df, ignore_index=True)
           
    return dist_df



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
    pass