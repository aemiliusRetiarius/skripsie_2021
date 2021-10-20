load Data/edm_raw;
lambda = 10;
semidefiniteRelaxation(dist_mat, mask_mat, lambda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm.mat'),'ans');