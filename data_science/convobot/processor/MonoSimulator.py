import logging
import os

from convobot.processor.LoopingSimulator import LoopingSimulator
from convobot.util.FilenameMgr import FilenameMgr

logger = logging.getLogger(__name__)


class MonoSimulator(LoopingSimulator):
    """
    Simulate images based on the configuration.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the Processor.
        :param name: Name of the processor stage
        :param cfg: Processor configuration.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)
        self._filename_mgr = FilenameMgr()

    def _render(self, theta: float, radius: float, alpha: float) -> None:
        """
        Render the images for the given Theta, Radius, Alpha
        :param theta: Theta for camera location
        :param radius: Radius for camera location
        :param alpha: Alpha for camera location
        :return: None
        """
        file_path = self._filename_mgr.label_to_radius_path(self.dst_dir_path, theta, radius, alpha)
        # Make sure the path exists to write the file.  They are chucked up by radius.
        dir_path = os.path.split(file_path)[0]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        self._blender_env.set_camera_location(theta, radius, round(alpha, 1))
        self._blender_env.render(file_path)
