import numpy as np
import pandas as pd


def reconstruct(dist_csv_string, num_points):
    dist_df = pd.read_csv(dist_csv_string)
    num_obs = dist_df.shape[0]
    
    #coef mat: x1, y1, z1, x2, y2, z2, x3, etc.
    coef_mat = np.zeros((num_obs, num_points*3)) #mul by 3 for 3 coords per point
    sq_dist_mat = np.zeros((num_obs, 1))

    for index, row in dist_df.iterrows():
        #print(row['source'], row['target'], row['dist'])
        source_index = int(row['source']) - 1 #offset
        target_index = int(row['target']) - 1 #offser=t
        sq_dist = row['dist']**2

        
        #TODO: Add handling for out of bounds obeservations, may need dynamic size of sq_dist_mat
        #if (source_index > num_points - 1) or (target_index > num_points - 1): 
        #    continue
        
        #fill squared distance matrix
        sq_dist_mat[index, 0] = sq_dist

        #activate source coeff in coeff matrix
        coef_mat[index, (source_index * 3)] = 1 #x coord
        coef_mat[index, (source_index * 3 + 1)] = 1 #y coord
        coef_mat[index, (source_index * 3 + 2)] = 1 #z coord

        #activate target coeff in coeff matrix
        coef_mat[index, target_index * 3] = 1 #x coord
        coef_mat[index, target_index * 3 + 1] = 1 #y coord
        coef_mat[index, target_index * 3 + 2] = 1 #z coord



reconstruct('.\cube_gen\dists.csv', 98)