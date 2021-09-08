import numpy as np
import pandas as pd

import scipy.io
import io
import os

import sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df

import matlab.engine

from sklearn.manifold import MDS

import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

def reconstruct_file(dist_csv_string, projection, verbosity=0):
    dist_df = pd.read_csv(dist_csv_string)
    num_points = int(max(dist_df['source'].max(), dist_df['source'].max())) +1
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print("Reconstructing with", num_points, "points")
    reconstruct(dist_df, num_points, projection, verbosity)

def reconstruct(dist_df, num_points, projection, verbosity=0):
    
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
    


if __name__ == '__main__':
    #reconstruct_file('.\cube_gen\Data\dists_test_40.csv', 98)

    filepath = None
    num_points = 98
    point_connections = 97
    noise_percentage = 0
    error_percentage = 0
    projection = 'alpha'
    verbosity = 0

    for param in range(1, len(sys.argv), 2):

        try:
            if (sys.argv[param] == '-f'):
                filepath = str(sys.argv[param+1])
            elif (sys.argv[param] == '-p'):
                num_points = int(sys.argv[param+1])
            elif (sys.argv[param] == '-c'):
                point_connections = int(sys.argv[param+1])
            elif (sys.argv[param] == '-n'):
                noise_percentage = float(sys.argv[param+1])
            elif (sys.argv[param] == '-e'):
                error_percentage = float(sys.argv[param+1])
            elif (sys.argv[param] == '-g'):
                projection = str(sys.argv[param+1])
            elif (sys.argv[param] == '-v'):
                verbosity = int(sys.argv[param+1])
            else:
                raise Exception("Parameter not recognized. Accepted types: -p -c -n -g -v")

        except:
            raise Exception("Malformed parameters.")

    if filepath == None:
        if verbosity > 0: print(">>>>>>>>>>>")
        if verbosity > 0: print("Generating distance list...")
        dist_df = gen_dist_df(num_points, point_connections, noise_percentage, error_percentage, verbosity)
        reconstruct(dist_df, num_points, projection, verbosity)
    else:
        reconstruct_file(filepath, projection, verbosity)