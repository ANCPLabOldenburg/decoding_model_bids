#! /usr/bin/env python3
'''Script to run the analysis using decoding_model_v6_script_based.py'''
import os
from sklearn.pipeline import Pipeline
import decoding_v6_script_based as dec
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA

## define parameters for decoding model
lag_par = 4

inp_dir = '/data/akitaitsev/data1/lagged/'
stim_param_dir = '/data/akitaitsev/data1/raw_data/processed_stimuli/'
model_config = {'subjects': ['01']}
out_dir = '/data/akitaitsev/data1/decoding_data3_script_based/'

### spatial models
print('Running spatial models...')
spatial_decoders = [dec.myRidge, dec.myRidge, CCA]

# decoders' configs
ridge_without_pca_config = {"alphas": [0,5,10]}
ridge_with_pca_config = {"alphas": [0,5,10], "var_explained": 0.9}
cca300_config = {"n_components":300}
spatial_decoders_configs = [ridge_without_pca_config, ridge_with_pca_config,\
    cca300_config]
# invoke decoders
spatial_models = dec.invoke_decoders(spatial_decoders, spatial_decoders_configs)

# create output directories for different spatial models
out_dir_spatial = ['ridge','ridge_pca0.9','cca300']

# run decoding models
for model_num  in range(len(spatial_decoders)):
    out_dir_iter = os.path.join(out_dir, 'SM', out_dir_spatial[model_num]) 
    if not os.path.isdir(out_dir_iter):
        print('Creating output directory ' + out_dir_iter + '...')
        os.makedirs(out_dir_iter)
    #dec.run_decoding(inp_dir, out_dir_iter, stim_param_dir, model_config, \
    #   spatial_models[model_num])

### spatial temporal models
print('Running spatial temporal models')


# spatial_temporal models
# create spatial-temporal decoder
spatial_decoders = [PCA, dec.myRidge, CCA]
spatial_decoders_configs = [ {'n_components':400}, {'alphas':[0,5,5],\
    'var_explained':0.9}, {'n_components':400}]
spatial_decoders = dec.invoke_decoders(spatial_decoders, spatial_decoders_configs)

temporal_decoders = [dec.myRidge, dec.myRidge, CCA]
temporal_decoders_configs = [ {'alphas':[0,5,5]}, {'alphas':[0,5,5], 'var_explained': 0.9},\
    {'n_components':200}]
folder_names = ['PCA400_ridge','PCA400_ridgePCA0.9', 'PCA400_cca200', \
    'ridgePCA0.9_ridge', 'ridgePCA0.9_ridgePCA0.9', 'ridgePCA0.9_cca200',\
    'cca400_ridge', 'cca400_ridgePCA0.9', 'cca400_cca200']

folder_cntr = 0 # folder counter
for sp_dec in range(len(spatial_decoders)):
    for tmp_dec in range(len(temporal_decoders)):
        print('Running STM '+folder_names[folder_cntr])
        temporal_decoder = dec.temporal_decoder(temporal_decoders[tmp_dec], temporal_decoders_configs[tmp_dec], lag_par)
        spatial_decoder = spatial_decoders[sp_dec]
        STM = Pipeline([('spatial', spatial_decoder), ('temporal', temporal_decoder)])
        # create output dirs
        out_dir_iter = os.path.join(out_dir, 'STM', folder_names[folder_cntr])
        if not os.path.isdir(out_dir_iter):
            print('Creating output directory ' + out_dir_iter + '...')
            os.makedirs(out_dir_iter)
        # run decoding model
        dec.run_decoding(inp_dir, out_dir_iter, stim_param_dir, model_config, decoder=STM)
        folder_cntr += 1
