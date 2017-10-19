import logging

from convobot.simulate.blender.AnimationSimulator import AnimationSimulator
from convobot.simulate.blender.MonoSimulator import MonoSimulator
from convobot.simulate.blender.StereoSimulator import StereoSimulator

logger = logging.getLogger(__name__)
simulators = {'mono-simulator': MonoSimulator,
                'stereo-simulator': StereoSimulator,
                'animation-simulator': AnimationSimulator}

class SimulatorLoader(object):
    '''
    Load the correct simulator based on the name in the configuration file.
    '''
    def __init__(self, global_cfg_mgr):
        '''
        Args:
            global_cfg_mgr: The global configuration manager.

        Returns: None
        '''
        logger.debug('Initializing')
        self._global_cfg_mgr = global_cfg_mgr
        self._cfg = self._global_cfg_mgr.get_stage_cfg('Simulation')

    def get_simulator(self):
        '''
        Dynamically create the simulator based on the configuration.

        Args:

        Returns: The configured Simulator
        '''
        name = self._cfg['Name']
        logger.debug('Loading simulator: %s', name)
        return simulators[name](self._global_cfg_mgr)
