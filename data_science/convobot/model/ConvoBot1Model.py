import logging

import os
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential

from convobot.model.ModelMgr import Model

logger = logging.getLogger(__name__)


class ConvoBot1Model(Model):
    """
    Build the keras model.
    """

    def __init__(self, name, cfg):
        """
        Construct the model.
        :param name: Name of the model
        :param cfg: Configuration for the model
        """

        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)
        self._model_file_name = os.path.join(self.dst_dir_path, self.parameters['model-file-name'])

    def _build_model(self) -> Sequential:
        """
        Build the model

        :return: Model
        """

        # Declare the model
        model = Sequential()

        num_filters1 = 16
        kernel_size1 = (8, 8)
        model.add(
            Conv2D(
                num_filters1,
                kernel_size1,
                padding='valid',
                input_shape=(
                    self.parameters['image']['size'][0],
                    self.parameters['image']['size'][1],
                    self.parameters['image']['channels']),
                data_format="channels_last"))
        model.add(BatchNormalization())
        model.add(Activation('relu'))

        num_filters2 = 32
        kernel_size2 = (2, 2)
        model.add(Conv2D(num_filters2, kernel_size2,
                         padding='valid'))

        model.add(BatchNormalization())
        model.add(Activation('relu'))

        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Activation('relu'))

        model.add(Dense(256))
        model.add(Dropout(0.25))
        model.add(Activation('relu'))

        model.add(Dense(3))
        model.add(Activation('relu'))

        return model
