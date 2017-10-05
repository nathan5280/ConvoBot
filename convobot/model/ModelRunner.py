import pandas as pd
import numpy as np
import os

from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import TensorBoard

from convobot.model.DataWrapper import DataWrapper
from convobot.model.DataConditioner import DataConditioner

# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# np.random.seed(123)  # for reproducibility

class ModelRunner(object):
    def __init__(self, cfg_mgr, model_builder, predictor=None):
        self._cfg_mgr = cfg_mgr
        self._model_builder = model_builder
        self._cfg = cfg_mgr.get_cfg()['Model']
        self._predictor=predictor

    def _print_stats(self, num_pred, val, pred, last_pred):
        last_pred = np.array(last_pred)

        max_row = 'Max:'
        mean_row = 'Mean:'
        for i in range(3):
            max_err = max(abs(val[:num_pred, i]-pred[:num_pred, i]))
            mean_err = np.mean(val[:num_pred, i]-pred[:num_pred, i])
            max_chg = max(abs(pred[:num_pred, i]-last_pred[:num_pred, i]))
            mean_chg = np.mean(pred[:num_pred, i]-last_pred[:num_pred, i])

            max_row += '\t\t{:5.1f}\t{:5.1f}\t'.format(max_err, max_chg)
            mean_row += '\t\t{:5.1f}\t{:5.1f}\t'.format(mean_err, mean_chg)

        print('----------------------------------------------------------------------------------------------')
        print(max_row)
        print(mean_row)


    def process(self):
        data_conditioner = DataConditioner(self._cfg_mgr)
        data_wrapper = DataWrapper(self._cfg_mgr, data_conditioner)

        X_train, y_train = data_wrapper.get_train()
        X_test, y_test = data_wrapper.get_test()
        X_val, y_val = data_wrapper.get_validation()

        y_train = data_conditioner.get_theta_radius_alpha_labels(y_train)
        y_test = data_conditioner.get_theta_radius_alpha_labels(y_test)
        y_val = data_conditioner.get_theta_radius_alpha_labels(y_val)

        model = self._model_builder.get_model()

        num_predictions = min(10, len(X_val))

        # Set aside space to show deltas predictions from epoch to epoch
        last_pred = [[0 for x in range(3)] for y in range(num_predictions)]

        # Check to see where to restart if resuming.
        start_phase = 0
        if self._cfg['Resume']:
            start_phase = self._cfg['ResumePhase']
            print('Resuming at phase: ', start_phase)

        schedule = self._cfg['Schedule']

        incremental_sessions_run = 0

        for phase in range(start_phase, len(schedule)):
            phase_cfg = schedule[phase]

            sessions = phase_cfg['Sessions']
            epochs = phase_cfg['Epochs']
            batch_size = phase_cfg['BatchSize']
            lr = phase_cfg['LearningRate']

            print('Phase {}: {}/{}'.format(phase_cfg['Name'], phase + 1, len(schedule)))
            print('Sessions: {}, Epochs: {}, Batch Size: {}, Learning Rate: {}'
                        .format(sessions, epochs, batch_size, lr))

            print('Learning rate: ', lr)

            tb_path =  self._cfg_mgr.get_absolute_path(self._cfg['TensorBoardPath'])
            tbCallBack = TensorBoard(log_dir=tb_path,
                                        histogram_freq=0,
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

                self._model_builder.save_model()

                score = model.evaluate(X_test, y_test, verbose=0)
                print('Test score:', score[0])
                print('Test mean absolute error:', score[1]) # this is the one we care about

                pred = model.predict(X_val[:num_predictions], batch_size=1)

                print('   Target | Prediction | Error | Change')
                print('Theta\t\t\t\t Radius\t\t\t\tAlpha')
                for i in range(num_predictions):
                    # Theta, Radius
                    # print('{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'. \
                    #     format(y_val[i][0], pred[i][0], y_val[i][0] - pred[i][0], pred[i][0]-last_pred[i][0], \
                    #             y_val[i][1], pred[i][1], y_val[i][1] - pred[i][1], pred[i][1]-last_pred[i][1]))
                    #

                    fmt = '{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'
                    theta = fmt.format(y_val[i][0], pred[i][0], y_val[i][0] - pred[i][0], pred[i][0]-last_pred[i][0])
                    radius = fmt.format(y_val[i][1], pred[i][1], y_val[i][1] - pred[i][1], pred[i][1]-last_pred[i][1])
                    alpha = fmt.format(y_val[i][2], pred[i][2], y_val[i][2] - pred[i][2], pred[i][2]-last_pred[i][2])
                    print('{}\t{}\t{}'.format(theta, radius, alpha))

                self._print_stats(num_predictions, y_val, pred, last_pred)

                for i in range(num_predictions):
                    last_pred[i][0] = pred[i][0]
                    last_pred[i][1] = pred[i][1]
                    last_pred[i][2] = pred[i][2]

                print('Sessions run:', incremental_sessions_run)
                if incremental_sessions_run == 0:
                    incremental_sessions_run = 5
                    if self._predictor:
                        self._predictor.process(model, X_val, y_val)

                incremental_sessions_run -= 1
