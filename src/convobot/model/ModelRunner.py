# https://elitedatascience.com/keras-tutorial-deep-learning-in-python

import pandas as pd
import numpy as np
import os, sys, getopt

from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import TensorBoard

from convobot.model.DataWrapper import DataWrapper
from convobot.model.DataConditioner import DataConditioner
from convobot.model.MNISTModelBuilder import MNISTModelBuilder
from convobot.workflow.Environment import Environment

# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# np.random.seed(123)  # for reproducibility
model_builders = {'mnist': MNISTModelBuilder}

def process(data_root, cfg_root, model_name, cfg_name):
    model_env = Environment(cfg_root, data_root)
    cfg = model_env.get_model_cfg(model_name, cfg_name)

    src_label_filename, src_image_filename, data_path = \
        model_env.get_model_data_path()

    img_color_layers = 1
    if cfg['color']:
        img_color_layers = 3

    data_conditioner = DataConditioner(cfg['image_size'], img_color_layers)
    data_wrapper = DataWrapper(src_label_filename, src_image_filename, data_path, data_conditioner, cfg)

    X_train, y_train = data_wrapper.get_train()
    X_test, y_test = data_wrapper.get_test()
    X_val, y_val = data_wrapper.get_validation()

    # Pull out just the theta and radius.
    # This will be the target values for the regression.
    # y_train = y_train[:,:2]
    # y_test = y_test[:,:2]
    y_train = data_conditioner.get_theta_radius_labels(y_train)
    y_test = data_conditioner.get_theta_radius_labels(y_test)
    y_val = data_conditioner.get_theta_radius_labels(y_val)
    # y_train = data_conditioner.get_x_y_labels(y_train)
    # y_test = data_conditioner.get_x_y_labels(y_test)
    # y_val = data_conditioner.get_x_y_labels(y_val)

    model_path = model_env.get_model_path()
    model_class = cfg['model_class']
    model_builder = model_builders[model_class](model_path, cfg)
    model = model_builder.get_model()

    # Set aside space to show deltas predictions from epoch to epoch
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

            model_builder.save_model()

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
    usage = 'ModelRunner.py -d <data_root> -e <cfg_root> -m <model_name> -c <cfg_name>'
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
