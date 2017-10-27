import importlib
import logging
from abc import ABCMeta
from convobot.model import ModelMgr
from convobot.processor.Processor import Processor

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
        self._model_mgr = self._load_model_mgr()

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
        pass

    def _load_model_mgr(self) -> ModelMgr:
        """
        Dynamically load the model based on the configuration parameters.

        :return: Model
        """

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
        model_mgr = cls(self.parameters['model-name'], model_cfg)
        return model_mgr
