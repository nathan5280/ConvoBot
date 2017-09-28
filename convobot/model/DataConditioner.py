import numpy as np
import pandas as pd

class DataConditioner(object):
    def __init__(self, img_size, color_layers):
        self._img_size = img_size
        self._img_color_layers = color_layers
        self._column_names = ['Theta', 'Radius', 'Alpha']

    def condition_labels(self, labels):
        print('Condition labels')
        df = pd.DataFrame(labels)
        df.columns = self._column_names
        df['X'] = df.Radius * np.cos(df.Theta/180 * np.pi)
        df['Y'] = df.Radius * np.sin(df.Theta/180 * np.pi)
        self._column_names = df.columns
        return df.values

    def condition_images(self, images):
        print('Condition images')
        images = images.astype('float32')/255
        return images

    def reshape_images(self, images):
        images = images.reshape(images.shape[0], self._img_size[0],
                                self._img_size[1], self._img_color_layers)
        return images

    def get_theta_radius_labels(self, labels):
        df = pd.DataFrame(labels, columns=self._column_names)
        return df[['Theta', 'Radius']].values

    def get_theta_radius_alpha_labels(self, labels):
        df = pd.DataFrame(labels, columns=self._column_names)
        return df[['Theta', 'Radius', 'Alpha']].values

    def get_x_y_labels(self, labels):
        df = pd.DataFrame(labels, columns=self._column_names)
        return df[['X', 'Y']].values
