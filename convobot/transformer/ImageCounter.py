'''
Count all the images in the tree.
Recursively search directory tree to find images to count.
'''

from convobot.transformer.Transformer import Transformer
from convobot.util.TreeUtil import TreeUtil
import os

class ImageCounter(Transformer):
    def __init__(self, cfg_mgr, transform_index, verbose=False):
        super(ImageCounter, self).__init__(cfg_mgr, transform_index, verbose)

        self._img_size = self._cfg_mgr.get_cfg()['Environment']['ImageSize']

        if self._verbose:
            print('Loading ImageCounter Transfomer')

        self._count = 0

    def get_count(self):
        return self._count

    def process(self):
        '''
        Count the images.
        '''
        def converter(src_path, dst_path, filename):
            self._count += 1
            # print('Counting: {}, {}'.format(os.path.join(src_path, filename), os.path.join(dst_path, filename)))

        self._tree_util.apply_files(converter, '*.png')
