import logging
from abc import ABCMeta, abstractmethod
from keras.models import load_model

import os

from convobot.configuration.CfgStage import CfgStage

logger = logging.getLogger(__name__)


class Model(CfgStage, metaclass=ABCMeta):
    """
    Base class for models.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the processor.
        :param name: Name of the processor.
        :param cfg: Configuration for the processor.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)
        self._model_file_path = os.path.join(self.dst_dir_path, self.parameters['model-file-name'])
        self._model = None

    @property
    def model(self):
        """
        Load or build the model.

        :return: Model
        """
        if self._model is None:
            if os.path.exists(self._model_file_path):
                logger.info('Loading model: %s: %s', self._name, self._model_file_path)
                self._model = load_model(self._model_file_path)
            else:
                # Build the model.
                logger.info('Building model: %s: %s', self._name, self._model_file_path)
                self._model = self._build_model()

        return self._model

    @abstractmethod
    def _build_model(self):
        pass

    def reset(self):
        """
        Delete the model to reset the training.

        :return: None
        """
        if os.path.exists(self._model_file_path):
            os.remove(self._model_file_path)

    def save_model(self):
        """
        Persist the model to disk.
        """
        logger.debug('Saving model: %s: %s', self._name, self._model_file_path)
        self._model.save(self._model_file_path)
