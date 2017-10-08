import logging
from convobot.util.CfgMgr import CfgMgr
from convobot.manipulate.CountManipulator import CountManipulator
from convobot.manipulate.NumpyManipulator import NumpyManipulator

logger = logging.getLogger(__name__)
manipulators = {'count-manipulator': CountManipulator,
                'numpy-manipulator': NumpyManipulator}

class ManipulatorLoader(object):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_manipulate_cfg()

    def get_manipulator(self):
        name = self._cfg['Name']
        logger.debug('Loading manipulator: %s', name)
        return manipulators[name](self._cfg_mgr)
