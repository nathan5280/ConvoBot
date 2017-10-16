import time, os, logging
from convobot.simulate.blender.LoopingSimulator import LoopingSimulator
from convobot.util.CfgMgr import CfgMgr

logger = logging.getLogger(__name__)

class MonoSimulator(LoopingSimulator):
    '''
    Simulate images with a mono (single) camera.
    '''
    def __init__(self, cfg_mgr):
        logger.info("Initializing")
        super(MonoSimulator, self).__init__(cfg_mgr)


    def _render(self, file_path, theta, radius, alpha):
        '''

        Args:
          file_path: The location to store the rendered image.
          theta: The theta value for the camera.
          radius: The radius value for the camera.
          alpha: The alpha value for the camera.

        Returns: None

        '''
        self._blender_env.set_camera_location(theta, radius, round(alpha, 1))
        render_time = self._blender_env.render(file_path)
