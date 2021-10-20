load Data/edm_raw1;
lambda = 10;
semidefiniteRelaxation(dist_mat, mask_mat, lambda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm1.mat'),'ans');