import logging
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.models import load_model
from convobot.train.ModelBuilder import ModelBuilder

logger = logging.getLogger(__name__)

class ConvoBot1Model(ModelBuilder):
    '''
    Build the keras model.
    '''
    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: Global configuration manager.
        '''
        logger.debug('Initializing')
        super(ConvoBot1Model, self).__init__(cfg_mgr)

        # TODO: Move all this to the base class.
        # Get the common configuration items to keep the body of the code cleaner.
        self._img_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']
        self._model_path = os.path.join(self._cfg['TrnDirPath'], 'model.h5')

    def get_model(self):
        '''
        Load or build the model.  This is the core of the CNN knowledge and learning.

        Args:

        Returns:  Keras model.
        '''
        # Change resume functionality to just be dependent on if the file
        # exists.
        if os.path.exists(self._model_path):
            # TODO: Add a command line argument to clean up the model file
            # and automatically restart the training.  For now, just delete
            # the model.h5 file to force the training to restart.
            logger.info('Loading model: %s', self._model_path)
            self._model = load_model(self._model_path)
        else:
            # Build the model from scratch.
            logger.info('Building model: %s', self._model_path)

            # Declare the model
            self._model = Sequential()

            num_filters1 = 16
            kernel_size1 = (8, 8)
            self._model.add(
                Conv2D(
                    num_filters1,
                    kernel_size1,
                    padding='valid',
                    input_shape=(
                        self._img_size[0],
                        self._img_size[1],
                        self._channels),
                    data_format="channels_last"))
            self._model.add(BatchNormalization())
            self._model.add(Activation('relu'))

            num_filters2 = 32
            kernel_size2 = (2, 2)
            self._model.add(Conv2D(num_filters2, kernel_size2,
                                   padding='valid'))

            self._model.add(BatchNormalization())
            self._model.add(Activation('relu'))

            self._model.add(MaxPooling2D(pool_size=(2, 2)))
            self._model.add(Dropout(0.25))
            self._model.add(Flatten())
            self._model.add(Activation('relu'))

            self._model.add(Dense(256))
            self._model.add(Dropout(0.25))
            self._model.add(Activation('relu'))

            self._model.add(Dense(3))
            self._model.add(Activation('relu'))

        return self._model
