import numpy as np
import pandas as pd

import scipy.io
import os

import sys

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
print('importing: ', sibling_path)
sys.path.insert(0, sibling_path)

from cube_gen import gen_dist_df

import matlab.engine

from sklearn.manifold import MDS

import matplotlib.pyplot as plt
from matplotlib import cm

def reconstruct_file(dist_csv_string, num_points):
    dist_df = pd.read_csv(dist_csv_string)
    reconstruct(dist_df, num_points)

def reconstruct(dist_df, num_points):
    
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
    print('Script Starting')
    eng.matlab_connector(nargout=0)
    print('Script Complete')

    print(">>>>>>>>>>>")
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Data", "recon_edm.mat")
    print(target_path)

    edm = scipy.io.loadmat(target_path)

    print('Loaded matrix shape: ' + str(edm['ans'].shape))

    embedding = MDS(n_components=3, verbose=1, dissimilarity='precomputed', max_iter=3000, eps=1e-12)
    res = embedding.fit_transform(edm['ans'])

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax = plt.axes(projection="3d")
    #ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='hsv')
    ax.plot_trisurf(res[:, 0], res[:, 1], res[:, 2], cmap=cm.jet, linewidth=0, antialiased=False)
    plt.show()


if __name__ == '__main__':
    #reconstruct_file('.\cube_gen\Data\dists_test_40.csv', 98)
    try:
        num_points = int(sys.argv[1])
        point_connections = int(sys.argv[2])
        noise_percentage = int(sys.argv[3])
    except:
        num_points = 98
        point_connections = 97
        noise_percentage = 0

    dist_df = gen_dist_df(num_points, point_connections, noise_percentage)
    reconstruct(dist_df, num_points)