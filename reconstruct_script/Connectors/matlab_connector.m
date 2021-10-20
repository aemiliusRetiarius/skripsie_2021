load Data/edm_raw;
lamda = 0.5;
semidefiniteRelaxation(dist_mat, mask_mat, lamda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm.mat'),'ans');