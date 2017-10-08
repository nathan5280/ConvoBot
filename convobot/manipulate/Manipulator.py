import logging, json
from convobot.util.TreeUtil import TreeUtil
from convobot.util.FilenameManager import FilenameManager

logger = logging.getLogger(__name__)

# TODO: Make this an abstract base class.
# TODO: Consider moving the SimulatorLoaer functionality in to this class as
# static class method.

class Manipulator(object):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_manipulate_cfg()

        logger.debug(json.dumps(self._cfg, indent=4))

        self._image_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']
        self._filename_manager = FilenameManager()


    # TODO: Implement abstract method
    # def process(self)
