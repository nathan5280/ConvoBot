import os
import numpy as np


class SplitDataMgr(object):
    """
    Manage the load and save of the split data arrays
    """

    def __init__(self, data_dir_path: str) -> None:
        # build the split file names.
        self._train_label_file_path = os.path.join(data_dir_path, 'train-label.npy')
        self._train_image_file_path = os.path.join(data_dir_path, 'train-image.npy')

        self._test_label_file_path = os.path.join(data_dir_path, 'test-label.npy')
        self._test_image_file_path = os.path.join(data_dir_path, 'test-image.npy')

        self._validation_label_file_path = os.path.join(data_dir_path, 'validation-label.npy')
        self._validation_image_file_path = os.path.join(data_dir_path, 'validation-image.npy')

        self._train_label_arr = None
        self._train_image_arr = None

        self._test_label_arr = None
        self._test_image_arr = None

        self._validation_label_arr = None
        self._validation_image_arr = None

    @property
    def train_label(self):
        if self._train_label_arr is None:
            self._train_label_arr = np.load(self._train_label_file_path)
        return self._train_label_arr

    @train_label.setter
    def train_label(self, arr: np.array):
        np.save(self._train_label_file_path, arr, allow_pickle=False)
        self._train_label_arr = arr

    @property
    def train_image(self):
        if self._train_image_arr is None:
            self._train_image_arr = np.load(self._train_image_file_path)
        return self._train_image_arr

    @train_image.setter
    def train_image(self, arr: np.array):
        np.save(self._train_image_file_path, arr, allow_pickle=False)
        self._train_image_arr = arr

    @property
    def test_label(self):
        if self._test_label_arr is None:
            self._test_label_arr = np.load(self._test_label_file_path)
        return self._test_label_arr

    @test_label.setter
    def test_label(self, arr: np.array):
        np.save(self._test_label_file_path, arr, allow_pickle=False)
        self._test_label_arr = arr

    @property
    def test_image(self):
        if self._test_image_arr is None:
            self._test_image_arr = np.load(self._test_image_file_path)
        return self._test_image_arr

    @test_image.setter
    def test_image(self, arr: np.array):
        np.save(self._test_image_file_path, arr, allow_pickle=False)
        self._test_image_arr = arr

    @property
    def validation_label(self):
        if self._validation_label_arr is None:
            self._validation_label_arr = np.load(self._validation_label_file_path)
        return self._validation_label_arr

    @validation_label.setter
    def validation_label(self, arr: np.array):
        np.save(self._validation_label_file_path, arr, allow_pickle=False)
        self._validation_label_arr = arr

    @property
    def validation_image(self):
        if self._validation_image_arr is None:
            self._validation_image_arr = np.load(self._validation_image_file_path)
        return self._validation_image_arr

    @validation_image.setter
    def validation_image(self, arr: np.array):
        np.save(self._validation_image_file_path, arr, allow_pickle=False)
        self._validation_image_arr = arr

    def reset(self) -> None:
        """
        Remove all the split files.

        :return:None
        """
        if os.path.exists(self._train_label_file_path):
            os.remove(self._train_label_file_path)
            self._train_label_arr = None

        if os.path.exists(self._train_image_file_path):
            os.remove(self._train_image_file_path)
            self._train_image_arr = None

        if os.path.exists(self._test_label_file_path):
            os.remove(self._test_label_file_path)
            self._test_label_arr = None

        if os.path.exists(self._test_image_file_path):
            os.remove(self._test_image_file_path)
            self._test_image_arr = None

        if os.path.exists(self._validation_label_file_path):
            os.remove(self._validation_label_file_path)
            self._validation_label_arr = None

        if os.path.exists(self._train_image_file_path):
            os.remove(self._train_image_file_path)
            self._validation_image_arr = None

    def all_exist(self) -> bool:
        """
        Check to see if all the split files exist.

        :return: bool
        """
        # Check to see if the split files all exist.  If they do then just skip this processor.
        return os.path.exists(self._test_image_file_path) and \
               os.path.exists(self._test_label_file_path) and \
               os.path.exists(self._train_image_file_path) and \
               os.path.exists(self._train_label_file_path) and \
               os.path.exists(self._validation_image_file_path) and \
               os.path.exists(self._validation_label_file_path)
