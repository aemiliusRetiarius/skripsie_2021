load Data/edm_raw2;
lamda = 1;
semidefiniteRelaxation(dist_mat, mask_mat, lamda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm2.mat'),'ans');