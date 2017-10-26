from abc import ABCMeta

import Pyro4
import Pyro4.util
import logging
import sys

from convobot.processor.Processor import Processor

logger = logging.getLogger(__name__)


class Simulator(Processor, metaclass=ABCMeta):
    """
    Connect to the Env running in Blender's python environment
    """

    def __init__(self, name, cfg):
        """
        Connect to Blender through SnakeShake.
        :param name: Name of the processor stage.
        :param cfg: Processor configuration
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)

        logger.debug('Initializing Blender environment')

        # Connect to the SnakeShake Server running in Blender.
        # https://github.com/nathan5280/SnakeShake
        sys.excepthook = Pyro4.util.excepthook
        self._blender_env = Pyro4.Proxy("PYRONAME:Env")

        # Get the Blender environment to some known state based on the
        # Simulation configuration.
        camera_direction = 180
        self._blender_env.set_render_resolution(self._parameters['image']['size'][0],
                                                self._parameters['image']['size'][1])
        self._blender_env.set_camera_height(self._parameters['camera-height'])
        self._blender_env.set_camera_focal_length(30)
        self._blender_env.set_camera_location(0, 15, camera_direction)
