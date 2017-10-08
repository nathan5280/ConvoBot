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
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        super(ConvoBot1Model, self).__init__(cfg_mgr)

        self._img_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']
        self._model_path = os.path.join(self._cfg['TrnDirPath'], 'model.h5')

    def get_model(self):
        # Change resume functionality to just be dependent on if the file exists.
        if os.path.exists(self._model_path):
            logger.info('Loading model: %s', self._model_path)
            self._model = load_model(self._model_path)
        else:
            logger.info('Building model: %s', self._model_path)

            # Declare the model
            self._model = Sequential()

            num_filters1 = 16
            kernel_size1 = (8,8)
            self._model.add(Conv2D(num_filters1, kernel_size1,
                            padding='valid',
                            input_shape=(self._img_size[0], self._img_size[1], self._channels),
                            data_format="channels_last"))
            self._model.add(BatchNormalization())
            self._model.add(Activation('relu'))

            num_filters2 = 32
            kernel_size2 = (2,2)
            self._model.add(Conv2D(num_filters2, kernel_size2,
                                 padding='valid'))

            self._model.add(BatchNormalization())
            self._model.add(Activation('relu'))

            self._model.add(MaxPooling2D(pool_size=(2,2)))
            self._model.add(Dropout(0.25))
            self._model.add(Flatten())
            self._model.add(Activation('relu'))

            self._model.add(Dense(256))
            self._model.add(Dropout(0.25))
            self._model.add(Activation('relu'))

            self._model.add(Dense(3))
            self._model.add(Activation('relu'))

        return self._model
