import logging
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from convobot.processor.manipulator.Manipulator import Manipulator

logger = logging.getLogger(__name__)


class SplitManipulator(Manipulator):
    """
    The SplitManipulator splits the full data set into Train, Test and Validation data sets based on the configuration.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the split manipulator.

        :param name: Name of the manipulator
        :param cfg: The stage configuration
        """
        logger.debug('Constructing: %s', self.__class__.__name__)

        super().__init__(name, cfg)

        # build the split file names.
        self._train_label_file_path = os.path.join(self.dst_dir_path, 'train-label.npy')
        self._train_image_file_path = os.path.join(self.dst_dir_path, 'train-image.npy')

        self._test_label_file_path = os.path.join(self.dst_dir_path, 'test-label.npy')
        self._test_image_file_path = os.path.join(self.dst_dir_path, 'test-image.npy')

        self._validation_label_file_path = os.path.join(self.dst_dir_path, 'validation-label.npy')
        self._validation_image_file_path = os.path.join(self.dst_dir_path, 'validation-image.npy')

    def reset(self):
        """
        Remove all the split files.
        :return: None
        """
        if os.path.exists(self._train_label_file_path):
            os.remove(self._train_label_file_path)

        if os.path.exists(self._train_image_file_path):
            os.remove(self._train_image_file_path)

        if os.path.exists(self._test_label_file_path):
            os.remove(self._test_label_file_path)

        if os.path.exists(self._test_image_file_path):
            os.remove(self._test_image_file_path)

        if os.path.exists(self._validation_label_file_path):
            os.remove(self._validation_label_file_path)

        if os.path.exists(self._train_image_file_path):
            os.remove(self._train_image_file_path)

    def process(self) -> None:
        """
        Load the label and image data sets and split them per the configuration.
        :return: None
        """

        logger.info('Processing stage: %s', self._name)

        # Check to see if the split files all exist.  If they do then just skip this processor.
        if not os.path.exists(self._test_image_file_path) or \
                not os.path.exists(self._test_label_file_path) or \
                not os.path.exists(self._train_image_file_path) or \
                not os.path.exists(self._train_label_file_path) or \
                not os.path.exists(self._validation_image_file_path) or \
                not os.path.exists(self._validation_label_file_path):
            # Something is missing.  Resplit the data files.
            self._split()

    def _split(self) -> None:
        # Load the data sets.
        in_label_file_name = os.path.join(self.src_dir_path, self.parameters['in-label-file-prefix'] + 'label.npy')
        full_label_arr = np.load(in_label_file_name)

        in_image_file_name = os.path.join(self.src_dir_path, self.parameters['in-image-file-prefix'] + 'image.npy')
        full_image_arr = np.load(in_image_file_name)

        # Shuffle the dataset.  It was generated in a specific order and Splitting
        # won't generate a very random set of data in each split.
        shuffle_idx = np.array(range(full_label_arr.shape[0]))
        np.random.shuffle(shuffle_idx)

        full_label_arr = full_label_arr[shuffle_idx]
        full_image_arr = full_image_arr[shuffle_idx]

        # Reshape the image file into a 2-D array
        shape = full_image_arr.shape
        full_image_arr = full_image_arr.reshape(shape[0], shape[1] * shape[2] * shape[3])

        # Convert to dataframe
        full_label_df = pd.DataFrame(full_label_arr, columns=self.parameters['label-column-names'])
        full_image_df = pd.DataFrame(full_image_arr)

        # Filter the full data set if there are portions that should be excluded from the training.
        exclusion_mask = np.ones((full_label_df.shape[0]), dtype=bool)
        full_filter_cfg = self.parameters['filters']['full']
        if 'theta' in full_filter_cfg:
            min_value = full_filter_cfg['theta']['min']
            max_value = full_filter_cfg['theta']['max']

            # Create the exclusion_mask
            exclusion_mask = exclusion_mask & np.array(
                (full_label_df.Theta >= min_value) & (full_label_df.Theta <= max_value), dtype=bool)

        if 'radius' in full_filter_cfg:
            min_value = full_filter_cfg['radius']['min']
            max_value = full_filter_cfg['radius']['max']

            # Create the exclusion_mask
            exclusion_mask = exclusion_mask & np.array(
                (full_label_df.Radius >= min_value) & (full_label_df.Radius <= max_value), dtype=bool)

        if 'alpha' in full_filter_cfg:
            min_value = full_filter_cfg['alpha']['min']
            max_value = full_filter_cfg['alpha']['max']

            # Create the exclusion_mask
            exclusion_mask = exclusion_mask & np.array(
                (full_label_df.Alpha >= min_value) & (full_label_df.Alpha <= max_value), dtype=bool)

        working_label_df = full_label_df[exclusion_mask]
        working_image_df = full_image_df[exclusion_mask]

        logger.debug('Full data set: %s', full_label_df.shape)
        logger.debug('Working data set: %s', working_label_df.shape)

        # Separate out any data that should be excluded from test and validation.
        # ie. any data that won't be used for predictions.  In this case it is the
        # data around the edges of the regression model.
        exclusion_mask = np.ones((working_label_df.shape[0]), dtype=bool)
        predict_filter_cfg = self.parameters['filters']['predict']
        if 'theta' in predict_filter_cfg:
            amount = predict_filter_cfg['theta']['amount']
            min_feature_value = working_label_df.Theta.min()
            max_feature_value = working_label_df.Theta.max()

            # Create the exclusion_mask
            exclusion_mask = exclusion_mask & np.array(
                (working_label_df.Theta >= min_feature_value + amount)
                & (working_label_df.Theta <= max_feature_value - amount), dtype=bool)

        if 'radius' in predict_filter_cfg:
            amount = predict_filter_cfg['radius']['amount']
            min_feature_value = working_label_df.Radius.min()
            max_feature_value = working_label_df.Radius.max()

            # Create the exclusion_mask
            exclusion_mask = exclusion_mask & np.array(
                (working_label_df.Radius >= min_feature_value + amount)
                & (working_label_df.Radius <= max_feature_value - amount), dtype=bool)

        if 'alpha' in predict_filter_cfg:
            amount = predict_filter_cfg['alpha']['amount']
            min_feature_value = working_label_df.Theta.min()
            max_feature_value = working_label_df.Theta.max()

            # Create the exclusion_mask
            exclusion_mask = exclusion_mask & np.array(
                (working_label_df.Alpha >= min_feature_value + amount)
                & (working_label_df.Alpha <= max_feature_value - amount), dtype=bool)

        predict_label_df = working_label_df[exclusion_mask]
        train_label_df = working_label_df[~exclusion_mask]
        predict_image_df = working_image_df[exclusion_mask]
        train_image_df = working_image_df[~exclusion_mask]

        # Split the data into train, test, validate
        # Use the max-predict-ratio to insure that there is enough data left in the predict
        # data set after the test and validation pieces have been taken out to have enough
        # training data in this space.
        # full
        #   working - Filter out areas we don't want to include in training
        #       train - Areas we want to train in, but not predict.
        #       predict - Areas where we want to predict
        #           Test - test data set selected from predict
        #           Validate - validate data set selected from predict
        #       Train - train data set (train + predict-(Test + Validate))
        #
        # max-predict-ratio = Test/(predict-Validate) or Validate/(predict-Test) If either of these is too large
        # it means that for the prediction area there is a high ratio of Test or Validate data relative
        # to what we are training on.

        num_predict = predict_label_df.shape[0]
        num_test = working_label_df.shape[0] * self.parameters['splits']['test']
        num_validate = working_label_df.shape[0] * self.parameters['splits']['validate']

        max_predict_ratio = max(num_test / (num_predict - num_validate),
                                num_validate / (num_predict - num_test))

        max_train_ratio = max(num_test / (working_label_df.shape[0] - num_validate),
                              num_validate / (working_label_df.shape[0] - num_test))

        if max_predict_ratio > self.parameters['splits']['max-predict-ratio']:
            logger.error('Unable to split the data.  max-predict-ratio %s', max_predict_ratio)
            exit(1)

        if max_train_ratio > self.parameters['splits']['max-train-ratio']:
            logger.error('Unable to split the data.  max-train-ratio %s', max_train_ratio)
            exit(1)

        # Split off the validation data set.
        predict_image_remainder_arr, validation_image_arr, predict_label_remainder_arr, validation_label_arr = \
            train_test_split(predict_image_df.values,
                             predict_label_df[self.parameters['splits']['features']].values,
                             test_size=int(num_validate))

        # Split off the test data set.
        predict_image_remainder_arr, test_image_arr, predict_label_remainder_arr, test_label_arr = \
            train_test_split(predict_image_remainder_arr, predict_label_remainder_arr, test_size=int(num_test))

        # Merge up the remainder or the prediction data set with the area that was excluded from the prediction area.
        train_label_arr = np.vstack((train_label_df[self.parameters['splits']['features']].values,
                                     predict_label_remainder_arr))
        train_image_arr = np.vstack((train_image_df.values, predict_image_remainder_arr))

        # Reshape the image arrays.
        image_shape = self.parameters['image']['size']
        image_channels = self.parameters['image']['channels']

        train_image_arr = train_image_arr.reshape(
            train_image_arr.shape[0], image_shape[0], image_shape[1], image_channels)

        test_image_arr = test_image_arr.reshape(
            test_image_arr.shape[0], image_shape[0], image_shape[1], image_channels)

        validation_image_arr = validation_image_arr.reshape(
            validation_image_arr.shape[0], image_shape[0], image_shape[1], image_channels)

        logger.debug('Writing train label split: %s', train_label_arr.shape)
        logger.debug('Writing train image split: %s', train_image_arr.shape)

        logger.debug('Writing test label split: %s', test_label_arr.shape)
        logger.debug('Writing test image split: %s', test_image_arr.shape)

        logger.debug('Writing validation label split: %s', validation_label_arr.shape)
        logger.debug('Writing validation image split: %s', validation_image_arr.shape)

        # Write the files.
        np.save(self._train_label_file_path, train_label_arr, allow_pickle=False)
        np.save(self._train_image_file_path, train_image_arr, allow_pickle=False)

        np.save(self._test_label_file_path, test_label_arr, allow_pickle=False)
        np.save(self._test_image_file_path, test_image_arr, allow_pickle=False)

        np.save(self._validation_label_file_path, validation_label_arr, allow_pickle=False)
        np.save(self._validation_image_file_path, validation_image_arr, allow_pickle=False)
