import numpy as np
import pandas as pd
import math
from random import randrange
from scipy.spatial.transform import Rotation

def distance(a, b, percentage, verbosity=0):
    dist = np.linalg.norm(a-b)
    if verbosity > 3: print("clean ", dist)
    dist = np.random.normal(dist, dist * percentage/100 * 0.28571428)
    if verbosity > 3: print("noisy ", dist)
    return dist

def check_reverse(target, source, dist_df):
    if ((dist_df['target'] == source) & (dist_df['source'] == target)).any():
        return True
    else:
        return False

def enforce_connections(dist_df, num_points, req_cons, post_error=False, noise_percent=0, verbosity=0):

    for i in range(num_points):
        
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
                if not post_error:
                    append_df = pd.DataFrame([[i+1, rand_target]], columns=['source', 'target'])
                    dist_df = dist_df.append(append_df, ignore_index=True)
                else:
                    append_df = pd.DataFrame([[i+1, rand_target, distance(i+1, rand_target, noise_percent, verbosity), False]], columns=['source', 'target', 'dist', 'changed'])
                    dist_df = dist_df.append(append_df, ignore_index=True)

    return dist_df

def correct_df(dist_df, verbosity=0):
    
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print("Correcting distance dataframe...")

    max_num = max(dist_df['source'].max(), dist_df['target'].max())
    if verbosity > 1: print("Max point number pre-correction:",max_num) 
    
    source_unique = dist_df.source.unique()
    target_unique = dist_df.target.unique()
    if verbosity > 2: print("Unique source values:",source_unique)
    if verbosity > 2: print("Unique target values:",target_unique)
    for i in range(max_num):
        point = max_num-i
        point_cons = dist_df[(dist_df['source'] == point) | (dist_df['target'] == point)].count()
        if verbosity > 2: print('Point',point,'Connections:', point_cons[0])
        if (point in source_unique) or (point in target_unique):
            continue
        else:
            if verbosity > 1: print("Point",point,"does not exist")
            dist_df['source'] = dist_df.apply(lambda row: decrement_point_num(row.source, point), axis=1)
            dist_df['target'] = dist_df.apply(lambda row: decrement_point_num(row.target, point), axis=1)

    dist_df['source'] = dist_df['source'].astype(int)
    dist_df['target'] = dist_df['target'].astype(int)

    max_num = max(dist_df['source'].max(), dist_df['target'].max())
    if verbosity > 0: print("Distance dataframe corrected")
    if verbosity > 1: print("Max point number post-correction:",max_num)

    dist_df = dist_df.sort_values(['source', 'target'], ascending=[True, True])
    if verbosity > 0: print("Distance dataframe re-sorted")
    return dist_df

def decrement_point_num(point_num, limit):
    if(point_num > limit):
        return point_num-1
    else:
        return point_num

def get_uniform_point_coords(num_points=98, init_cube_length=100):

    points_df = pd.DataFrame(columns=['point_id','x_pos', 'y_pos','z_pos','x_tol','y_tol','z_tol'])
    
    for i in range(num_points):

        x_pos = np.random.uniform(0, init_cube_length)
        y_pos = np.random.uniform(0, init_cube_length)
        z_pos = np.random.uniform(0, init_cube_length)
        std_dev = math.sqrt(3*(init_cube_length*init_cube_length)) / 3 # check 3.5 -> 3
        point_df = pd.DataFrame([[i+1,x_pos,y_pos,z_pos,std_dev,std_dev,std_dev]],columns=['point_id','x_pos', 'y_pos','z_pos','x_tol','y_tol','z_tol'])
        points_df = points_df.append(point_df, ignore_index=True)

    return points_df

def get_rot_matrix(res_subset, true_subset, verbosity=0):
    
    cross = np.cross(res_subset[1,:],res_subset[3,:])
    normed_cross = cross/np.linalg.norm(cross)
    if verbosity > 1: print("Subset cross product norm:", normed_cross)
    
    normed_z  = res_subset[2,:]/np.linalg.norm(res_subset[2,:])
    if verbosity > 1: print("True cross product norm:", normed_z)
    
    dot_product = np.dot(normed_cross, normed_z)
    if verbosity > 1: print("Subset and true normal dot product:", dot_product)

    householder_flag = False
    householder = None
    if(dot_product < 0):
        if verbosity > 0: print("Changing reconstruction from LH to RH...")
        normed_cross = normed_cross[:,np.newaxis]
        householder = np.identity(3) - 2 * np.dot(normed_cross, normed_cross.T)

        if verbosity > 2: print("Householder matrix:", householder)
        if verbosity > 1: print("Householder determinant:", np.linalg.det(householder))
        res_subset = np.dot(res_subset, householder)
        householder_flag = True
        
    trans_rot = Rotation.align_vectors(true_subset,res_subset)
    #trans_rot = Rotation.align_vectors(true_points,res)
    trans = np.asarray(trans_rot)[0].as_matrix()

    #if dot_product < 0:
    #    trans = np.dot(householder, trans)

    return trans_rot, householder_flag, householder