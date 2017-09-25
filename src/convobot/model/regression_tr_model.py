# https://elitedatascience.com/keras-tutorial-deep-learning-in-python

import pandas as pd
import numpy as np
# np.random.seed(123)  # for reproducibility

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from keras.models import load_model
from keras.callbacks import TensorBoard

from sklearn.model_selection import train_test_split
from DataWrapper import DataWrapper

import os
# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

resume = True
train = True
model_name = 'model.h5'

root_path = '../../../dataf'
root_name = 'gs_28x28'

data = DataWrapper(root_path, root_name, resplit=False,
    validation_split=0.25, test_split=0.10)

X_train, y_train = data.get_train()
X_test, y_test = data.get_test()
X_val, y_val = data.get_validation()

# Pull out just the theta and radius.
# This will be the target values for the regression.
y_train = y_train[:,:2]
y_test = y_test[:,:2]

# from matplotlib import pyplot as plt
# plt.imshow(X_train[0])
# plt.show()

# Align with the shape that keras expects for the 2D Convolutional input layer
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
X_val = X_val.reshape(X_val.shape[0], 28, 28, 1)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_val = X_val.astype('float32')
X_train /= 255
X_test /= 255
X_val /= 255

if not resume:
    # Declare the model
    model = Sequential()

    num_filters1 = 32
    kernel_size1 = (3,3)
    model.add(Conv2D(num_filters1, kernel_size1,
                         padding='valid',
                         activation='relu',
                         input_shape=(28,28,1)))

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
    model.add(Dense(2, activation='relu'))
else:
    print('Loading model: ', model_name)
    model = load_model(model_name)

if train:
    last_pred = [[0 for x in range(2)] for y in range(10)]
    num_train_sessions = 10
    epochs = 1
    batch_size = 100
    lr = 0.0001
    print('Learning rate: ', lr)

    tbCallBack = TensorBoard(log_dir='./Graph',
                                histogram_freq=5,
                                write_graph=True,
                                write_images=True)

    optimizer = Adam(lr=lr, beta_1=0.9,
                        beta_2=0.999, epsilon=1e-08, decay=0.0)
    model.compile(loss='mse',
                  optimizer=optimizer,
                  metrics=['mae'])

    for i in range(num_train_sessions):
        print('Training iteration: {}/{}/{} '.format(i+1, num_train_sessions,
                                                num_train_sessions * epochs))
        model.fit(X_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    callbacks=[tbCallBack])

        model.save(model_name)

        score = model.evaluate(X_test, y_test, verbose=0)
        print('Test score:', score[0])
        print('Test mean absolute error:', score[1]) # this is the one we care about

        num_predictions = 10
        pred = model.predict(X_val[:num_predictions], batch_size=1)

        print('   Target | Prediction | Error | Delta')
        print('    Theta | Radius')
        for i in range(num_predictions):
            print('{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'. \
                format(y_val[i][0], pred[i][0], y_val[i][0] - pred[i][0], pred[i][0]-last_pred[i][0], \
                        y_val[i][1], pred[i][1], y_val[i][1] - pred[i][1], pred[i][1]-last_pred[i][1]))

            last_pred[i][0] = pred[i][0]
            last_pred[i][1] = pred[i][1]