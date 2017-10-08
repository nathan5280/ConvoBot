import Pyro4, time, sys, json, logging
from convobot.util.CfgMgr import CfgMgr

logger = logging.getLogger(__name__)

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

# TODO: Make this an abstract base class.
# TODO: Consider moving the SimulatorLoaer functionality in to this class as
# static class method.

class Simulator(object):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_simulate_cfg()

        logger.debug('Initializing Blender environment')
        logger.debug(json.dumps(self._cfg, indent=4))

        # Connect to the SnakeShake Server running in Blender.
        # https://github.com/nathan5280/SnakeShake
        sys.excepthook = Pyro4.util.excepthook
        self._blender_env = Pyro4.Proxy("PYRONAME:Env")

        self._image_size = self._cfg['Image']['Size']

        # Grid search the envrionment to create the images.
        camera_direction = 180
        self._blender_env.set_render_resolution(self._image_size[0], self._image_size[1])
        self._blender_env.set_camera_height(self._cfg['CameraHeight'])
        self._blender_env.set_camera_focal_length(30)
        self._blender_env.set_camera_location(0, 15, 180)

    # TODO: Implement abstract method
    # def process(self)
