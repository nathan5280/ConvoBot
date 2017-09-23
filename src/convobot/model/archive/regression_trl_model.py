# https://elitedatascience.com/keras-tutorial-deep-learning-in-python

import pandas as pd
import numpy as np
np.random.seed(123)  # for reproducibility

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from keras.models import load_model
from keras.callbacks import TensorBoard
from keras import backend as K

from sklearn.model_selection import train_test_split

import os
# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

import pickle
import os

resume = False
train = True
model_name = 'model_cust_loss.h5'

root_path = '../../../dataf'
label_file_path = os.path.join(root_path, 'gs_28x28_lable.pkl')
image_file_path = os.path.join(root_path, 'gs_28x28_image.pkl')

def theta_loss(y_true, y_pred):
    return K.mean(K.square(K.abs(K.abs(y_pred)-360) - y_true), axis=-1)

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

# Subset the data
# Minimally remove points between 330 and 30 degrees.  These cause problems
# when the regressor predicts -5 for 355 and the loss function doesn't
# know what to do with that.   Need custom loss function to address this.
# print('Pre-subset:')
# print('Image: ',image.shape)
# print('Label: ', label.shape)

label_df = pd.DataFrame(label)
label_df.columns = ['Theta', 'Radius', 'Alpha']

theta_range = (0, 360)
radius_range = (19, 21)
mask = (label_df.Theta >= theta_range[0]) & (label_df.Theta <= theta_range[1]) & \
            (label_df.Radius >= radius_range[0]) & (label_df.Radius <=radius_range[1])

label = label[mask]
image = image[mask]

print('Post-subset:')
print('Image: ',image.shape)
print('Label: ', label.shape)

# Pull out just the theta for now.
# This will be the target values for the regression.
theta_radius = label[:,:2]
# print(theta_radius.shape)
# print(theta_radius[:10])

X_train, X_test, y_train, y_test = train_test_split(image, theta_radius, test_size=0.33)

# Convert the target arrays to np.array for keras interface
y_train = np.array(y_train)
y_test = np.array(y_test)

# print('Original shape x train: ', X_train.shape)

# from matplotlib import pyplot as plt
# plt.imshow(X_train[0])
# plt.show()

X_train = X_train.reshape(X_train.shape[0], 28, 28, 1)
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1)
# print('Reshaped x train: ', X_train.shape)

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

# print('Original shape y train: ', y_train.shape)
# print('Original Labels: ', y_train[:10])

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
    # model = load_model(model_name)
    model = load_model('.',
        custom_objects={'theta_loss': theta_loss})

if train:
    last_pred = [[0 for x in range(2)] for y in range(10)]
    num_train_sessions = 10
    epochs = 2
    batch_size = 100
    lr = 0.01
    print('Learning rate: ', lr)

    tbCallBack = TensorBoard(log_dir='./GraphCustomLoss',
                                histogram_freq=5,
                                write_graph=True,
                                write_images=True)

    optimizer = Adam(lr=lr, beta_1=0.9,
                        beta_2=0.999, epsilon=1e-08, decay=0.0)
    model.compile(loss=theta_loss,
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
        pred = model.predict(X_test[:num_predictions], batch_size=1)

        print('   Target | Prediction | Delta')
        print('    Theta | Radius')
        for i in range(num_predictions):
            print('{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'. \
                format(y_test[i][0], pred[i][0], last_pred[i][0]-pred[i][0], \
                        y_test[i][1], pred[i][1], last_pred[i][1]-pred[i][1]))

            last_pred[i][0] = pred[i][0]
            last_pred[i][1] = pred[i][1]
