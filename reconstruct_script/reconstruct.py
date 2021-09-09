import numpy as np
import pandas as pd

import scipy.io
import io
import os
import warnings

import sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df, encode_point

import matlab.engine

from sklearn.manifold import MDS

import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

def reconstruct_file(dist_csv_string, projection=None, rotate=True, return_err_ord=None, verbosity=0):
    dist_df = pd.read_csv(dist_csv_string)
    num_points = int(max(dist_df['source'].max(), dist_df['target'].max()))
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print("Reconstructing with", num_points, "points")
    return reconstruct(dist_df, projection, rotate, return_err_ord, verbosity)

def reconstruct(dist_df, projection=None, rotate=True, err_ord=None, verbosity=0):
    
    num_points = int(max(dist_df['source'].max(), dist_df['target'].max()))
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print('Reconstructing from', num_points, 'points')
    dist_mat = np.zeros((num_points, num_points)) #dist matrix between points for MDS
    mask_mat = np.zeros((num_points, num_points))

    for index, row in dist_df.iterrows():
        
        source_index = int(row['source']) - 1 #offset
        target_index = int(row['target']) - 1 #offser=t
        dist = row['dist']
        
        #TODO: Add handling for out of bounds obeservations, may need dynamic size of sq_dist_mat
        #if (source_index > num_points - 1) or (target_index > num_points - 1): 
        #    continue
        
        #fill dist_mat for MDS, matrix must be symmetric
        dist_mat[source_index, target_index] = dist
        dist_mat[target_index, source_index] = dist
        
        #fill mask matrix
        mask_mat[source_index, target_index] = 1
        mask_mat[target_index, source_index] = 1

    if verbosity > 0: print(">>>>>>>>>>>")
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "edm_raw.mat")
    scipy.io.savemat(target_path, dict(dist_mat=dist_mat, mask_mat=mask_mat))
    if verbosity > 0: print(target_path)
    if verbosity > 0: print('Incomplete EDM Matrices saved')
    
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print('Connecting to Matlab...')
    eng = matlab.engine.start_matlab()
    eng.addpath(os.path.dirname(os.path.abspath(__file__)), nargout= 0 )
    eng.addpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data"), nargout= 0 )
    if verbosity > 0: print('Script Starting')
    if verbosity < 2:
        out = io.StringIO()
        err = io.StringIO()
        eng.matlab_connector(nargout=0,background=False,stdout=out,stderr=err)
    else:
        eng.matlab_connector(nargout=0)
    if verbosity > 0: print('Script Complete')

    if verbosity > 0: print(">>>>>>>>>>>")
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "recon_edm.mat")
    if verbosity > 0: print(target_path)

    edm = scipy.io.loadmat(target_path)

    if verbosity > 0: print('Loaded matrix shape: ' + str(edm['ans'].shape))
    if verbosity > 0: verbosity = verbosity - 1
    embedding = MDS(n_components=3, verbose=verbosity, dissimilarity='precomputed', max_iter=3000, eps=1e-12)
    res = embedding.fit_transform(edm['ans'])
    if verbosity > 0: print("Points Reconstructed")
    if verbosity > 0: print(">>>>>>>>>>>")

    if rotate == True or err_ord != None:
        #true array shape (98, 3)
        for i in range(num_points):
            true_point = encode_point(i+1)
            if i == 0:
                true_points = true_point
            else:
                true_points = np.hstack((true_points, true_point))
        true_points = true_points.T

    if(rotate == True):

        trans = np.dot(np.linalg.pinv(res), true_points)
        res = res - res[0, :]
        res = np.dot(res, trans)

    if projection != None:
        fig = plt.figure()
        ax = plt.axes(projection="3d")
    if projection == 'scatter':
        ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='hsv')
        plt.show()
    if projection == 'trisurf':
        ax.plot_trisurf(res[:, 0], res[:, 1], res[:, 2], cmap=cm.jet, linewidth=0, antialiased=False)
        plt.show()
    if projection == 'alpha':
        res_list = list(map(tuple, res))
        alpha_shape = alsh.alphashape(res_list, 0.01)
        ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
        plt.show()

    if(err_ord != None):
        if(rotate == False):
            warnings.warn('Rotation flag not set to true, returning unrotated error')
        if err_ord == 'rel':
            return ((np.linalg.norm((res-true_points), 2)) / np.linalg.norm((true_points), 2))
        else:
            return np.linalg.norm((res-true_points), err_ord)
    


if __name__ == '__main__':
    #reconstruct_file('.\cube_gen\Data\dists_test_40.csv', 98)

    filepath = None
    num_points = 98
    point_connections = 97
    noise_percentage = 0
    error_percentage = 0
    return_err_ord = None
    projection = None
    rotate = True
    verbosity = 0

    for param in range(1, len(sys.argv), 2):

        try:
            if (sys.argv[param] == '-f'):
                
                filepath = str(sys.argv[param+1])
            elif (sys.argv[param] == '-p'):
                
                num_points = int(sys.argv[param+1])
                if num_points < 1 or num_points > 98:
                    raise Exception("Number of points to be reconstructed out of bounds. Must be in the interval 1 to 98.")
            
            elif (sys.argv[param] == '-c'):
                
                point_connections = int(sys.argv[param+1])
                if point_connections < 1 or point_connections > 98:
                    raise Exception("Number of point connections out of bounds. Must be in the interval 1 to 97.")
            
            elif (sys.argv[param] == '-n'):
                
                noise_percentage = float(sys.argv[param+1])
                if noise_percentage < 0:
                    raise Exception("Noise percentage must be non-negative.")
            
            elif (sys.argv[param] == '-e'):
                
                error_percentage = float(sys.argv[param+1])
                if error_percentage < 0:
                    raise Exception("Record error percentage must be non-negative.")

            elif (sys.argv[param] == '-g'):
                
                projection = str(sys.argv[param+1])
                if not(projection == 'scatter' or projection == 'trisurf' or projection == 'alpha'):
                    raise Exception("Projection not parseable. Accepted types: scatter, trisurf, alpha.")

            elif (sys.argv[param] == '-r'):

                if (str(sys.argv[param+1])) == 'true' or (str(sys.argv[param+1])) == 'True' or (str(sys.argv[param+1])) == 'TRUE' or (str(sys.argv[param+1])) == '1':
                    rotate = True
                elif (str(sys.argv[param+1])) == 'false' or (str(sys.argv[param+1])) == 'False' or (str(sys.argv[param+1])) == 'FALSE' or (str(sys.argv[param+1])) == '0':
                    rotate = False
                else:
                    raise Exception("Boolean not parseable. Accepted types: true/false, True/False, TRUE/FALSE, 1/0.")
            
            elif (sys.argv[param] == '-eo'):

                if(str(sys.argv[param+1]) == 'rel'):
                    return_err_ord = 'rel'
                else:
                    return_err_ord = int(sys.argv[param+1])
            elif (sys.argv[param] == '-v'):
                verbosity = int(sys.argv[param+1])
                if verbosity < 0:
                    raise Exception("Verbosity must be non-negative.")
                if verbosity > 4:
                    warnings.warn("Verbosity levels above 4 currently have no additional effect.")
            else:
                raise Exception("Parameter not recognized. Accepted types: -p -c -n -e -g -r -eo -v.")

        except:
            raise Exception("Malformed parameters.")

    if filepath == None:
        
        if verbosity > 0: print(">>>>>>>>>>>")
        if verbosity > 0: print("Generating distance list...")
        dist_df = gen_dist_df(num_points, point_connections, noise_percentage, error_percentage, verbosity)
        error = reconstruct(dist_df, projection, rotate, return_err_ord, verbosity)
    else:
        error = reconstruct_file(filepath, projection, rotate, return_err_ord, verbosity)
    
    if return_err_ord != None:
            if return_err_ord == 'rel':
                print("Reconstructed relative error:", error)
            else:
                print("Reconstructed error of order", return_err_ord,":", error)