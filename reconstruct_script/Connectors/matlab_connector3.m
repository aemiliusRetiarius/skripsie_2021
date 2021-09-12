load Data/edm_raw3;
lamda = 1;
semidefiniteRelaxation(dist_mat, mask_mat, lamda);
save(strcat(pwd, '/reconstruct_script/Data/recon_edm3.mat'),'ans');