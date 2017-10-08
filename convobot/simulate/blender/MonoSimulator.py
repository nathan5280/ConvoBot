import time, os, logging
from convobot.simulate.blender.LoopingSimulator import LoopingSimulator
from convobot.util.CfgMgr import CfgMgr

logger = logging.getLogger(__name__)

class MonoSimulator(LoopingSimulator):
    def __init__(self, cfg_mgr):
        logger.info("Initializing")
        super(MonoSimulator, self).__init__(cfg_mgr)


    def _render(self, file_path, theta, radius, alpha):
        self._blender_env.set_camera_location(theta, radius, round(alpha, 1))
        render_time = self._blender_env.render(file_path)
