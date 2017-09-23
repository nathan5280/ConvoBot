import pandas as pd
import numpy as np
import os, pickle
from sklearn.model_selection import train_test_split

class DataWrapper(object):
    def __init__(self, label_file_path, image_file_path, validation_split=0.25, test_split=0.10):
        # Load the data from the pickle
        with open(image_file_path, 'rb') as f:
            image = pickle.load(f)

        # Load the data from the pickle
        with open(label_file_path, 'rb') as f:
            label = pickle.load(f)

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
        theta_range = (30, 330)
        radius_range = (16, 29)
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
        X, self._X_val, y, self._y_val = train_test_split(predict_image, predict_label,
                                                            test_size=validation_split)

        # Split off the test set.
        X, self._X_test, y, self._y_test = train_test_split(X, y,
                                                            test_size=test_split)

        # Add the reminder and the edge areas together into the train dataset.
        self._X_train = np.concatenate((X, edge_image), axis=0)
        self._y_train = np.concatenate((y, edge_label), axis=0)

        # print('Image, Label, Index: ')
        # print('All:', image.shape, label.shape, index.shape)
        # print('Predict:', predict_image.shape, predict_label.shape, predict_index.shape)
        # print('Edge:', edge_image.shape, edge_label.shape, edge_index.shape)
        # print('Validation: ', validation_split, self._X_val.shape, self._y_val.shape)
        # print('Remainder: ', X.shape, y.shape)
        # print('Test: ', test_split, self._X_test.shape, self._y_test.shape)
        # print('Remainder: ', X.shape, y.shape)
        # print('Train: ', self._y_train.shape, self._X_train.shape)

    def get_train(self):
        return self._X_train, self._y_train

    def get_test(self):
        return self._X_test, self._y_test

    def get_validation(self):
        return self._X_val, self._y_val

if __name__ == '__main__':
    root_path = '../../../dataf'
    label_file_path = os.path.join(root_path, 'gs_28x28_lable.pkl')
    image_file_path = os.path.join(root_path, 'gs_28x28_image.pkl')

    dw = DataWrapper(label_file_path, image_file_path, validation_split=0.25, test_split=0.10)
