import logging
import json

from convobot.processor.Processor import Processor
from convobot.util.TreeUtil import TreeUtil
from convobot.util.FilenameMgr import FilenameMgr

logger = logging.getLogger(__name__)


class Manipulator(Processor):
    """
    Manipulator base class used to manage the global and manipulator configurations.
    """

    def __init__(self, name, cfg):
        """
        Construct the base manipulator
        :param name: Name of the processor stage.
        :param cfg: Processor configuration
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)

        # Create a FileManager to help with the conversion of Theta, Radius,
        # alpha feature parameters to and from filenames.
        self._filename_manager = FilenameMgr()

