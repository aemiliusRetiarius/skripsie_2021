#TODO: add function to observe dimensions from file 

import numpy as np
import pandas as pd

from sklearn.metrics import euclidean_distances

import matplotlib.pyplot as plt
from matplotlib import cm
import alphashape as alsh

import subprocess
import os, sys, warnings

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cube_gen')
sys.path.insert(0, sibling_path)

from cube_gen import get_point_coords, gen_dist_df, get_true_points_array

sibling_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'common_tools')
sys.path.insert(0, sibling_path)

from common_tools import get_uniform_point_coords

def get_normalized_error(old_dist, new_dist):
    return abs(new_dist - old_dist) / old_dist

def reconstruct(dist_df, init_std=None, init_rand=None, projection=None, err_ord=None, ret_points=None, pgm_lambda=0.8, pgm_max_iter=20, pgm_tol=294, verbosity=0):
    
    program_path = './reconstruct_pgm/build/src/reconstruct_pgm'
    priorPos_path = './reconstruct_pgm/Data/working_init_pos.csv'
    dists_path = './reconstruct_pgm/Data/distance_measurements.csv'
    results_path = "./reconstruct_pgm/Data/result.csv"
    dist_df.to_csv(dists_path)

    num_points = int(max(dist_df['source'].max(), dist_df['target'].max()))
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print('Reconstructing from', num_points, 'points')
    if verbosity > 0: print(">>>>>>>>>>>")
    
    if verbosity > 0: print('Initialising prior positions')

    if init_std != None:
        pos_df = get_point_coords(init_std)
    if init_rand != None:
        pos_df = get_uniform_point_coords()

    if (init_std == None) and (init_rand == None):
        raise Exception("Prior initialisation must be specified")
    if (init_std != None) and (init_rand != None):
        warnings.warn('Prior initialisation overspecified, using random initialisation')

    if verbosity > 0: print('Prior positions initialised')
    #Ditch

    #pos_df.iloc[0,1] = 0
    #pos_df.iloc[0,2] = 0
    #pos_df.iloc[0,3] = 0
    #pos_df.iloc[0,4] = 0
    #pos_df.iloc[0,5] = 0
    #pos_df.iloc[0,6] = 0

    #pos_df.iloc[1,1] = 0
    #pos_df.iloc[1,3] = 0
    #pos_df.iloc[1,2] = 9.08269
    #pos_df.iloc[1,4] = 0

    #pos_df.iloc[2,3] = 0
    #pos_df.iloc[2,6] = 0

    #pos_df.iloc[3,3] = 0
    #pos_df.iloc[3,6] = 0

    #pos_df.iloc[4,3] = 0
    #pos_df.iloc[4,6] = 0

    #pos_df.iloc[5,3] = 0
    #pos_df.iloc[5,6] = 0

    #pos_df.iloc[6,3] = 0
    #pos_df.iloc[6,6] = 0

    #/Ditch

    # point1
    pos_df.iloc[0,1] = 0
    pos_df.iloc[0,2] = 0
    pos_df.iloc[0,3] = 0
    pos_df.iloc[0,4] = 0
    pos_df.iloc[0,5] = 0
    pos_df.iloc[0,6] = 0
    # point5
    pos_df.iloc[4,1] = 100
    pos_df.iloc[4,2] = 0 #
    pos_df.iloc[4,3] = 0 #
    pos_df.iloc[4,4] = 0
    pos_df.iloc[4,5] = 0 #
    pos_df.iloc[4,6] = 0 #
    # point21
    pos_df.iloc[20,1] = 0 #
    pos_df.iloc[20,2] = 0 #
    pos_df.iloc[20,3] = 100
    pos_df.iloc[20,4] = 0 #
    pos_df.iloc[20,5] = 0 #
    pos_df.iloc[20,6] = 0
    # point30
    pos_df.iloc[29,1] = 0 #
    pos_df.iloc[29,2] = 100
    pos_df.iloc[29,3] = 0 #
    pos_df.iloc[29,4] = 0 #
    pos_df.iloc[29,5] = 0
    pos_df.iloc[29,6] = 0 #

    if verbosity > 0: print('Prior positions observed')

    pos_df.to_csv(priorPos_path)
    
    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print('PGM script starting...')

    status = subprocess.run([program_path, "--p", priorPos_path, "--d", dists_path, "--r", results_path, "-l", str(pgm_lambda), "-t", str(pgm_tol), "-i", str(pgm_max_iter), "-f","true"])
    print("status code: ",status.returncode) # will return -6 if cov underflows

    if status.returncode == -6:
        raise Exception("PGM script failed. This is probably due to underflow of the covariance matrices. Consider increasing lambda/tolerance or lowering the maximum iterations.")

    if verbosity > 0: print('PGM Script Complete')

    if verbosity > 0: print(">>>>>>>>>>>")
    if verbosity > 0: print('Reading inferred positions')

    res_df = pd.read_csv(results_path, index_col=0)
    res = np.zeros((98,3))

    for i in range(98):
        res[i,0] = res_df["x_pos"][i]
        res[i,1] = res_df["y_pos"][i]
        res[i,2] = res_df["z_pos"][i]

    true_points = get_true_points_array()

    #trans = np.zeros((3,3))
    #trans = np.dot(np.linalg.pinv(res), true_points)
    #res = res - res[0, :]
    #res = np.dot(res, trans)
    #print(trans)

    if projection != None:
        fig = plt.figure()
        ax = plt.axes(projection="3d")
    if projection == 'scatter':
        ax.scatter3D(res[:, 0], res[:, 1], res[:, 2], c=res[:, 2], cmap='viridis')
        plt.show()
    if projection == 'trisurf':
        ax.plot_trisurf(res[:, 0], res[:, 1], res[:, 2], cmap=cm.jet, linewidth=0, antialiased=False)
        plt.show()
    if projection == 'alpha':
        res_list = list(map(tuple, res))
        alpha_shape = alsh.alphashape(res_list, 0.01)
        ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, cmap=cm.coolwarm)
        plt.show()

    #only return error of specified order
    if(err_ord != None) and ((ret_points == None) or (ret_points == False)):
        
        if err_ord == 'edm_rel':

            true_edm = euclidean_distances(true_points)
            res_edm = euclidean_distances(res)
            return ((np.linalg.norm(true_edm-res_edm)) / np.linalg.norm(true_edm))
        
        elif err_ord == 'rel':
            return ((np.linalg.norm(res-true_points)) / np.linalg.norm(true_points))
        
        else:
            return np.linalg.norm((res-true_points), err_ord)
    
    #only return reconstructed points
    if(err_ord == None) and (ret_points == True):
        return res

    #return both error of specified order and reconstructed points
    if(err_ord != None) and (ret_points == True):
        
        if err_ord == 'edm_rel':
            true_edm = euclidean_distances(true_points)
            res_edm = euclidean_distances(res)
            return ((np.linalg.norm(true_edm-res_edm)) / np.linalg.norm(true_edm)), res
        
        elif err_ord == 'rel':
            return ((np.linalg.norm(res-true_points)) / np.linalg.norm(true_points)) , res
        
        else:
            return np.linalg.norm((res-true_points), err_ord), res

#dist_df.drop(['new_dist','normalized_error'], inplace=True, axis=1)
#dist_df.to_csv(dists_path)

if __name__ == '__main__':
    #reconstruct_file('.\cube_gen\Data\dists_test_40.csv', 98)

    num_points = 98
    point_connections = 97
    noise_percentage = 0
    error_percentage = 0
    init_std=None
    init_rand=None
    pgm_lambda = 0.8
    pgm_max_iter = 20
    pgm_tol = 294
    return_err_ord = None
    return_points = None
    projection = None
    verbosity = 0

    for param in range(1, len(sys.argv), 2):

        try:
            if (sys.argv[param] == '-p'): #Number of points to reconstruct
                
                num_points = int(sys.argv[param+1])
                if num_points < 1 or num_points > 98:
                    raise Exception("Number of points to be reconstructed out of bounds. Must be in the interval 1 to 98.")
            
            elif (sys.argv[param] == '-c'): #Number of connections per point
                
                point_connections = int(sys.argv[param+1])
                if point_connections < 1 or point_connections > 98:
                    raise Exception("Number of point connections out of bounds. Must be in the interval 1 to 97.")
            
            elif (sys.argv[param] == '-n'): #Noise percentage (3.5 sigma)
                
                noise_percentage = float(sys.argv[param+1])
                if noise_percentage < 0:
                    raise Exception("Noise percentage must be non-negative.")
            
            elif (sys.argv[param] == '-e'): #Record percentage to change
                
                error_percentage = float(sys.argv[param+1])
                if error_percentage < 0:
                    raise Exception("Record error percentage must be non-negative.")

            elif (sys.argv[param] == '-i_std'): #Initialisation standard deviation for prior
                
                init_std = float(sys.argv[param+1])
                if init_std < 0:
                    raise Exception("Initialisation standard deviation must be non-negative.")

            elif (sys.argv[param] == '-i_rand'): #Initialisation standard deviation for prior
                
                init_rand = float(sys.argv[param+1])
                if init_rand < 0:
                    raise Exception("Initialisation uniform random cube side length must be non-negative.")

            elif (sys.argv[param] == '-l'): #pgm lambda damping factor
                
                pgm_lambda = float(sys.argv[param+1])
                if pgm_lambda < 0:
                    raise Exception("PGM lambda damping factor must be non-negative.")

            elif (sys.argv[param] == '-i'): #pgm max iter
                
                pgm_max_iter = float(sys.argv[param+1])
                if pgm_max_iter < 0:
                    raise Exception("PGM maximum iterations must be non-negative.")

            elif (sys.argv[param] == '-t'): #pgm tolerance
                
                pgm_tol = float(sys.argv[param+1])
                if pgm_tol < 0:
                    raise Exception("PGM convergence tolerance must be non-negative.")

            elif (sys.argv[param] == '-g'): #Graph mode
                
                projection = str(sys.argv[param+1])
                if not(projection == 'scatter' or projection == 'trisurf' or projection == 'alpha'):
                    raise Exception("Projection not parseable. Accepted types: scatter, trisurf, alpha.")
            
            elif (sys.argv[param] == '-eo'): #Order of error returned

                if(str(sys.argv[param+1]) == 'rel'):
                    return_err_ord = 'rel'
                elif(str(sys.argv[param+1]) == 'edm_rel'):
                    return_err_ord = 'edm_rel'
                else:
                    return_err_ord = int(sys.argv[param+1])
            
            elif(sys.argv[param] == '-ret'):

                if (str(sys.argv[param+1])) == 'true' or (str(sys.argv[param+1])) == 'True' or (str(sys.argv[param+1])) == 'TRUE' or (str(sys.argv[param+1])) == '1':
                    return_points = True
                elif (str(sys.argv[param+1])) == 'false' or (str(sys.argv[param+1])) == 'False' or (str(sys.argv[param+1])) == 'FALSE' or (str(sys.argv[param+1])) == '0':
                    return_points = False
                else:
                    raise Exception("Boolean not parseable. Accepted types: true/false, True/False, TRUE/FALSE, 1/0.")

            elif (sys.argv[param] == '-v'): #Level of verbosity

                verbosity = int(sys.argv[param+1])
                if verbosity < 0:
                    raise Exception("Verbosity must be non-negative.")
                if verbosity > 4:
                    warnings.warn("Verbosity levels above 4 currently have no additional effect.")

            else:
                raise Exception("Parameter not recognized. Accepted types: -p -c -n -e -g -r -eo -ret -v.")

        except:
            raise Exception("Malformed parameters.")


    dist_df = gen_dist_df(num_points, point_connections, noise_percentage, error_percentage, verbosity)
        
    if return_err_ord == None and return_points == None:
        reconstruct(dist_df, init_std, init_rand, projection, return_err_ord, return_points, pgm_lambda, pgm_max_iter, pgm_tol, verbosity)
    elif return_err_ord != None and return_points == None:
        error = reconstruct(dist_df, init_std, init_rand, projection, return_err_ord, return_points, pgm_lambda, pgm_max_iter, pgm_tol, verbosity)
    elif return_err_ord == None and return_points != None:
        points = reconstruct(dist_df, init_std, init_rand, projection, return_err_ord, return_points, pgm_lambda, pgm_max_iter, pgm_tol, verbosity)
    else:
        error, points = reconstruct(dist_df, init_std, init_rand, projection, return_err_ord, return_points, pgm_lambda, pgm_max_iter, pgm_tol, verbosity)
    
    if return_points != None:
        print("Reconstructed Points:")
        print(points)

    if return_err_ord != None:
            if return_err_ord == 'rel':
                print("Reconstructed relative error:", error)
            else:
                print("Reconstructed error of order", return_err_ord,":", error)
