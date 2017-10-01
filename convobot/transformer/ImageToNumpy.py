import pandas as pd
import numpy as np
from PIL import Image
import os
from convobot.util.TreeUtil import TreeUtil
from convobot.util.FilenameManager import FilenameManager
from convobot.transformer.Transformer import Transformer
from convobot.transformer.ImageCounter import ImageCounter

class ImageToNumpy(Transformer):
    def __init__(self, cfg_mgr, transform_index, verbose=False):
        super(ImageToNumpy, self).__init__(cfg_mgr, transform_index, verbose)
        self._img_size = self._cfg_mgr.get_cfg()['Environment']['ImageSize']
        self._channels = 3

        if self._verbose:
            print('Loading ImageToNumpy Transfomer')

        converter = ImageCounter(cfg_mgr, transform_index)
        converter.process()
        img_cnt = converter.get_count()

        self._image = np.zeros([img_cnt, self._img_size[0]*self._img_size[1]*self._channels], dtype=np.uint8)
        self._label = np.zeros([img_cnt, 3], dtype=np.float32)

        self._idx = 0
        self._filename_manager = FilenameManager()
        print('Preparing to store labels and images.')

    def process(self):
        '''
        Get image, convert to numpy array, store in list.
        '''
        def loader(src_path, dest_path, filename):
            img = Image.open(os.path.join(src_path, filename))
            img_np = np.array(img)
            img_np = img_np.reshape(self._img_size[0]*self._img_size[1]*self._channels,)
            self._image[self._idx] = img_np.tolist()

            theta, radius, alpha = self._filename_manager.filename_to_labels(filename)
            label = [theta, radius, alpha]

            for i in range(len(label)):
                self._label[self._idx][i] = label[i]

            self._idx += 1

        self._tree_util.apply_files(loader, '*.png')
        self._image = self._image.reshape(len(self._image), self._img_size[0], self._img_size[1], self._channels)
        # print('Label: ', self._label.shape)
        # print('Image: ', self._image.shape)

        label_file_path, image_file_path = self._cfg_mgr.get_np_array_path(self._output_path)
        print('Saving np.array data to: ', self._output_path)
        np.save(image_file_path, self._image, allow_pickle=False)
        np.save(label_file_path, self._label, allow_pickle=False)
