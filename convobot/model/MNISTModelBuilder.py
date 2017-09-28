# https://elitedatascience.com/keras-tutorial-deep-learning-in-python

import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.models import load_model

class MNISTModelBuilder(object):
    def __init__(self, model_path, cfg):
        self._model_path = model_path
        self._resume = cfg['resume']
        self._img_size = cfg['image_size']
        self._img_color = cfg['color']
        self._img_color_layers = 1
        if self._img_color:
            self._img_color_layers = 3

    def get_model(self):
        print(self._resume, os.path.exists(self._model_path))
        if self._resume and os.path.exists(self._model_path):
            print('Loading model: ', self._model_path)
            model = load_model(self._model_path)
        else:
            print('Building model: ', self._model_path)
            # Declare the model
            model = Sequential()

            num_filters1 = 32
            kernel_size1 = (3,3)
            model.add(Conv2D(num_filters1, kernel_size1,
                                 padding='valid',
                                 activation='relu',
                                 input_shape=(self._img_size[0], self._img_size[1],
                                                self._img_color_layers)))

            num_filters2 = 32
            kernel_size2 = (1,1)
            model.add(Conv2D(num_filters2, kernel_size2,
                                 padding='valid',
                                 activation='relu'))

            model.add(MaxPooling2D(pool_size=(2,2)))
            model.add(Dropout(0.25))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dropout(0.25))
            model.add(Dense(3, activation='relu'))

        self._model = model
        return self._model

    def save_model(self):
        print('Saving model')
        self._model.save(self._model_path)
