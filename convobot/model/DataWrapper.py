import pandas as pd
import numpy as np
import os, pickle
from sklearn.model_selection import train_test_split

phase_train = 'train'
phase_test = 'test'
phase_val = 'val'
dataset_image = 'image'
dataset_label = 'label'
pkl_ext = '.pkl'

class DataWrapper(object):
    def __init__(self, cfg_mgr, data_conditioner):
        self._cfg_mgr = cfg_mgr
        self._cfg = cfg_mgr.get_cfg()['Model']
        self._data_conditioner = data_conditioner
        self._split = self._cfg['Split']
        self._validation_split = self._cfg['ValidationSplit']
        self._test_split = self._cfg['TestSplit']

        src_label_filename = self._cfg_mgr.get_absolute_path(self._cfg['Data']['Label'])
        src_image_filename = self._cfg_mgr.get_absolute_path(self._cfg['Data']['Image'])

        self._image_train = None
        self._image_test = None
        self._image_val = None
        self._label_train = None
        self._label_test = None
        self._label_val = None

        self._output_dir_name = self._cfg['OutputDirName']

        self._image_train_fn = self._filename(self._output_dir_name, dataset_image, phase_train)
        self._image_test_fn = self._filename(self._output_dir_name, dataset_image, phase_test)
        self._image_val_fn = self._filename(self._output_dir_name, dataset_image, phase_val)

        self._label_train_fn = self._filename(self._output_dir_name, dataset_label, phase_train)
        self._label_test_fn = self._filename(self._output_dir_name, dataset_label, phase_test)
        self._label_val_fn = self._filename(self._output_dir_name, dataset_label, phase_val)

        # Check to see if we need to resplit either by explicit request or
        # any of the files is missing.
        if self._split or not cfg['resume'] or \
                not os.path.exists(self._image_train_fn) or \
                not os.path.exists(self._image_test_fn) or \
                not os.path.exists(self._image_val_fn) or \
                not os.path.exists(self._label_train_fn) or \
                not os.path.exists(self._label_test_fn) or \
                not os.path.exists(self._label_val_fn):
            self._split_data(src_label_filename, src_image_filename)
        else:
            self._load()


    def _split_data(self, label_path, image_path):
        print('Splitting')
        # Load the data from the pickle
        # Load the data from the pickle
        label = np.load(label_path)
        label = self._data_conditioner.condition_labels(label)

        image = np.load(image_path)
        image = self._data_conditioner.condition_images(image)

        # Shuffle things because they were probably generated in order.
        shuffle_idx = np.array(range(len(image)))
        np.random.shuffle(shuffle_idx)

        image = image[shuffle_idx]
        label = label[shuffle_idx]

        index = pd.DataFrame(label)
        index.columns = ['Theta', 'Radius', 'Alpha', 'X', 'Y']

        # Remove any points we aren't including in the project
        # theta_range = (20, 340)
        radius_range = (15, 30)
        # mask = (index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
        #             (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1])

        mask = np.array((index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1]), dtype=bool)

        label = label[mask]
        image = image[mask]
        index = index[mask]

        # Separate out the areas that we aren't including in the test and validation.
        # These are points at the edges of the training area.
        theta_range = (30, 330)
        radius_trim = 0
        radius_range = (radius_range[0] + radius_trim, radius_range[1] - radius_trim)
        print('Radius range: ', radius_range)
        mask = np.array((index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
                    (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1]), dtype=bool)
        not_mask = np.array([not m for m in mask], dtype=bool)

        predict_label = label[mask]
        predict_image = image[mask]
        predict_index = index[mask]

        # Save the rest for the test set.
        edge_label = label[not_mask]
        edge_image = image[not_mask]
        edge_index = index[not_mask]

        # Split off the validataion set.
        X, self._image_val, y, self._label_val = train_test_split(predict_image, predict_label,
                                                            test_size=self._validation_split)

        # Split off the test set.
        X, self._image_test, y, self._label_test = train_test_split(X, y,
                                                            test_size=self._test_split)

        # Add the reminder and the edge areas together into the train dataset.
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


    def _load(self):
        print('Loading')
        np.load(self._image_train_fn)
        np.load(self._image_test_fn)
        np.load(self._image_val_fn)

        np.load(self._label_train_fn)
        np.load(self._label_test_fn)
        np.load(self._label_val_fn)


    def _filename(self, path, dataset, phase):
        return self._cfg_mgr.get_absolute_path(os.path.join(path, '_'.join((dataset, phase))))

    def get_train(self):
        return self._data_conditioner.reshape_images(self._image_train), self._label_train

    def get_test(self):
        return self._data_conditioner.reshape_images(self._image_test), self._label_test

    def get_validation(self):
        return self._data_conditioner.reshape_images(self._image_val), self._label_val
