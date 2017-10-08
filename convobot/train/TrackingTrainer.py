import logging
import pandas as pd
import numpy as np
import os

from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import TensorBoard

from convobot.train.DataWrapper import DataWrapper
from convobot.train.DataConditioner import DataConditioner
from convobot.train.Trainer import Trainer
from convobot.train.ModelLoader import ModelLoader

# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

logger = logging.getLogger(__name__)

class TrackingTrainer(Trainer):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        super(TrackingTrainer, self).__init__(cfg_mgr)
        self._model_loader = ModelLoader(self._cfg_mgr)
        self._model_builder = self._model_loader.get_model_builder()
        self._model = self._model_builder.get_model()

        self._data_conditioner = DataConditioner(self._cfg_mgr)
        self._data_wrapper = DataWrapper(self._cfg_mgr, self._data_conditioner)

        self._X_train, self._y_train = self._data_wrapper.get_train()
        self._X_test, self._y_test = self._data_wrapper.get_test()
        self._X_val, self._y_val = self._data_wrapper.get_validation()

        self._y_train = self._data_conditioner.get_theta_radius_alpha_labels(self._y_train)
        self._y_test = self._data_conditioner.get_theta_radius_alpha_labels(self._y_test)
        self._y_val = self._data_conditioner.get_theta_radius_alpha_labels(self._y_val)

        self._num_predictions = min(10, len(self._X_val))

        # Set aside space to show deltas predictions from epoch to epoch
        self._last_pred = [[0 for x in range(3)] for y in range(self._num_predictions)]

        self._train_cfg = self._cfg['Trainer']
        self._sessions = self._train_cfg['Sessions']
        self._epochs = self._train_cfg['Epochs']
        self._batch_size = self._train_cfg['BatchSize']
        self._lr = self._train_cfg['LearningRate']

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
        logger.info('Session: {}, Epochs: {}, Batch Size: {}, Learning Rate: {}'.
                format(self._sessions, self._epochs, self._batch_size, self._lr))
        tb_path =  os.path.join(self._cfg['TrnDirPath'], 'graph')

        tbCallBack = TensorBoard(log_dir=tb_path,
                                    histogram_freq=0,
                                    write_graph=True,
                                    write_images=True)

        optimizer = Adam(lr=self._lr, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

        self._model.compile(loss='mse', optimizer=optimizer, metrics=['mae'])

        for session in range(self._sessions):
            logger.info('Session: {} of {}'.format(session+1, self._sessions))

            self._model.fit(self._X_train, self._y_train,
                                batch_size=self._batch_size,
                                epochs=self._epochs,
                                verbose=1,
                                callbacks=[tbCallBack])

            self._model_builder.save_model()

            score = self._model.evaluate(self._X_test, self._y_test, verbose=0)
            print('Test score:', score[0])
            print('Test mean absolute error:', score[1]) # this is the one we care about

            pred = self._model.predict(self._X_val[:self._num_predictions], batch_size=1)

            print('   Target | Prediction | Error | Change')
            print('Theta\t\t\t\t Radius\t\t\t\tAlpha')

            # Allocate the space for the theta, radius, alpha information to be
            # displayed
            results = ['']*3

            for i in range(self._num_predictions):
                fmt = '{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'
                for j in range(3):
                    results[j] = fmt.format(self._y_val[i][j], pred[i][j],
                            self._y_val[i][j] - pred[i][j], pred[i][j]-self._last_pred[i][j])
                print('{}\t{}\t{}'.format(results[0], results[1], results[2]))

            self._print_stats(self._num_predictions, self._y_val, pred, self._last_pred)

            for i in range(self._num_predictions):
                for j in range(3):
                    self._last_pred[i][j] = pred[i][j]


            # Run the model against the validation dataset and save the results
            # to generate the training error animation.
            pred = self._model.predict(self._X_val, batch_size=1)
            pred_file_path = os.path.join(self._cfg['PredDirPath'], '{0:04d}'.format(session) + '.csv')

            val_df = pd.DataFrame(self._y_val)
            pred_df = pd.DataFrame(pred)
            results_df = pd.concat((val_df, pred_df), axis=1)
            results_df.columns = ['vTheta', 'vRadius', 'vAlpha', 'pTheta', 'pRadius', 'pAlpha']

            print('Saving prediction results: ', pred_file_path)
            results_df.to_csv(pred_file_path, ',', index=False)
