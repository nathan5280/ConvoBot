import logging
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

phase_train = 'train'
phase_test = 'test'
phase_val = 'val'
dataset_image = 'image'
dataset_label = 'label'
ext = '.npy'

# TODO: Store all of the label and image data together in a single typed
# numpy array.   This will make it simpler to keep the label and image data
# together and in sync.

class DataWrapper(object):
    '''
    Manage how the label and image data is saved and loaded from disk.  Also
    manage the splitting of the data into train, test and validation datasets.
    '''

    def __init__(self, cfg_mgr, data_conditioner):
        '''
        Args:
            cfg_mgr: Global configuration manager.
            data_conditioner: Handle any shaping, typing and other manilipation
                        of the data.
        '''
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_train_cfg()
        self._data_conditioner = data_conditioner

        # Get the common configuration items.
        self._validation_split = self._cfg['Trainer']['ValidationSplit']
        self._test_split = self._cfg['Trainer']['TestSplit']
        self._output_dir_name = self._cfg['TrnDirPath']

        # Allocate parameters for the individual datasets.
        self._image_train = None
        self._image_test = None
        self._image_val = None
        self._label_train = None
        self._label_test = None
        self._label_val = None

        # Build all the filenames to use for persisting and reading the data.
        self._image_train_fn = self._filename(
            self._output_dir_name, dataset_image, phase_train) + ext
        self._image_test_fn = self._filename(
            self._output_dir_name, dataset_image, phase_test) + ext
        self._image_val_fn = self._filename(
            self._output_dir_name, dataset_image, phase_val) + ext

        self._label_train_fn = self._filename(
            self._output_dir_name, dataset_label, phase_train) + ext
        self._label_test_fn = self._filename(
            self._output_dir_name, dataset_label, phase_test) + ext
        self._label_val_fn = self._filename(
            self._output_dir_name, dataset_label, phase_val) + ext

        # Change functionality to split or load based on whether or not the
        # files can be found.
        if not os.path.exists(self._image_train_fn) or \
                not os.path.exists(self._image_test_fn) or \
                not os.path.exists(self._image_val_fn) or \
                not os.path.exists(self._label_train_fn) or \
                not os.path.exists(self._label_test_fn) or \
                not os.path.exists(self._label_val_fn):

            # One or more of the split data files is missing.  Reload the
            # full numpy arrays and resplit and condition the data.
            label_file_path = os.path.join(
                self._cfg['ManDirPath'], 'label.npy')
            image_file_path = os.path.join(
                self._cfg['ManDirPath'], 'image.npy')

            self._split_data(label_file_path, image_file_path)
        else:
            # All of the split data files are present.  Reaload them.
            # TODO: Add a command line argument to flush this data and resplit.
            self._load()

    def _split_data(self, label_file_path, image_file_path):
        '''
        Split the full numpy arrays of the images into the train, test and Validation
        datasets and persist them to disk.

        Args:
          label_file_path: The file_path for the full numpy array of labels.
          image_file_path: The file_path for the full numpy array of images.

        Returns: None
        '''

        logger.info('Splitting dataset (Train, Test, Validation)')
        # Load the full numpy arrays.  Condition the data to add X, Y and
        # Convert the images to float.
        label = np.load(label_file_path)
        label = self._data_conditioner.condition_labels(label)

        image = np.load(image_file_path)
        image = self._data_conditioner.condition_images(image)

        # Shuffle the dataset.  It was generated in a specific order and Splitting
        # won't generate a very random set of data in each split.
        shuffle_idx = np.array(range(len(image)))
        np.random.shuffle(shuffle_idx)

        image = image[shuffle_idx]
        label = label[shuffle_idx]

        # TODO: Move this to the DataConditioner.  It already has a DataFrame of
        # the data.  It will also keep the DataWrapper focused on just the
        # Load and Store of the data.
        index = pd.DataFrame(label)
        index.columns = ['Theta', 'Radius', 'Alpha', 'X', 'Y']

        # Remove any points we aren't including in the project
        # theta_range = (20, 340)
        radius_range = (15, 30)
        # mask = (index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
        #             (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1])

        mask = np.array(
            (index.Radius >= radius_range[0]) & (
                index.Radius <= radius_range[1]),
            dtype=bool)

        label = label[mask]
        image = image[mask]
        index = index[mask]

        # Separate out the areas that we aren't including in the test and validation.
        # These are points at the edges of the training area.
        theta_range = (30, 330)
        radius_trim = 0
        radius_range = (
            radius_range[0] +
            radius_trim,
            radius_range[1] -
            radius_trim)
        print('Radius range: ', radius_range)
        mask = np.array(
            (index.Theta >= theta_range[0]) & (
                index.Theta <= theta_range[1]) & (
                index.Radius >= radius_range[0]) & (
                index.Radius <= radius_range[1]),
            dtype=bool)
        not_mask = np.array([not m for m in mask], dtype=bool)

        predict_label = label[mask]
        predict_image = image[mask]
        predict_index = index[mask]

        # Save the rest for the test set.
        edge_label = label[not_mask]
        edge_image = image[not_mask]
        edge_index = index[not_mask]
        # TODO: End of stuff to move to DataConditioner

        # Split off the validataion set.
        X, self._image_val, y, self._label_val = train_test_split(
            predict_image, predict_label, test_size=self._validation_split)

        # Split off the test set.
        X, self._image_test, y, self._label_test = train_test_split(
            X, y, test_size=self._test_split)

        # Add the reminder and the edge areas together into the train dataset.
        # TODO: Verify what is going on here.  If the data is dropped out of the
        # dataset for validation it should also be dropped out of the train?
        # We may decide not to predict on it later, but we need to Verify
        # the current practice.
        self._image_train = np.concatenate((X, edge_image), axis=0)
        self._label_train = np.concatenate((y, edge_label), axis=0)

        # print('Image, Label, Index: ')
        # print('All:', image.shape, label.shape, index.shape)
        # print('Predict:', predict_image.shape, predict_label.shape, predict_index.shape)
        # print('Edge:', edge_image.shape, edge_label.shape, edge_index.shape)
        # print('Validation: ', self._validation_split, self._label_val.shape, self._image_val.shape)
        # print('Remainder: ', X.shape, y.shape)
        # print('Test: ', self._test_split, self._label_test.shape, self._image_test.shape)
        # print('Remainder: ', X.shape, y.shape)
        # print('Train: ', self._label_train.shape, self._image_train.shape)

        np.save(self._image_train_fn, self._image_train, allow_pickle=False)
        np.save(self._image_test_fn, self._image_test, allow_pickle=False)
        np.save(self._image_val_fn, self._image_val, allow_pickle=False)

        np.save(self._label_train_fn, self._label_train, allow_pickle=False)
        np.save(self._label_test_fn, self._label_test, allow_pickle=False)
        np.save(self._label_val_fn, self._label_val, allow_pickle=False)

    # TODO: Change this to load only when one of the get methods is called.
    # If validation data is all that is required then there is no need to load
    # the much larger train and test data sets.
    def _load(self):
        '''
        Load the 6 data files.
        '''
        print('Loading existing split data (Train, Test, Validation)')
        self._image_train = np.load(self._image_train_fn)
        print('Train images: ', self._image_train.shape)

        self._image_test = np.load(self._image_test_fn)
        print('Test images: ', self._image_test.shape)

        self._image_val = np.load(self._image_val_fn)
        print('Validation images: ', self._image_val.shape)

        self._label_train = np.load(self._label_train_fn)
        print('Train labels: ', self._label_train.shape)

        self._label_test = np.load(self._label_test_fn)
        print('Test labels: ', self._label_test.shape)

        self._label_val = np.load(self._label_val_fn)
        print('Validation images: ', self._label_val.shape)

    def _filename(self, dir_path, dataset, phase):
        '''
        Generate the correct file name based on if it is train, test, validation
        and image or label data.

        Args:
          dir_path: The directory path for the data file.
          dataset: The type of the data set (train, test, validation)
          phase: The phase of data set (image, label)

        Returns: Absolute path to where the dataset file.

        '''
        return os.path.join(dir_path, '_'.join((dataset, phase)))

    def get_train(self):
        '''
        Get the train label and image datasets.

        Returns: numpy arrays for the image and label data.
        '''
        return self._data_conditioner.reshape_images(
            self._image_train), self._label_train

    def get_test(self):
        '''
        Get the test label and image datasets.

        Returns: numpy arrays for the image and label data.
        '''
        return self._data_conditioner.reshape_images(
            self._image_test), self._label_test

    def get_validation(self):
        '''
        Get the validation label and image datasets.

        Returns: numpy arrays for the image and label data.
        '''
        return self._data_conditioner.reshape_images(
            self._image_val), self._label_val
