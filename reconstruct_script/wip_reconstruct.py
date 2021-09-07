from operator import rshift
import numpy as np
from numpy.linalg.linalg import cholesky
import pandas as pd
import json

import matlab.engine
import scipy.io

from sklearn.manifold import MDS
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh
from descartes import PolygonPatch
#from mayavi import mlab


def reconstruct(dist_csv_string, num_points):
    dist_df = pd.read_csv(dist_csv_string)
    num_obs = dist_df.shape[0]
    
    #coef mat: x1, y1, z1, x2, y2, z2, x3, etc.
    coef_mat = np.zeros((num_obs, num_points*3)) #mul by 3 for 3 coords per point
    sq_dist_mat = np.zeros((num_obs, 1))
    dist_mat = np.zeros((num_points, num_points)) #dist matrix between points for MDS
    mask_mat = np.zeros((num_points, num_points))

    for index, row in dist_df.iterrows():
        
        source_index = int(row['source']) - 1 #offset
        target_index = int(row['target']) - 1 #offser=t
        sq_dist = row['dist']**2
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

    #res = np.dot(np.linalg.pinv(coef_mat), sq_dist_mat)
    
    #gram = np.dot(coef_mat, np.transpose(coef_mat))
    #w = np.dot(np.linalg.pinv(gram), sq_dist_mat)
    #res = np.dot(np.transpose(coef_mat), w)
    
    #res = np.linalg.lstsq(coef_mat, sq_dist_mat, rcond=None)

    #res = abs((np.min(res))) + res
    #res = np.sqrt(res)

    #perform MDS with sklearn
    #embedding = MDS(n_components=3, verbose=2, dissimilarity='precomputed', max_iter=3000, eps=1e-12)
    #res = embedding.fit_transform(dist_mat)
    #print(res.shape)
    #print(test_dist)
    
    #perform manual MDS
    #print(dist_mat[0, :])
    #D_1_j_sq = np.dot(dist_mat[0, :][:,np.newaxis], dist_mat[0, :][np.newaxis,:])
    #D_i_1_sq = np.dot(dist_mat[:, 0][:,np.newaxis], dist_mat[:, 0][np.newaxis,:])
    #m_dist_mat = 0.5*(D_1_j_sq + D_i_1_sq - np.dot(dist_mat, dist_mat))
    #print(m_dist_mat)
    #np.linalg.cholesky(m_dist_mat)
    #sing, eig = np.linalg.eig(m_dist_mat)
    #print(sing.shape)
    #sing = np.sqrt(np.diag(np.absolute(sing)))
    #res = np.dot(eig, sing)
    #print(res)
    #print(res.shape)
    #print(res)

    #Drineas et. al.

    #SVD-RECONSTRUCT

    #P_i_j = ( (num_obs/num_points) *2) / num_points
    #gamma = 50
    
    #construct S
    #S = np.zeros((num_points, num_points))
    
    #for row in range(num_points):
    #    for col in range(num_points):
    #        if(dist_mat[row, col] != 0):
    #            S[row, col] = ((dist_mat[row, col]**2) - gamma*(1-P_i_j)) / P_i_j
    #        else:
    #            S[row, col] = gamma

    #construct rank 4 approximation of S
    #rank = 4
    #P, D, Q = np.linalg.svd(S)
    #S_4 = np.matrix(P[:, :rank]) * np.diag(D[:rank]) * np.matrix(Q[:rank, :])

    #Run MDSLOCALIZE on S4

    #MDSLOCALIZE

    #L = np.identity(num_points) - (1/num_points) * np.ones((num_points, num_points))

    #tau = -0.5 * np.dot(L, np.dot(S_4, L)) #-0.5 * L D L
    #P, D, Q = np.linalg.svd(tau)
    #rank = 2
    #res = np.matrix(P[:, :rank]) * np.sqrt(np.diag(D[:rank]))

    embedding = MDS(n_components=3, verbose=2, dissimilarity='precomputed', max_iter=3000, eps=1e-12)
    res = embedding.fit_transform(dist_mat)

    #SEMIDEFINITE RELAXATION

    #scipy.io.savemat('.\\reconstruct_script\edm_raw.mat', dict(dist_mat=dist_mat, mask_mat=mask_mat))
    
    #mat_conv = matlab.double(mat_test.tolist())
    
    #print("connecting to matlab")
    #edm, x = eng.semidefiniteRelaxation(mat_conv, mat_conv, matlab.double(1), nargout=2)

    #print(type(edm))
    #print(x.shape)

    

    #PCA TEST

    #pca = PCA(n_components=3)
    #res = pca.fit_transform(res)

    #PlOTTING

    #plt.scatter([res[:,0]], [res[:,1]])
    #plt.show()

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax = plt.axes(projection="3d")

    #ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='hsv')
    #ax.plot_trisurf(res[:, 0], res[:, 1], res[:, 2], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    #ax.plot_wireframe(res[:, 0], res[:, 1], res[:, 2],rstride=10, cstride=10)
    #test_dist = (res[2, 0]**2 + res[2, 1]**2 + res[2, 2]**2 + res[3, 0]**2 + res[3, 1]**2 + res[3, 2]**2)**0.5
    
    #alphashape
    points_2d = [(0., 0.), (0., 1.), (1., 1.), (1., 0.),
          (0.5, 0.25), (0.5, 0.75), (0.25, 0.5), (0.75, 0.5)]
    points_3d = [
    (0., 2., -1.), (3., -2., 1.), (3., 2., -1.),
    (0., 2., -1.), (3., -2., 1.), (3., 2., -1.),
    ]
    
    #fig, ax = plt.subplots()
    res_list = list(map(tuple, res))
    alpha_shape = alsh.alphashape(res_list, 0.005)
    #print(alpha_shape)
    #ax.scatter(*zip(*res_list))
    #ax.add_patch(PolygonPatch(alpha_shape, alpha=0.2))
    
    #print(res_list[0])
    #alpha_shape = alsh.alphashape(res_list)
    ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces,cmap=cm.jet)

    #delauny
    #pts = mlab.points3d(res[:, 0], res[:, 1], res[:, 2], res[:, 2])

    plt.show()

#reconstruct('.\cube_gen\dists.csv', 98)
#reconstruct('.\cube_gen\dists_test_49.csv', 98)
#reconstruct('.\cube_gen\dists_test_90.csv', 98)
reconstruct('.\cube_gen\Data\dists_test_full.csv', 98)
#reconstruct('.\cube_gen\Data\dists_test_2d_full.csv', 25)