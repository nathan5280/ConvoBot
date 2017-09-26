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
    def __init__(self, label_filename, image_filename, data_path, cfg):
        self._split = cfg['split']
        self._validation_split = cfg['validation_split']
        self._test_split = cfg['test_split']
        self._radius_trim = cfg['radius_trim']

        self._image_train = None
        self._image_test = None
        self._image_val = None
        self._label_train = None
        self._label_test = None
        self._label_val = None

        self._image_train_fn = self._filename(data_path, dataset_image, phase_train)
        self._image_test_fn = self._filename(data_path, dataset_image, phase_test)
        self._image_val_fn = self._filename(data_path, dataset_image, phase_val)

        self._label_train_fn = self._filename(data_path, dataset_label, phase_train)
        self._label_test_fn = self._filename(data_path, dataset_label, phase_test)
        self._label_val_fn = self._filename(data_path, dataset_label, phase_val)

        # Check to see if we need to resplit either by explicit request or
        # any of the files is missing.
        if cfg['resume']:
            self._load()
            return
            
        if self._split or \
                not os.path.exists(self._image_train_fn) or \
                not os.path.exists(self._image_test_fn) or \
                not os.path.exists(self._image_val_fn) or \
                not os.path.exists(self._label_train_fn) or \
                not os.path.exists(self._label_test_fn) or \
                not os.path.exists(self._label_val_fn):
            self._split_data(label_filename, image_filename)
        else:
            self._load()


    def _split_data(self, label_path, image_path):
        print('Splitting')
        # Load the data from the pickle
        # Load the data from the pickle
        with open(label_path, 'rb') as f:
            label = pickle.load(f)

        with open(image_path, 'rb') as f:
            image = pickle.load(f)


        # Shuffle things because they were probably generated in order.
        shuffle_idx = np.array(range(len(image)))
        np.random.shuffle(shuffle_idx)

        image = image[shuffle_idx]
        label = label[shuffle_idx]

        index = pd.DataFrame(label)
        index.columns = ['Theta', 'Radius', 'Alpha']

        # Remove any points we aren't including in the project
        theta_range = (20, 340)
        radius_range = (15, 30)
        mask = (index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
                    (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1])

        label = label[mask]
        image = image[mask]
        index = index[mask]

        # Separate out the areas that we aren't including in the test and validation.
        # These are points at the edges of the training area.
        theta_range = (35, 325)
        radius_range = (radius_range[0] + self._radius_trim, radius_range[1] - self._radius_trim)
        print('Radius range: ', radius_range)
        mask = (index.Theta >= theta_range[0]) & (index.Theta <= theta_range[1]) & \
                    (index.Radius >= radius_range[0]) & (index.Radius <=radius_range[1])
        not_mask = [not m for m in mask]

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

        print('Image, Label, Index: ')
        print('All:', image.shape, label.shape, index.shape)
        print('Predict:', predict_image.shape, predict_label.shape, predict_index.shape)
        print('Edge:', edge_image.shape, edge_label.shape, edge_index.shape)
        print('Validation: ', self._validation_split, self._label_val.shape, self._image_val.shape)
        print('Remainder: ', X.shape, y.shape)
        print('Test: ', self._test_split, self._label_test.shape, self._image_test.shape)
        print('Remainder: ', X.shape, y.shape)
        print('Train: ', self._label_train.shape, self._image_train.shape)

        with open(self._image_train_fn, 'wb') as f:
            pickle.dump(self._image_train, f)

        with open(self._image_test_fn, 'wb') as f:
            pickle.dump(self._image_test, f)

        with open(self._image_val_fn, 'wb') as f:
            pickle.dump(self._image_val, f)

        with open(self._label_train_fn, 'wb') as f:
            pickle.dump(self._label_train, f)

        with open(self._label_test_fn, 'wb') as f:
            pickle.dump(self._label_test, f)

        with open(self._label_val_fn, 'wb') as f:
            pickle.dump(self._label_val, f)


    def _load(self):
        print('Loading')
        with open(self._image_train_fn, 'rb') as f:
            self._image_train = pickle.load(f)

        with open(self._image_test_fn, 'rb') as f:
            self._image_test = pickle.load(f)

        with open(self._image_val_fn, 'rb') as f:
            self._image_val = pickle.load(f)

        with open(self._label_train_fn, 'rb') as f:
            self._label_train = pickle.load(f)

        with open(self._label_test_fn, 'rb') as f:
            self._label_test = pickle.load(f)

        with open(self._label_val_fn, 'rb') as f:
            self._label_val = pickle.load(f)


    def _filename(self, path, dataset, phase):
        return os.path.join(path, '_'.join((dataset, phase)) + pkl_ext)

    def get_train(self):
        return self._image_train, self._label_train

    def get_test(self):
        return self._image_test, self._label_test

    def get_validation(self):
        return self._image_val, self._label_val
