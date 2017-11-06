import importlib
import logging
import shutil
from abc import ABCMeta

import os

from convobot.model import ModelMgr
from convobot.processor.Processor import Processor
from convobot.processor.manipulator.SplitDataMgr import SplitDataMgr
from convobot.processor.predictors.Predictor import Predictor
from convobot.processor.predictors.TrainPredictor import TrainPredictor

logger = logging.getLogger(__name__)


class Trainer(Processor, metaclass=ABCMeta):
    """
    Base class for trainers.  Provide access to the configuration information.
    """

    def __init__(self, name, cfg):
        """
        Construct the base trainer

        :param name: Name of the processor stage.
        :param cfg: Processor configuration
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)
        self._model_mgr = None
        self._split_data_mgr = SplitDataMgr(self.src_dir_path)
        self._predictor = None

    @property
    def model_mgr(self) -> ModelMgr:
        """
        Access the model defined in the configuration.  The process follows this hierarchy:
        1) Model already loaded
        2) Model stored on disk
        3) Model constructed from script.

        :return: ModelMgr
        """
        if self._model_mgr is None:
            # Move any global or stage configuration data over to the model dictionary.
            model_cfg = {'configuration': {}, 'parameters': {}}
            model_cfg['configuration']['dst-dir-path'] = self.dst_dir_path
            model_cfg['parameters'] = self.parameters['model']
            model_cfg['parameters']['image'] = self.parameters['image']

            mod_name = self.parameters['model-module']
            mod = importlib.import_module(mod_name)

            # Get the class definition
            cls = getattr(mod, self.parameters['model-class'])

            # Instantiate the class
            self._model_mgr = cls(self.parameters['model-name'], model_cfg)

        return self._model_mgr

    @property
    def split_data_mgr(self):
        """
        Access the data manager.

        :return: SplitDataMgr
        """
        return self._split_data_mgr

    @property
    def predictor(self) -> Predictor:
        """
        Access to a predictor that can run intermediate predictions against the model.
        The predictor saves the results for reporting and charting of the training process.

        :return: Predictor
        """

        # Move any global or stage configuration data over to the prediction dictionary.
        if self._predictor is None:
            predict_cfg = {'configuration': {}, 'parameters': {}}
            predict_cfg['configuration']['src-dir-path'] = self.src_dir_path
            predict_cfg['configuration']['dst-dir-path'] = self.dst_dir_path
            predict_cfg['configuration']['pred-dir-path'] = self.configuration['pred-dir-path']
            predict_cfg['parameters'] = self.parameters['predictor']

            self._predictor = TrainPredictor(self.parameters['predictor-name'], predict_cfg,
                                             self._model_mgr.model, self._split_data_mgr)

        return self._predictor

    def reset(self) -> None:
        """
        Reset the training stage.  Delete the model.

        :return: None
        """
        self._model_mgr.reset()

        # Clean up any other tracker files

    def sweep(self) -> None:
        """
        Sweep up any files created by the stage but not required for future stages.

        :return: None
        """
        graph_dir_path = os.path.join(self.dst_dir_path, 'graph')
        if os.path.exists(graph_dir_path):
            shutil.rmtree(graph_dir_path)
