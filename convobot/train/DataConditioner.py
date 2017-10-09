import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataConditioner(object):
    '''
    Manipulate the label matrix to add X, Y information.
    Manipulate the image data to convert from  uint8 to float and normalize
    between 0 and 1.
    '''

    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: Global configuraiton manager.
        '''
        logger.debug("Initializing")
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_train_cfg()

        # Pull out the commonly used configuration items.
        self._img_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']

    def _get_dataframe(self, array):
        '''
        Convert the numpy label array to a dataframe and add the correct
        column names based on whether or not it has X, Y information already in it.

        Args:
          array: The label array.

        Returns:  DataFrame with column labels.

        '''
        if array.shape[1] == 3:
            column_names = ['Theta', 'Radius', 'Alpha']
        else:
            column_names = ['Theta', 'Radius', 'Alpha', 'X', 'Y']
        return pd.DataFrame(array, columns=column_names)

    # TODO: Convert the radian and degree conversions to math model methods.
    def condition_labels(self, labels):
        '''
        Add the X and Y coordinates to the labels.

        Args:
          labels: The label dataframe

        Returns: DataFrame with the X, Y columns added.

        '''
        print('Condition labels')
        df = self._get_dataframe(labels)
        df['X'] = df.Radius * np.cos(df.Theta / 180 * np.pi)
        df['Y'] = df.Radius * np.sin(df.Theta / 180 * np.pi)
        self._column_names = df.columns
        return df.values

    def condition_images(self, images):
        '''
        Convert the uint8 image data to floats between 0 and 1.

        Args:
          images:  The numpy image array.

        Returns: Numpy image array of floats between 0 and 1.

        '''
        print('Condition images')
        images = images.astype('float32') / 255
        return images

    def reshape_images(self, images):
        '''
        Reshape the image array to make sure they are N * N * 3 for RGB.

        Args:
          images:  Numpy image array.

        Returns:  Numpy image array of the correct shape for Keras.

        '''
        images = images.reshape(images.shape[0], self._img_size[0],
                                self._img_size[1], self._channels)
        return images

    # TODO: Check to see if we can delete this method.
    def get_theta_radius_labels(self, labels):
        '''
        Get just the Theta and Radius columns from the label array.

        Args:
          labels:  Label DataFrame.

        Returns: DataFrame of just Theta and Radius.

        '''
        df = self._get_dataframe(labels)
        return df[['Theta', 'Radius']].values


    def get_theta_radius_alpha_labels(self, labels):
        '''
        Get just the T, R, A columns from the label array.

        Args:
          labels: Label array.

        Returns:  T, R, A array.

        '''
        df = self._get_dataframe(labels)
        return df[['Theta', 'Radius', 'Alpha']].values

    def get_x_y_labels(self, labels):
        '''
        Get just the X and Y columns from the label array.

        Args:
          labels:  Label array.

        Returns:  X, Y array.

        '''
        df = self._get_dataframe(labels)
        return df[['X', 'Y']].values
