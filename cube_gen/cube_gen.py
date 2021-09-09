#TODO: change points per face to be dynamic

import numpy as np
import pandas as pd
from random import randint, uniform, randrange


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
    dist = np.random.normal(dist, dist * percentage * 0.28571428)
    if verbosity > 3: print("noisy ", dist)
    return dist

def gen_dist_df(num_points, req_cons, noise_percent=0, error_percent=0, verbosity=0):

    df = pd.DataFrame(columns=['source', 'target', 'dist'])

    rand_target = randint(2, num_points) #was 98
    new_row = {'source': 1, 'target': rand_target, 'dist': distance(1, rand_target, noise_percent/100)}
    df = df.append(new_row, ignore_index=True)

    for source in range(1, num_points):
        total_cons = 0
        if verbosity > 1: print("source: ", source)
        while( total_cons < req_cons):

            #count source connections
            try:
                source_cons = df['source'].value_counts().loc[source]
            except:
                source_cons = 0

            #count target connections
            try:
                target_cons = df['target'].value_counts().loc[source]
            except:
                target_cons = 0

            #if total connections is enough, move to next point
            total_cons = source_cons + target_cons
            if verbosity > 2: print("cons: ", total_cons)
            if(total_cons >= req_cons):
                continue
            
            #find valid target
            valid_target = False
            iteration = 0
            while (not valid_target) and iteration < 100:
                rand_target = randint(1, num_points)
                
                #if targeting itself, continue
                if rand_target == source:
                    continue
                #if connection already exists, continue
                if ((df['source'] == source) & (df['target'] == rand_target)).any() == True:
                    continue        
                #if inverse connection already exists, continue
                if ((df['source'] == rand_target) & (df['target'] == source)).any() == True:
                    continue 

                #count target connections        
                try:
                    target_source_cons = df['source'].value_counts().loc[rand_target]
                except:
                    target_source_cons = 0

                try:
                    target_target_cons = df['target'].value_counts().loc[rand_target]
                except:
                    target_target_cons = 0
                
                #if target connections less than required, set it as a valid target
                target_total_cons = target_source_cons + target_target_cons
                if target_total_cons < req_cons:
                    valid_target = True
                
                #iterate loop
                iteration = iteration + 1
            
            if(iteration == 100):
                if verbosity > 2 : print("iters reached")
            new_row = {'source': source, 'target': rand_target, 'dist': distance(source, rand_target, noise_percent/100, verbosity)}
            df = df.append(new_row, ignore_index=True)
    
    error_num = int(len(df.index)*(error_percent/100))
    if verbosity > 0: print("Total number of records: ", int(len(df.index)))
    
    max_dist = df['dist'].max()
    min_dist = df['dist'].min()
    max_index = int(max(df['source'].max(), df['target'].max()))
    min_index = int(min(df['source'].min(), df['target'].min()))
    
    if verbosity > 1: print("Index max:", max_index, "min:", min_index)
    if verbosity > 1: print("Distance max:", max_dist, "min:", min_dist)

    for _ in range(error_num):
        
        sample = df.sample()
        if verbosity > 2: print('Index of record changed:', sample.index.item())
        col_to_change = randrange(0,3)

        if col_to_change == 0:
            
            if verbosity > 3: print('Old source:', int(sample['source']))
            new_source = randrange(min_index, max_index + 1)
            sample.source = new_source
            df.update(sample)
            if verbosity > 3: print('New source:', new_source)

        elif col_to_change == 1:
            
            if verbosity > 3: print('Old target:', int(sample['source']))
            new_target = randrange(min_index, max_index + 1)
            sample.target = new_target
            df.update(sample)
            if verbosity > 3: print('New target:', new_target)

        else:
            
            if verbosity > 3: print('Old distance: ', float(sample['dist']))
            new_dist = uniform(min_dist, max_dist)
            sample.dist = new_dist
            df.update(sample)
            if verbosity > 3: print('New distance: ', float(new_dist))

    if verbosity > 0 and error_num > 0: print("Number of records changed: ", error_num)

    return df

if(__name__ == '__main__'):
    df = gen_dist_df(98, 10)
    df.to_csv('.\cube_gen\dists_test_10_perc_noise.csv')
