import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class CfgStage(metaclass=ABCMeta):
    """
    Base class for all Configured Stages.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the configured stage.
        :param name: Name of the stage.
        :param cfg: Configuration for the stage.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        self._name = name
        self._stage_cfg = cfg  # Overall stage configuration including the processor configuration items.
        self._configuration = self.stage_cfg.get('configuration', None)  # Stage configuration (directories)
        self._parameters = self.stage_cfg.get('parameters', None)  # Processor parameters

    @property
    def stage_cfg(self):
        """
        Access the stage configuration.
        :return: Stage configuration dictionary
        """
        return self._stage_cfg

    @property
    def configuration(self):
        """
        Access the configuration portion of the stage configuration.
        :return:
        """
        return self._configuration

    @property
    def parameters(self):
        """
        Access the parameters portion of the stage configuration
        :return: Parameters configuration dictionary
        """
        return self._parameters

    @property
    def tmp_dir_path(self) -> str:
        """
        Access the path to the temporary directory.
        :return: Temporary directory path.
        """
        return self.configuration['tmp-dir-path']

    @property
    def src_dir_path(self) -> str:
        """
        Access the path to the source directory.
        :return: Source directory path
        """
        return self.configuration.get('src-dir-path', None)

    @property
    def dst_dir_path(self) -> str:
        """
        Access the path to the destination directory
        :return: Destination directory path
        """
        return self.configuration.get('dst-dir-path', None)

    @property
    def name(self) -> str:
        """
        Name of the processor.
        :return: Name of the processor.
        """
        return self._name

