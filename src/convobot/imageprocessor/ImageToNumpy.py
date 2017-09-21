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
    def __init__(self, src_root, dst_root):
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

        self._img = np.zeros([img_cnt, 28, 28], dtype=np.uint8)
        self._label = np.zeros([img_cnt, 3], dtype=np.float32)
        self._idx = 0
        self._filename_manager = FilenameManager()

    def process(self):
        '''
        Get image, convert to numpy array, store in list.
        '''
        def loader(src_path, dst_path, filename):
            img = Image.open(os.path.join(src_path, filename))
            img_list = np.array(img).tolist()
            theta, radius, alpha = self._filename_manager.filename_to_labels(filename)
            label = [theta, radius, alpha]

            for i in range(len(label)):
                self._label[self._idx][i] = label[i]

            for i in range(len(img_list)):
                for j in range(len(img_list[0])):
                    self._img[self._idx][i][j] = img_list[i][j]

            self._idx += 1
            print('Storing: {}, {}', os.path.join(src_path, filename), os.path.join(dst_path, filename))

        self.tree_util.apply_files(loader, '*.png')

    def get_data(self):
        return self._label, self._img

def main():
    converter = ColorToGrayScale('../Data/dataset1', './Data/dataset1/gs_28x28', (28, 28))
    converter.process()

if __name__ == '__main__':
    main()
