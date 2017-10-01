from convobot.simulator.blender.MonoSimulator import MonoSimulator
from convobot.simulator.blender.StereoSimulator import StereoSimulator
from convobot.workflow.ConfigurationManager import ConfigurationManager

simulators = {'mono': MonoSimulator, 'stereo': StereoSimulator}

class SimulatorLoader(object):
    def __init__(self, cfg_mgr, verbose=False):
        self._cfg_mgr = cfg_mgr
        self._cfg = cfg_mgr.get_cfg()
        self._verbose = verbose

    def get_simulator(self):
        name = self._cfg['Simulation']['SimulatorName']

        if self._verbose:
            print('Loading simulator: ', name)

        return simulators[name](self._cfg_mgr)
