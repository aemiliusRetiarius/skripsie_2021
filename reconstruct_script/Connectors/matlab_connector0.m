load Data/edm_raw0;
lambda = 10;
semidefiniteRelaxation(dist_mat, mask_mat, lambda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm0.mat'),'ans');