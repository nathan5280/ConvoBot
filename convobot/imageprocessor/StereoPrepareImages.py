from convobot.imageprocessor.MergeColorSizeConverter import MergeColorSizeConverter
from convobot.imageprocessor.ImageCounter import ImageCounter
from convobot.imageprocessor.ImageToNumpy import ImageToNumpy
from convobot.workflow.Environment import Environment
import pickle
import os
import pandas as pd
import numpy as np
import sys, getopt

c2g = True
cnt = False
i2n = True

class StereoPrepareImages(object):
    def process(self, data_root, cfg_root, cfg_name):
        # load the simulation configuration from the convobot environment.
        processing_env = Environment(cfg_root, data_root, verbose=False)
        cfg = processing_env.get_processing_cfg(cfg_name)

        src_l_path, src_r_path, dest_path = processing_env.get_stereo_processing_path()

        print(src_l_path, src_r_path)

        size = cfg['size']
        grayscale = not cfg['color']

        if c2g:
            print('\tConverting')
            target_size = None
            if cfg['resize']:
                target_size = size

            converter = MergeColorSizeConverter(src_l_path, src_r_path, dest_path, resize=target_size)
            converter.process()

        if cnt:
            print('\tCounting')
            converter = ImageCounter(dest_path, dest_path)
            converter.process()
            img_cnt = converter.get_count()
            print('Images in dataset: ', img_cnt)

        if i2n:
            print('\tStoring')
            converter = ImageToNumpy(dest_path, dest_path, grayscale=grayscale, size=size)
            converter.process()
            label, image = converter.get_data()
            print('Label: ', label.shape)
            print('Image: ', image.shape)

            label_file_path, image_file_path = processing_env.get_np_array_path()
            np.save(image_file_path, image, allow_pickle=False)

            with open(label_file_path, 'wb') as f:
                pickle.dump(label, f)

            with open(image_file_path, 'wb') as f:
                pickle.dump(image, f)
