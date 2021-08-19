#TODO: change points per face to be dynamic

import numpy as np
from numpy.core.defchararray import mod
import pandas as pd


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



