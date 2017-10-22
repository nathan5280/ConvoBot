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
