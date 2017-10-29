import logging
import os
from keras.callbacks import TensorBoard
from keras.optimizers import Adam
from convobot.processor.trainer.Trainer import Trainer

# Turn off TF warnings to recommend that we should compile for SSE4.2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

logger = logging.getLogger(__name__)


class TrackingTrainer(Trainer):
    """
    Core class for training the model.  The TrackingTrainer also logs files for
    review by TensorBoard.  The TrackingTrainer uses the validation data
    set to make and save predictions for review and animation after training
    is complete.
    """

    def __init__(self, name, cfg):
        """
        Construct the Trainer

        :param name: Name of the processor stage.
        :param cfg: Processor configuration
        """

        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)

    # def _print_stats(self, num_pred, val, pred, last_pred):
    #     '''
    #     Calculate some basic stats to be shown with the predictions after
    #     each epoch.  These don't influence the training or error calculations
    #     of the models.  They are only to help understand what is happening with
    #     the pregress of the model training.
    #
    #     Args:
    #       num_pred: How many predictions were made.
    #       val: Validataion dataset locations (labels).
    #       pred: Predicted dataset locations (labels).
    #       last_pred: The previous set of predictions to calculate deltas.
    #
    #     Returns: None
    #
    #     '''
    #     last_pred = np.array(last_pred)
    #
    #     max_row = 'Max:'
    #     mean_row = 'Mean:'
    #     for i in range(3):
    #         max_err = max(abs(val[:num_pred, i] - pred[:num_pred, i]))
    #         mean_err = np.mean(val[:num_pred, i] - pred[:num_pred, i])
    #         max_chg = max(abs(pred[:num_pred, i] - last_pred[:num_pred, i]))
    #         mean_chg = np.mean(pred[:num_pred, i] - last_pred[:num_pred, i])
    #
    #         max_row += '\t\t{:5.1f}\t{:5.1f}\t'.format(max_err, max_chg)
    #         mean_row += '\t\t{:5.1f}\t{:5.1f}\t'.format(mean_err, mean_chg)
    #
    #     print('----------------------------------------------------------------------------------------------')
    #     print(max_row)
    #     print(mean_row)
    #

    def process(self) -> None:
        # Get the model that from the model manager created based on the configuration.
        # This may be a new model or a partially trained model that was loaded from disk.
        model = self.model_mgr.model

        # Get the hyper and training parameters.
        sessions = self.parameters['Sessions']
        epochs = self.parameters['Epochs']
        batch_size = self.parameters['BatchSize']
        lr = self.parameters['LearningRate']

        logger.info(
            'Session: {}, Epochs: {}, Batch Size: {}, Learning Rate: {}'.format(
                sessions, epochs, batch_size, lr))

        # Set up the tensor board callback to generate output files to review
        # the training progress.
        tb_path = os.path.join(self.configuration['tf-graph-dir-path'])
        tb_call_back = TensorBoard(log_dir=tb_path,
                                   histogram_freq=0,
                                   write_graph=True,
                                   write_images=True)

        # Set up the optimizer and it's hyperparameters.
        optimizer = Adam(lr=lr, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

        # Specify what the metrics are that the optimizer will use to measure loss.
        model.compile(loss='mse', optimizer=optimizer, metrics=['mae'])

        # Loop through all the sessions as specified in the configuration.
        for session in range(sessions):
            logger.info(
                'Session: {} of {}'.format(session + 1, sessions))

            # Train!
            model.fit(self.split_data_mgr.train_image, self.split_data_mgr.train_label,
                      batch_size=batch_size,
                      epochs=epochs,
                      verbose=1,
                      callbacks=[tb_call_back])

            # Save the model so that we can easily break out of training and Change
            # hyperparameters and then reload the model and restart training where
            # we left off.
            self._model_mgr.save_model()

            score = model.evaluate(self.split_data_mgr.test_image, self.split_data_mgr.test_label, verbose=0)
            print('Test score:', score[0])
            # this is the one we care about
            print('Test mean absolute error:', score[1])

            if self.parameters['predict']:
                self.predictor.process()
                #
                #         # to make this prediction and then redo it when we predict the engire
                #         # validation set for tracking of the training errors.
                #         pred = self._model.predict(
                #             self._X_val[:self._num_predictions], batch_size=1)
                #
                #         # Generate output to the screen to easily see what progress is being
                #         # made from one training sesson to the next.
                #         print('   Target | Prediction | Error | Change')
                #         print('Theta\t\t\t\t Radius\t\t\t\tAlpha')
                #
                #         # Allocate the space for the theta, radius, alpha information to be
                #         # displayed
                #         results = [''] * 3
                #
                #         for i in range(self._num_predictions):
                #             fmt = '{:5.1f}\t{:5.1f}\t{:5.1f}\t{:5.1f}'
                #             for j in range(3):
                #                 results[j] = fmt.format(
                #                     self._y_val[i][j],
                #                     pred[i][j],
                #                     self._y_val[i][j] -
                #                     pred[i][j],
                #                     pred[i][j] -
                #                     self._last_pred[i][j])
                #             print('{}\t{}\t{}'.format(results[0], results[1], results[2]))
                #
                #         self._print_stats(
                #             self._num_predictions,
                #             self._y_val,
                #             pred,
                #             self._last_pred)
                #
                #         for i in range(self._num_predictions):
                #             for j in range(3):
                #                 self._last_pred[i][j] = pred[i][j]
                #
                #         # Run the model against the validation dataset and save the results
                #         # to generate the training error animation.
                #         pred = self._model.predict(self._X_val, batch_size=1)
                #         pred_file_path = os.path.join(
                #             self._cfg['PredDirPath'],
                #             '{0:04d}'.format(session) + '.csv')
                #
                #         val_df = pd.DataFrame(self._y_val)
                #         pred_df = pd.DataFrame(pred)
                #         results_df = pd.concat((val_df, pred_df), axis=1)
                #         results_df.columns = [
                #             'vTheta',
                #             'vRadius',
                #             'vAlpha',
                #             'pTheta',
                #             'pRadius',
                #             'pAlpha']
                #
                #         print('Saving prediction results: ', pred_file_path)
                #         results_df.to_csv(pred_file_path, ',', index=False)