#TODO: change points per face to be dynamic

import numpy as np
import pandas as pd
from random import randint


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

def distance(a, b, percentage):
    dist = np.linalg.norm(encode_point(a)-encode_point(b))
    print("clean ", dist)
    dist = np.random.normal(dist, dist * percentage * 0.28571428)
    print("noisy ", dist)
    return dist

def gen_dist_df(req_cons, noise_percent):

    df = pd.DataFrame(columns=['source', 'target', 'dist'])

    rand_target = randint(2, 98) #was 98
    new_row = {'source': 1, 'target': rand_target, 'dist': distance(1, rand_target, noise_percent/100)}
    df = df.append(new_row, ignore_index=True)

    for source in range(1, 98):
        total_cons = 0
        print("source: ", source)
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
            print("cons: ", total_cons)
            if(total_cons >= req_cons):
                continue
            
            #find valid target
            valid_target = False
            iteration = 0
            while (not valid_target) and iteration < 100:
                rand_target = randint(1, 98)
                
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
                print("iters reached")
            new_row = {'source': source, 'target': rand_target, 'dist': distance(source, rand_target, noise_percent/100)}
            df = df.append(new_row, ignore_index=True)
    
    return df

df = gen_dist_df(98, 10)
df.to_csv('.\cube_gen\dists_test_10_perc_noise.csv')
