import logging
from abc import ABCMeta, abstractmethod

from convobot.configuration.CfgStage import CfgStage

logger = logging.getLogger(__name__)


class Processor(CfgStage, metaclass=ABCMeta):
    """
    Base class for all Processors.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the processor.
        :param name: Name of the processor.
        :param cfg: Configuration for the processor.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        # self._name = name
        # self._stage_cfg = cfg  # Overall stage configuration including the processor configuration items.
        # self._configuration = self.stage_cfg.get('configuration', None)  # Stage configuration (directories)
        # self._parameters = self.stage_cfg.get('parameters', None)  # Processor parameters
        super().__init__(name, cfg)

    @abstractmethod
    def process(self) -> None:
        """
        Subclasses of processor implement this method.  Calling this method
        causes the Processor to perform it's main function.
        :return: None
        """
        pass

    def reset(self) -> None:
        """
        Remove output files that are required for future stages to process.  Removing these
        files will require this stage to be rerun to generate the replacement files.  Examples
        include simulated or manipulated image files or trained models.  Some processors will
        skip regenerating these files if the file exists by name and has a size > 0.  Without
        a call to reset the processor will incrementally add to the output files, but not replace
        them.  Reset clears these files and forces them to be recreated.
        :return: None
        """
        logger.info('Resetting: %s', self._name)

    def sweep(self) -> None:
        """
        Remove any nonessential files that are generated during normal processing.
        Examples include log files and intermediate prediction results used for generating
        reports, but aren't required for future stages to process.

        Subclasses only need to implement this if they have unique requirements.
        :return: None
        """
        logger.info('Sweeping: %s', self._name)
