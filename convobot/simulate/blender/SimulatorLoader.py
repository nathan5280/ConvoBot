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
    '''
    Load the correct simulator based on the name in the configuration file.
    '''
    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: The global configuration manager.

        Returns: None
        '''
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_simulate_cfg()

    def get_simulator(self):
        '''
        Dynamically create the simulator based on the configuration.

        Args:

        Returns: The configured Simulator
        '''
        name = self._cfg['Name']
        logger.debug('Loading simulator: %s', name)
        return simulators[name](self._cfg_mgr)
