'''
Count all the images in the tree.
Recursively search directory tree to find images to count.
'''

from convobot.util.TreeUtil import TreeUtil
import os

class ImageCounter(object):
    def __init__(self, src_root, dst_root):
        '''
        Args:
            src_root: Source root directory
            dst_root: Target root directory.   This will always be created.
        '''
        self.tree_util = TreeUtil(src_root, dst_root)
        self._count = 0

    def get_count(self):
        return self._count

    def process(self):
        '''
        Count the images.
        '''
        def converter(src_path, dst_path, filename):
            self._count += 1
            print('Counting: {}, {}'.format(os.path.join(src_path, filename), os.path.join(dst_path, filename)))

        self.tree_util.apply_files(converter, '*.png')
