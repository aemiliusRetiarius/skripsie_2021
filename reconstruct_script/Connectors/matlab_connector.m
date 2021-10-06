load Data/edm_raw;
lamda = 1;
semidefiniteRelaxation(dist_mat, mask_mat, lamda);
save(strcat(pwd, '/Data/recon_edm.mat'),'ans');