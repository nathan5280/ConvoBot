import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class Processor(metaclass=ABCMeta):
    """
    Base class for all Processors.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the processor.
        :param name:
        :param cfg:
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        self._name = name
        self._stage_cfg = cfg  # Overall stage configuration including the processor configuration items.
        self._process_cfg = self.stage_cfg['config']  # Just the configuration that is required for the process method.

    @property
    def stage_cfg(self):
        """
        Access the stage configuration.
        :return: Stage configuration dictionary
        """
        return self._stage_cfg

    @property
    def process_cfg(self):
        """
        Access the process configuration
        :return: Process configuration dictionary
        """
        return self._process_cfg

    @property
    def tmp_dir_path(self) -> str:
        """
        Access the path to the temporary directory.
        :return: Temporary directory path.
        """
        return self.stage_cfg['processor']['tmp-dir-path']

    @property
    def src_dir_path(self) -> str:
        """
        Access the path to the source directory.
        :return: Source directory path
        """
        return self.stage_cfg['processor'].get('src-dir-path', None)

    @property
    def dst_dir_path(self) -> str:
        """
        Access th
        :return:
        """
        return self.stage_cfg['processor'].get('dst-dir-path', None)

    @property
    def name(self) -> str:
        """
        Name of the processor.
        :return: Name of the processor.
        """
        return self._name

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