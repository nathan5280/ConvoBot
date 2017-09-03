'''
Code to update filenames to match the theta_radius_alpha format.
Should only need this one
'''

import os

data_path = os.path.join('data1')
dirs = os.listdir(data_path)
for dir in dirs:
    if '.' != dir[0]:
        print(dir)
        dist_path = os.path.join(data_path, dir)
        files = os.listdir(dist_path)
        for file in files:
            if 'png' == file[-3:]:
                fn = file[0:-4]
                fnr = fn + '_180' + '.png'
                print('\t', file, fnr)
                os.rename(os.path.join(dist_path, file), os.path.join(dist_path, fnr))
