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

def distance(a, b):
    dist = np.linalg.norm(encode_point(a)-encode_point(b))
    return dist

df = pd.DataFrame(columns=['source', 'target', 'dist'])

rand_target = randint(2, 25) #was 98
new_row = {'source': 1, 'target': rand_target, 'dist': distance(1, rand_target)}
df = df.append(new_row, ignore_index=True)

for source in range(1, 25):
    total_cons = 0
    print("source: ", source)
    out_iter = 0
    while( total_cons < 20):
        print(out_iter)
        if out_iter > 50:
            break

        try:
            source_cons = df['source'].value_counts().loc[source]
        except:
            source_cons = 0

        try:
            target_cons = df['target'].value_counts().loc[source]
        except:
            target_cons = 0

        total_cons = source_cons + target_cons

        if(total_cons > 19):    
            continue

        valid_target = False
        in_iter = 0
        while not valid_target:
            rand_target = randint(1, 25)
            if rand_target != source:
                
                if ((df['source'] == source) & (df['target'] == rand_target)).any() == False:
                    
                    if ((df['source'] == rand_target) & (df['target'] == source)).any() == False:
                        try:
                            target_source_cons = df['source'].value_counts().loc[rand_target]
                        except:
                            target_source_cons = 0

                        try:
                            target_target_cons = df['target'].value_counts().loc[rand_target]
                        except:
                            target_target_cons = 0

                        target_total_cons = target_source_cons + target_target_cons
                        if target_total_cons < 20:
                            valid_target = True
            
            in_iter = in_iter + 1
            if(in_iter > 200):
                break

        if valid_target:
            new_row = {'source': source, 'target': rand_target, 'dist': distance(source, rand_target)}
            df = df.append(new_row, ignore_index=True)

        out_iter = out_iter+1

print(df)
df.to_csv('.\cube_gen\dists_test_2d.csv')
