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
    def __init__(self, cfg_mgr, model_builder):
        self._cfg_mgr = cfg_mgr
        self._model_builder = model_builder
        self._cfg = cfg_mgr.get_cfg()['Model']

    def process(self):
        data_conditioner = DataConditioner(self._cfg_mgr)
        data_wrapper = DataWrapper(self._cfg_mgr, data_conditioner)

        X_val, y_val = data_wrapper.get_validation()
        y_val = data_conditioner.get_theta_radius_alpha_labels(y_val)

        model = self._model_builder.get_model()

        score = model.evaluate(X_val, y_val, verbose=0)
        print('Test score:', score[0])
        print('Test mean absolute error:', score[1]) # this is the one we care about

        pred = model.predict(X_val, batch_size=1)

        results_filename = self._cfg_mgr.get_absolute_path(self._cfg['Data']['Results'])

        val_df = pd.DataFrame(y_val)
        pred_df = pd.DataFrame(pred)
        results_df = pd.concat((val_df, pred_df), axis=1)
        results_df.columns = ['vTheta', 'vRadius', 'vAlpha', 'pTheta', 'pRadius', 'pAlpha']

        print('Saving prediction results: ', results_filename)
        results_df.to_csv(results_filename, ',', index=False)
