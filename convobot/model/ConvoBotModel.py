import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras.models import load_model
from convobot.model.Model import Model

class ConvoBotModel(Model):
    def __init__(self, cfg_mgr, verbose=False):
        super(ConvoBotModel, self).__init__(cfg_mgr, verbose)

        self._img_size = self._cfg_mgr.get_cfg()['Environment']['ImageSize']
        self._channels = self._cfg_mgr.get_cfg()['Environment']['Channels']
        self._resume = self._model_cfg['Resume']
        self._model_path = self._cfg_mgr.get_absolute_path(
                        os.path.join(self._output_path, self._model_cfg['ModelFilename']))

        if self._verbose:
            print('Preparing to load model: ', self._model_path)

    def get_model(self):
        if self._resume and os.path.exists(self._model_path):
            print('Loading model: ', self._model_path)
            model = load_model(self._model_path)
        else:
            print('Building model: ', self._model_path)
            # Declare the model
            model = Sequential()

            num_filters1 = 16
            kernel_size1 = (8,8)
            model.add(Conv2D(num_filters1, kernel_size1,
                            padding='valid',
                            input_shape=(self._img_size[0], self._img_size[1], self._channels),
                            data_format="channels_last"))
            model.add(BatchNormalization())
            model.add(Activation('relu'))

            num_filters2 = 32
            kernel_size2 = (2,2)
            model.add(Conv2D(num_filters2, kernel_size2,
                                 padding='valid'))

            model.add(BatchNormalization())
            model.add(Activation('relu'))

            model.add(MaxPooling2D(pool_size=(2,2)))
            model.add(Dropout(0.25))
            model.add(Flatten())
            model.add(Activation('relu'))

            model.add(Dense(256))
            model.add(Dropout(0.25))
            model.add(Activation('relu'))
            
            model.add(Dense(3))
            model.add(Activation('relu'))

        self._model = model
        return self._model

    def save_model(self):
        print('Saving model')
        self._model.save(self._model_path)
