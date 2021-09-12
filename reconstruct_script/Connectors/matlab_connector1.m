load Data/edm_raw;
lamda = 1;
semidefiniteRelaxation(dist_mat, mask_mat, lamda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm1.mat'),'ans');