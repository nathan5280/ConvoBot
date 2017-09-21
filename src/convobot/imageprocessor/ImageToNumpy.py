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

        self._img = np.zeros([img_cnt, 784], dtype=np.uint8)
        self._label = np.zeros([img_cnt, 3], dtype=np.float32)
        self._idx = 0
        self._filename_manager = FilenameManager()

    def process(self):
        '''
        Get image, convert to numpy array, store in list.
        '''
        def loader(src_path, dst_path, filename):
            img = Image.open(os.path.join(src_path, filename))
            img_np = np.array(img)

            img_np = img_np.reshape(784,)
            self._img[self._idx] = img_np.tolist()

            theta, radius, alpha = self._filename_manager.filename_to_labels(filename)
            label = [theta, radius, alpha]

            for i in range(len(label)):
                self._label[self._idx][i] = label[i]

            self._idx += 1
            print('Storing: {}, {}', os.path.join(src_path, filename), os.path.join(dst_path, filename))

        self.tree_util.apply_files(loader, '*.png')

    def get_data(self):
        return self._label, self._img.reshape(len(self._img), 28, 28)

def main():
    converter = ColorToGrayScale('../Data/dataset1', './Data/dataset1/gs_28x28', (28, 28))
    converter.process()

if __name__ == '__main__':
    main()
