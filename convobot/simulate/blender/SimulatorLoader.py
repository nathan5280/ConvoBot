import logging
from convobot.simulate.blender.MonoSimulator import MonoSimulator
from convobot.simulate.blender.StereoSimulator import StereoSimulator
from convobot.simulate.blender.AnimationSimulator import AnimationSimulator
from convobot.util.FilenameManager import FilenameManager
from convobot.util.CfgMgr import CfgMgr

logger = logging.getLogger(__name__)
simulators = {'mono-simulator': MonoSimulator,
                'stereo-simulator': StereoSimulator,
                'animiation-simulator': AnimationSimulator}

class SimulatorLoader(object):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_simulate_cfg()

    def get_simulator(self):
        name = self._cfg['Name']
        logger.debug('Loading simulator: %s', name)
        return simulators[name](self._cfg_mgr)
