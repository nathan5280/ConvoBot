import logging
from abc import ABCMeta

from convobot.processor.Processor import Processor

logger = logging.getLogger(__name__)


class Trainer(Processor, metaclass=ABCMeta):
    """
    Base class for trainers.  Provide access to the configuration information.
    """

    def __init__(self, name, cfg):
        """
        Construct the base manipulator
        :param name: Name of the processor stage.
        :param cfg: Processor configuration
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)
