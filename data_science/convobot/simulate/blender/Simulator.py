import Pyro4, json, logging, sys
from abc import ABC, abstractmethod

from convobot.environment import GlobalCfgMgr

logger = logging.getLogger(__name__)

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

class Simulator(ABC):
    '''
    Connect to the Env running in Blender's python environment
    '''
    def __init__(self, global_cfg_mgr):
        '''
        Connection to Blender through SnakeShake.
        Args:
            global_cfg_mgr: Access to global configuration.
        '''
        logger.debug('Initializing')
        self._global_cfg_mgr = global_cfg_mgr
        self._cfg = self._global_cfg_mgr.get_stage_cfg('Simulation')

        logger.debug('Initializing Blender environment')
        logger.debug(json.dumps(self._cfg, indent=4))

        # Connect to the SnakeShake Server running in Blender.
        # https://github.com/nathan5280/SnakeShake
        sys.excepthook = Pyro4.util.excepthook
        self._blender_env = Pyro4.Proxy("PYRONAME:Env")

        # Get the image size information from the global section of the configuration.
        self._image_size = self._global_cfg_mgr.image_size

        # Get the Blender environment to some known state based on the
        # Simulation configuration.
        camera_direction = 180
        self._blender_env.set_render_resolution(self._image_size[0], self._image_size[1])
        self._blender_env.set_camera_height(self._cfg['CameraHeight'])
        self._blender_env.set_camera_focal_length(30)
        self._blender_env.set_camera_location(0, 15, camera_direction)

    @abstractmethod
    def process(self):
        '''

        Returns: None

        '''
        pass

