# skripsie_2021
Repository containing skripsie of 21595240

# Deterministic Reconstruction Script
(Requires MATLAB with the CVX package)

Call the reconstruction script from the root directory in the format:

python reconstruct_script\reconstruct.py -f <reconstruct_from_filepath=None> -p <num_points=98> -c <connections_per_point=97> -n <noise_percentage=0> -e <error_percentage=0> -g <graph_style=None> -r <rotation_flag=True> -eo <error_order=None> -ret <return_points_flag=False> -v <verbosity=0>

# Probabilistic Reconstruction Script
(Requires EMDW PGM library)

Call the reconstruction script from the root directory in the format:

python reconstruct_pgm\reconstruct.py -p <num_points=98> -c <connections_per_point=97> -n <noise_percentage=0> -e <error_percentage=0> -g <graph_style=None> -i_std <prior_std_dev=None> -i_rand <prior_uniform_ran=None> -l <pgm_lambda=0.8> -i <pgm_max_iter=25> -t <pgm_tol=294> -eo <error_order=None> -ret <return_points_flag=False> -v <verbosity=0>
