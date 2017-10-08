import pandas as pd
import numpy as np
from PIL import Image
import os, logging
from convobot.util.TreeUtil import TreeUtil
from convobot.manipulate.Manipulator import Manipulator
from convobot.manipulate.CountManipulator import CountManipulator

logger = logging.getLogger(__name__)

class NumpyManipulator(Manipulator):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        super(NumpyManipulator, self).__init__(cfg_mgr)

        # TODO: Fix TreeUtil to have an inplace option and not copy the
        # tree structure to the output directory now that the manipulators
        # don't copy any of the files.
        counter = CountManipulator(cfg_mgr)
        counter.process()
        image_count = counter.get_count()
        logger.debug('Manipulating %s images', image_count)

        self._image = np.zeros([image_count, self._image_size[0]*self._image_size[1]*self._channels], dtype=np.uint8)
        self._label = np.zeros([image_count, 3], dtype=np.float32)

        logger.debug('Initialized image array: %s', self._image.shape)
        logger.debug('Initialized label array: %s', self._label.shape)

        self._idx = 0
        logger.info('Preparing to store labels and images.')

    def process(self):
        def loader(src_path, dest_path, filename):
            image = Image.open(os.path.join(src_path, filename)).convert('RGB')
            image_np = np.array(image)
            image_np = image_np.reshape(self._image_size[0]*self._image_size[1]*self._channels,)
            self._image[self._idx] = image_np.tolist()

            theta, radius, alpha = self._filename_manager.filename_to_labels(filename)
            label = [theta, radius, alpha]

            for i in range(len(label)):
                self._label[self._idx][i] = label[i]

            self._idx += 1

        tree_util = TreeUtil(self._cfg['SimDirPath'], self._cfg['ManDirPath'])
        tree_util.apply_files(loader, '*.png')
        self._image = self._image.reshape(len(self._image), self._image_size[0], self._image_size[1], self._channels)
        label_file_path = os.path.join(self._cfg['ManDirPath'], 'label.npy')
        image_file_path = os.path.join(self._cfg['ManDirPath'], 'image.npy')

        logger.debug('Saving %s of shape %s', label_file_path, self._label.shape)
        logger.debug('Saving %s of shape %s', image_file_path, self._image.shape)

        np.save(image_file_path, self._image, allow_pickle=False)
        np.save(label_file_path, self._label, allow_pickle=False)
