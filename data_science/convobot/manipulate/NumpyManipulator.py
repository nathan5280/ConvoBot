import pandas as pd
import numpy as np
from PIL import Image
import os
import logging
from convobot.util.TreeUtil import TreeUtil
from convobot.manipulate.Manipulator import Manipulator
from convobot.manipulate.CountManipulator import CountManipulator

logger = logging.getLogger(__name__)

class NumpyManipulator(Manipulator):
    '''
    The primary manipulator loader used for convobot.  This Manipulator
    converts the images from RGBA to RGB and stacks them in a numpy array
    to feed into Keras/TensorFlow.
    '''

    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: The global configuration manager.
        '''
        logger.debug('Initializing')
        super(NumpyManipulator, self).__init__(cfg_mgr)

        # TODO: Fix TreeUtil to have an inplace option and not copy the
        # tree structure to the output directory now that the manipulators
        # don't copy any of the files.
        counter = CountManipulator(cfg_mgr)
        counter.process()
        image_count = counter.get_count()
        logger.debug('Manipulating %s images', image_count)

        # Pre-allocate the arrays to hold the images and labels.  Allocating the
        # arrays up front significantly speeds things up by avoiding continual
        # memory reallocation of the space for the numpy array everytime that an image
        # is appended to the array.

        # Store the image as uint8 as it takes less space than normalizing it to
        # float at this point.
        self._image = np.zeros([image_count, self._image_size[0]
                                * self._image_size[1] * self._channels], dtype=np.uint8)
        self._label = np.zeros([image_count, 3], dtype=np.float32)

        logger.debug('Initialized image array: %s', self._image.shape)
        logger.debug('Initialized label array: %s', self._label.shape)

        self._idx = 0
        logger.info('Preparing to store labels and images.')

    def process(self):
        '''
        Instruct the manipulator to apply the loader function to the tree utility.
        This is the functional programming implementation of applying the transform
        to the objects (images).
        '''
        def loader(src_path, dest_path, filename):
            '''
            This is the transform that is functionally applied to the files as
            the image tree is traversed.

            Args:
              src_path: The path where the source file (image) is located.
              dest_path: The path where the transformed file (image) should be stored.
              filename: The filename of image to be transformed.

            Returns:  None

            '''
            # Load the image and convert it from 4 channels (RGBA) to 3 channels (RGB)
            # Convert to a numpy array of shape N x N x 3.
            image = Image.open(os.path.join(src_path, filename)).convert('RGB')
            image_np = np.array(image)
            image_np = image_np.reshape(
                self._image_size[0] * self._image_size[1] * self._channels,)

            # Repace the image location in the pre-allocated array with the one
            # that was just loaded.
            self._image[self._idx] = image_np.tolist()

            # Extract the features from the filename and add them to the
            # corresponding row in the label array.
            # TODO: Use typed numpy array so that the labels and the images
            # are in one array.  This will cut down on the chance that the
            # images and labels somehow get mismatched.
            theta, radius, alpha = \
                    self._filename_manager.filename_to_labels(filename)
            label = [theta, radius, alpha]

            for i in range(len(label)):
                self._label[self._idx][i] = label[i]

            self._idx += 1

        # The tree walk that functionally applies the loader method to each file.
        # Instantiate the tree walker.  Build the numpy arrays of the labels
        # and images.  Get everything into the right shape.
        tree_util = TreeUtil(self._cfg['SimDirPath'], self._cfg['ManDirPath'])
        tree_util.apply_files(loader, '*.png')
        self._image = self._image.reshape(
            len(self._image), self._image_size[0], self._image_size[1], self._channels)
        label_file_path = os.path.join(self._cfg['ManDirPath'], 'label.npy')
        image_file_path = os.path.join(self._cfg['ManDirPath'], 'image.npy')

        logger.debug(
            'Saving %s of shape %s',
            label_file_path,
            self._label.shape)
        logger.debug(
            'Saving %s of shape %s',
            image_file_path,
            self._image.shape)

        # Save the label and image numpy arrays to the manipulate directory.
        np.save(image_file_path, self._image, allow_pickle=False)
        np.save(label_file_path, self._label, allow_pickle=False)
