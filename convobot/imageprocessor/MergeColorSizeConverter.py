'''
Convert color images to black and white and resize.
Recursively search directory tree to find images to convert.
Create output directory tree as required.
'''

from PIL import Image
from convobot.util.TreeUtil import TreeUtil
import os

class MergeColorSizeConverter(object):
    def __init__(self, src_l_root, src_r_root, dst_root, resize=None):
        '''
        Args:
            src_root: Source root directory
            dst_root: Target root directory.   This will always be created.
            resize: tuple of the new x and y size.
        '''
        self.tree_util = TreeUtil(src_root, dst_root)
        self._resize = resize
        print('Preparing to convert color/grayscale')

    def process(self):
        '''
        Convert Color files to Gray Scale.
        '''
        def converter(src_l_path, src_r_path, dst_path, filename):
            # Convert from RGBA to RGB
            img_l = Image.open(os.path.join(src_l_path, filename)).convert('RGB')
            img_r = Image.open(os.path.join(src_r_path, filename)).convert('RGB')

            # convert to np.array, concatentate (stack) them on top of each other
            # and convert back to PIL image.
            img_npl = np.array(img_l)
            img_npr = np.array(img_r)
            img_stk = Image.fromarray((img_npl, img_npr))
            img = img_stk.resize((self._resize[0], self._resize[1]))

            img.save(os.path.join(dst_path, filename))
            # print('Converting: {}, {}'.format(os.path.join(src_path, filename), os.path.join(dst_path, filename)))

        self.tree_util.apply_files(converter, '*.png')
