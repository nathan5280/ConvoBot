import logging
import os
import shutil

import numpy as np
from PIL import Image

from convobot.processor.simulator.LoopingSimulator import LoopingSimulator
from convobot.util.FilenameMgr import FilenameMgr

logger = logging.getLogger(__name__)


class StereoSimulator(LoopingSimulator):
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

    def reset(self):
        """
        Remove all the simulated image files.
        :return: None
        """
        dirs = glob.glob(os.path.join(self.dst_dir_path, '*'))
        for dir in dirs:
            shutil.rmtree(dir)

    def _render(self, theta: float, radius: float, alpha: float) -> None:
        """
        Render the images for the given Theta, Radius, Alpha
        :param theta: Theta for camera location
        :param radius: Radius for camera location
        :param alpha: Alpha for camera location
        :return: None
        """
        file_path = self._filename_mgr.label_to_radius_path(self.dst_dir_path, theta, radius, alpha)
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            return
        else:
            # Render the left and right images into a temporary directory.
            # Load and resize them to a stacked format and save to the filename
            # requested as if rendering a mono image.

            omega = self.parameters['stereo-offset']
            # Don't render the image if it exists and has size > 0.
            # This allows for breaking a simulation and restarting it without
            # having to recreate all the image.   This is helpful when filling in an
            # existing dataset.
            right_file_path = os.path.join(self.tmp_dir_path, 'right.png')
            self._blender_env.set_camera_location(theta + omega, radius, alpha - omega)
            self._blender_env.render(right_file_path)

            # Left Image
            left_file_path = os.path.join(self.tmp_dir_path, 'left.png')
            self._blender_env.set_camera_location(theta - omega, radius, alpha + omega)
            self._blender_env.render(left_file_path)

            img_l = Image.open(left_file_path)
            img_r = Image.open(right_file_path)

            # convert to np.array, concatenate (stack) them on top of each other
            # and convert back to PIL image.
            npl = np.array(img_l)
            npr = np.array(img_r)
            nps = np.concatenate((npl, npr), axis=0)
            img_stk = Image.fromarray(nps)
            img = img_stk.resize(self._parameters['image']['size'])

            # Make sure the path exists to write the file.  They are chucked up by radius.
            dir_path = os.path.split(file_path)[0]
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

            # Save the stereo stacked image.
            img.save(file_path)



