'''
Convert color images to black and white and resize.
Recursively search directory tree to find images to convert.
Create output directory tree as required.
'''

from PIL import Image
import os
from convobot.util.TreeUtil import TreeUtil
from convobot.transformer.Transformer import Transformer

class ColorConverter(Transformer):
    def __init__(self, cfg_mgr, transform_index, verbose=False):
        super(ColorConverter, self).__init__(cfg_mgr, transform_index, verbose)

        if self._verbose:
            print('Loading StereoStacker Transfomer')

    def process(self):
        '''
        Convert Color files to Gray Scale.
        '''
        def converter(src_path, dst_path, filename):
            img = Image.open(os.path.join(src_path, filename)).convert('RGB')
            img.save(os.path.join(dst_path, filename))
            # print('Converting: {}, {}'.format(os.path.join(src_path, filename), os.path.join(dst_path, filename)))

        self._tree_util.apply_files(converter, '*.png')
