import numpy as np
import pandas as pd

class DataConditioner(object):
    def __init__(self, cfg_mgr):
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_cfg()['Model']
        self._img_size = self._cfg_mgr.get_cfg()['Environment']['ImageSize']
        self._channels = self._cfg_mgr.get_cfg()['Environment']['Channels']

    def _get_dataframe(self, array):
        if array.shape[1] == 3:
            column_names = ['Theta', 'Radius', 'Alpha']
        else:
            column_names = ['Theta', 'Radius', 'Alpha', 'X', 'Y']
        return pd.DataFrame(array, columns=column_names)

    def condition_labels(self, labels):
        print('Condition labels')
        df = self._get_dataframe(labels)
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
                                self._img_size[1], self._channels)
        return images

    def get_theta_radius_labels(self, labels):
        df = self._get_dataframe(labels)
        return df[['Theta', 'Radius']].values

    def get_theta_radius_alpha_labels(self, labels):
        df = self._get_dataframe(labels)
        return df[['Theta', 'Radius', 'Alpha']].values

    def get_x_y_labels(self, labels):
        df = self._get_dataframe(labels)
        return df[['X', 'Y']].values
