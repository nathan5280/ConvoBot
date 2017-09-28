'''
Convert images to numpy array, stack with labels.
Recursively search directory tree to find images to convert.
Create output directory tree as required.
'''

import pandas as pd
import numpy as np
from PIL import Image
from convobot.util.TreeUtil import TreeUtil
from convobot.util.FilenameManager import FilenameManager
from convobot.imageprocessor.ImageCounter import ImageCounter
import os

class ImageToNumpy(object):
    def __init__(self, src_root, dst_root, grayscale, size):
        '''
        Args:
            src_root: Source root directory
            dst_root: Target root directory.   This will always be created.
            resize: tuple of the new x and y size.
        '''
        self.tree_util = TreeUtil(src_root, dst_root)

        converter = ImageCounter(src_root, src_root)
        converter.process()
        img_cnt = converter.get_count()

        self._size = size
        self._grayscale = grayscale

        self._color_layers = 1
        if not self._grayscale:
            self._color_layers = 3

        self._img = np.zeros([img_cnt, size[0]*size[1]*self._color_layers], dtype=np.uint8)
        self._label = np.zeros([img_cnt, 3], dtype=np.float32)
        self._idx = 0
        self._filename_manager = FilenameManager()

    def process(self):
        '''
        Get image, convert to numpy array, store in list.
        '''
        def loader(src_path, dest_path, filename):
            img = Image.open(os.path.join(src_path, filename))
            img_np = np.array(img)

            img_np = img_np.reshape(self._size[0]*self._size[1]*self._color_layers,)
            self._img[self._idx] = img_np.tolist()

            theta, radius, alpha = self._filename_manager.filename_to_labels(filename)
            label = [theta, radius, alpha]

            for i in range(len(label)):
                self._label[self._idx][i] = label[i]

            self._idx += 1
            print('Storing: {}, {}'.format(os.path.join(src_path, filename),
                            os.path.join(dest_path, filename)))

        self.tree_util.apply_files(loader, '*.png')

    def get_data(self):
        if self._grayscale:
            return self._label, self._img.reshape(len(self._img), self._size[0], self._size[1])
        else:
            return self._label, self._img.reshape(len(self._img), self._size[0], self._size[1], self._color_layers)
