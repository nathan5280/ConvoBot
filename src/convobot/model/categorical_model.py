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

from sklearn.model_selection import train_test_split

import os
# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

import pickle
import os

root_path = '../../../dataf'
label_file_path = os.path.join(root_path, 'gs_28x28_lable.pkl')
image_file_path = os.path.join(root_path, 'gs_28x28_image.pkl')

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

print('Image: ',image.shape)
print('Label: ', label.shape)

# Pull out just the theta for now.
theta = [int(label[i][0]) for i in range(len(label))]
label_unique = sorted(np.unique(theta))

# Need this until switch to regression.
one_hot = np.zeros([len(theta), len(label_unique)], dtype=np.uint8)
for i in range(len(theta)):
    one_hot[i][label_unique.index(theta[i])] = 1

X_train, X_test, y_train, y_test = train_test_split(image, one_hot, test_size=0.33)

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

# Convert 1-dimensional class arrays to label-dimensional class matrices
label_cnt = len(one_hot[0])
# Y_train = np_utils.to_categorical(y_train, label_cnt)
# Y_test = np_utils.to_categorical(y_test, label_cnt)
# print('Categorized shape y train: ', Y_train.shape)
# print('Categorized Labels: ', Y_train)

resume = False
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
    model.add(Dropout(0.5))
    model.add(Dense(label_cnt, activation='softmax'))

    optimizer = Adam(lr=0.0025, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
else:
    print('Loading model')
    model = load_model('cat_convobot_model.h5')

model.fit(X_train, y_train, batch_size=500, epochs=10, verbose=1)
model.save('cat_convobot_model.h5')

score = model.evaluate(X_test, y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1]) # this is the one we care about
