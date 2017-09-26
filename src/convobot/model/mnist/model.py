# https://elitedatascience.com/keras-tutorial-deep-learning-in-python

import pandas as pd
import numpy as np
import os
import sys, getopt

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from keras.models import load_model
from keras.callbacks import TensorBoard

from sklearn.model_selection import train_test_split
from convobot.model.DataWrapper import DataWrapper
from convobot.workflow.Environment import Environment

# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# np.random.seed(123)  # for reproducibility

def process(data_root, cfg_root, model_name, cfg_name):
    model_env = Environment(cfg_root, data_root)
    cfg = model_env.get_model_cfg(model_name, cfg_name)

    resume = cfg['resume']
    train = True

    model_name = model_env.get_model_name()
    print(model_name)

    src_label_filename, src_image_filename, data_path = \
        model_env.get_model_data_path()
    data = DataWrapper(src_label_filename, src_image_filename, data_path, cfg)
        # resplit=split, validation_split=0.25, test_split=0.10)

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
    img_size = cfg['image_size']
    X_train = X_train.reshape(X_train.shape[0], img_size[0], img_size[1], 1)
    X_test = X_test.reshape(X_test.shape[0], img_size[0], img_size[1], 1)
    X_val = X_val.reshape(X_val.shape[0], img_size[0], img_size[1], 1)

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
                             input_shape=(img_size[0], img_size[1],1)))

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

        # Check to see where to restart if resuming.
        start_phase = 0
        if cfg['resume']:
            start_phase = cfg['resume_phase']
            print('Resuming at phase: ', start_phase)

        schedule = cfg['schedule']

        for phase in range(start_phase, len(schedule)):
            phase_cfg = schedule[phase]

            sessions = phase_cfg['sessions']
            epochs = phase_cfg['epochs']
            batch_size = phase_cfg['batch_size']
            lr = phase_cfg['learning_rate']


            print('Phase {}: {}/{}'.format(phase_cfg['name'], phase, len(schedule)))
            print('Sessions: {}, Epochs: {}, Batch Size: {}, Learning Rate: {}'
                        .format(sessions, epochs, batch_size, lr))

            print('Learning rate: ', lr)

            tb_path = model_env.get_tensorboard_path()
            tbCallBack = TensorBoard(log_dir=tb_path,
                                        histogram_freq=5,
                                        write_graph=True,
                                        write_images=True)

            optimizer = Adam(lr=lr, beta_1=0.9,
                                beta_2=0.999, epsilon=1e-08, decay=0.0)
            model.compile(loss='mse',
                          optimizer=optimizer,
                          metrics=['mae'])

            for i in range(sessions):
                print('Training iteration: {}/{}/{} '.format(i+1, sessions, sessions * epochs))
                model.fit(X_train, y_train,
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=1,
                            callbacks=[tbCallBack])

                model.save(model_name)

                score = model.evaluate(X_test, y_test, verbose=0)
                print('Test score:', score[0])
                print('Test mean absolute error:', score[1]) # this is the one we care about

                num_predictions = min(10, len(X_val))
                pred = model.predict(X_val[:num_predictions], batch_size=1)

                print('   Target | Prediction | Error | Delta')
                print('    Theta | Radius')
                for i in range(num_predictions):
                    print('{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'. \
                        format(y_val[i][0], pred[i][0], y_val[i][0] - pred[i][0], pred[i][0]-last_pred[i][0], \
                                y_val[i][1], pred[i][1], y_val[i][1] - pred[i][1], pred[i][1]-last_pred[i][1]))

                    last_pred[i][0] = pred[i][0]
                    last_pred[i][1] = pred[i][1]


def main(argv):
    data_root = None
    cfg_name = None  # Name of the configuration to load
    cfg_root = None  # Root director for the configuration files
    model_name = None  # Directory where to run the model.
    usage = 'PrepareImages.py -d <data_root> -e <cfg_root> -m <model_name> -c <cfg_name>'
    try:
        opts, args = getopt.getopt(argv,"hd:e:m:c:",["data_root=", "cfg_root=", "model_name=", "cfg_name="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--data_root"):
            data_root = arg
        elif opt in ("-e", "--cfg_root"):
            cfg_root = arg
        elif opt in ("-m", "--model_name"):
            model_name = arg
        elif opt in ("-c", "--cfg_name"):
            cfg_name = arg

    if not data_root or not cfg_root or not model_name or not cfg_name:
        print(usage)
    else:
        process(data_root, cfg_root, model_name, cfg_name)

if __name__ == "__main__":
    main(sys.argv[1:])
