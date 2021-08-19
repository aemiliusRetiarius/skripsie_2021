#TODO: change points per face to be dynamic

import numpy as np
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
        raise("Invalid value to be encoded: " + a)
    #############

    #define x, y and z for face origins. F,B,L,R,T,B
    up = 100 # upper limit
    low = 0 #lower limit
    interval = (up - low) / 5
    origins = np.array([[low, up, low, up, low, low],
                        [low, up, up, low, low, up],
                        [low, low, low, low, up, low]])

    if(a >= 90): #bottom face
        origin = origins[:,5]
        return

    elif(a >= 81): #top face
        origin = origins[:,4]
        return

    elif(a >= 66): #right face
        origin = origins[:,3]
        return

    elif(a >= 51): #left face
        origin = origins[:,2]
        return

    elif(a >= 81): #back face
        origin = origins[:,1]
        return

    else:          #front face
        origin = origins[:,0]
        return
def distance(a, b):
    
    return