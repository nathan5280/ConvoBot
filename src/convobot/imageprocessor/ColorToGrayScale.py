'''
Convert color images to black and white and resize.
Recursively search directory tree to find images to convert.
Create output directory tree as required.
'''

from PIL import Image
from convobot.util.TreeUtil import TreeUtil
import os

class ColorToGrayScale(object):
    def __init__(self, src_root, dst_root, resize=None):
        '''
        Args:
            src_root: Source root directory
            dst_root: Target root directory.   This will always be created.
            resize: tuple of the new x and y size.
        '''
        self.tree_util = TreeUtil(src_root, dst_root)
        self._resize = resize

    def process(self):
        '''
        Convert Color files to Gray Scale.
        '''
        def converter(src_path, dst_path, filename):
            img = Image.open(os.path.join(src_path, filename)).convert('L')
            if self._resize:
                img.thumbnail(self._resize, Image.ANTIALIAS)
            img.save(os.path.join(dst_path, filename))
            print('Processing: {}, {}', os.path.join(src_path, filename), os.path.join(dst_path, filename))

        print('Processing: ')
        self.tree_util.apply_files(converter, '*.png')

def main():
    converter = ColorToGrayScale('../Data/dataset1', './Data/dataset1/gs_28x28', (28, 28))
    converter.process()

if __name__ == '__main__':
    main()
