# https://elitedatascience.com/keras-tutorial-deep-learning-in-python

import pandas as pd
import numpy as np
import os

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

class Predictor(object):
    def __init__(self, data_root, cfg_root, model_name, cfg_name):
        self._data_root = data_root
        self._cfg_root = cfg_root
        self._model_name = model_name
        self._cfg_name = cfg_name

    def process(self):
        model_env = Environment(self._cfg_root, self._data_root)
        cfg = model_env.get_model_cfg(self._model_name, self._cfg_name)

        src_label_filename, src_image_filename, data_path = \
            model_env.get_model_data_path()

        img_color_layers = 1
        if cfg['color']:
            img_color_layers = 3

        data_conditioner = DataConditioner(cfg['image_size'], img_color_layers)
        data_wrapper = DataWrapper(src_label_filename, src_image_filename, data_path, data_conditioner, cfg)

        X_val, y_val = data_wrapper.get_validation()
        y_val = data_conditioner.get_theta_radius_alpha_labels(y_val)

        model_path = model_env.get_model_path()
        model_class = cfg['model_class']
        model_builder = model_builders[model_class](model_path, cfg)
        model = model_builder.get_model()

        num_predictions = min(10, len(X_val))

        # Set aside space to show deltas predictions from epoch to epoch
        last_pred = [[0 for x in range(3)] for y in range(num_predictions)]

        score = model.evaluate(X_val, y_val, verbose=0)
        print('Test score:', score[0])
        print('Test mean absolute error:', score[1]) # this is the one we care about

        pred = model.predict(X_val, batch_size=1)

        results_filename = model_env.get_result_path()

        val_df = pd.DataFrame(y_val)
        pred_df = pd.DataFrame(pred)
        results_df = pd.concat((val_df, pred_df), axis=1)
        results_df.columns = ['vTheta', 'vRadius', 'vAlpha', 'pTheta', 'pRadius', 'pAlpha']

        print('Saving prediction results: ', results_filename)
        results_df.to_csv(results_filename, ',', index=False)
