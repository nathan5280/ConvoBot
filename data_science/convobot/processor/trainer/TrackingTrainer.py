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

    def process(self) -> None:
        # Get the model that from the model manager created based on the configuration.
        # This may be a new model or a partially trained model that was loaded from disk.
        model = self.model_mgr.model

        # Get the hyper parameters.
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
