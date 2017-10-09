import logging
import json
from convobot.util.TreeUtil import TreeUtil
from convobot.util.FilenameManager import FilenameManager

logger = logging.getLogger(__name__)

# TODO: Make this an abstract base class.
# TODO: Consider moving the SimulatorLoaer functionality in to this class as
# static class method.


class Manipulator(object):
    '''
    Manipulator base class used to manage the global and manipulator configurations.
    '''

    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: The global configuration manager.
        '''
        logger.debug('Initializing')

        # Keep track of the global configuration and the manipulator specific
        # configuration.
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_manipulate_cfg()

        logger.debug(json.dumps(self._cfg, indent=4))

        # Pull out the most commonly used configuration information from
        # the configuration to simplify configuration access in sub-classes.
        self._image_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']

        # Create a FileManager to help with the conversion of Theta, Radius,
        # alpha feature parameters to and from filenames.
        self._filename_manager = FilenameManager()

    # TODO: Implement abstract method
    # def process(self)
