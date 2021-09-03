import numpy as np
import pandas as pd

import scipy.io
import os

import matlab.engine

from sklearn.manifold import MDS

import matplotlib.pyplot as plt
from matplotlib import cm

def reconstruct(dist_csv_string, num_points):
    
    dist_df = pd.read_csv(dist_csv_string)
    
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

    print(">>>>>>>>>>>")
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "edm_raw.mat")
    scipy.io.savemat(target_path, dict(dist_mat=dist_mat, mask_mat=mask_mat))
    print(target_path)
    print('Incomplete EDM Matrices saved')
    
    print(">>>>>>>>>>>")
    print('Connecting to Matlab...')
    eng = matlab.engine.start_matlab()
    eng.addpath(os.path.dirname(os.path.abspath(__file__)), nargout= 0 )
    eng.addpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data"), nargout= 0 )
    print('Connected')
    print('Script Running')
    eng.matlab_connector(nargout=0)
    print('Script Complete')

    print(">>>>>>>>>>>")
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "recon_edm.mat")
    print(target_path)

    edm = scipy.io.loadmat(target_path)

    print('Loaded matrix shape: ' + str(edm['ans'].shape))

    embedding = MDS(n_components=3, verbose=2, dissimilarity='precomputed', max_iter=3000, eps=1e-12)
    res = embedding.fit_transform(edm['ans'])

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax = plt.axes(projection="3d")
    ax.plot_trisurf(res[:, 0], res[:, 1], res[:, 2], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()


reconstruct('.\cube_gen\dists_test_full.csv', 98)