import numpy as np
import pandas as pd


def reconstruct(dist_csv_string, num_points):
    dist_df = pd.read_csv(dist_csv_string)
    num_obs = dist_df.shape[0]
    
    #coef mat: x1, y1, z1, x2, y2, z2, x3, etc.
    coef_mat = np.zeros((num_obs, num_points*3)) #mul by 3 for 3 coords per point
    sq_dist_mat = np.zeros((num_obs, 1))

    for index, row in dist_df.iterrows():
        
        source_index = int(row['source']) - 1 #offset
        target_index = int(row['target']) - 1 #offser=t
        sq_dist = row['dist']**2

        
        #TODO: Add handling for out of bounds obeservations, may need dynamic size of sq_dist_mat
        #if (source_index > num_points - 1) or (target_index > num_points - 1): 
        #    continue
        
        #fill squared distance matrix
        sq_dist_mat[index, 0] = sq_dist

        #in coef mat all rows are linearly idependent, a_t dot a is nonsingular, will not work bec. cloumns dependent
        #in coef mat columns linearly dependent, thus noninvertible

        #activate source coeff in coeff matrix
        coef_mat[index, (source_index * 3)] = 1 #x coord
        coef_mat[index, (source_index * 3 + 1)] = 1 #y coord
        coef_mat[index, (source_index * 3 + 2)] = 1 #z coord

        #activate target coeff in coeff matrix
        coef_mat[index, target_index * 3] = 1 #x coord
        coef_mat[index, target_index * 3 + 1] = 1 #y coord
        coef_mat[index, target_index * 3 + 2] = 1 #z coord

    res = np.dot(np.linalg.pinv(coef_mat), sq_dist_mat)
    
    #gram = np.dot(coef_mat, np.transpose(coef_mat))
    #w = np.dot(np.linalg.pinv(gram), sq_dist_mat)
    #res = np.dot(np.transpose(coef_mat), w)
    
    #res = np.linalg.lstsq(coef_mat, sq_dist_mat, rcond=None)

    res = abs((np.min(res))) + res
    res = np.sqrt(res)
    print(res)


reconstruct('.\cube_gen\dists.csv', 98)