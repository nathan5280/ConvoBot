import time, os, logging
from PIL import Image
import numpy as np
from convobot.simulate.blender.LoopingSimulator import LoopingSimulator

logger = logging.getLogger(__name__)

class StereoSimulator(LoopingSimulator):
    '''
    Simulator to simulate a stacked stereoscopic image.  Two images are
    generated and stored in the tmp directory.  One for the left and one for
    the right with a spacing specified in the configuration file.

    These images are then loaded, resized, stacked and saved to the simulate
    image tree as if they were a single generated image.
    '''
    def __init__(self, global_cfg_mgr):
        '''
        Args:
            global_cfg_mgr: Global configuration manager.
        '''
        logger.debug('Initializing')
        super(StereoSimulator, self).__init__(global_cfg_mgr)

    def _render(self, file_path, theta, radius, alpha):
        '''
        Process the request from the baseclass to render the image from the specified
        location in the simulation environment and store it at the specified
        file path.

        Args:
          file_path: The location to store the final rendered stero stacked image.
          theta: The radial angle from the x-axis to simulate the image from.
          radius: The radius from the center of the target to simulate the image from .
          alpha: The twist of the robot relative to the radius.

        Returns:  None
        '''
        # Render the left and right images into a temporary directory.
        # Load and resize them to a stacked format and save to the filename
        # requested as if rendering a mono image.
        tmp_dir_path = self._global_cfg_mgr.tmp_dir_path
        self._global_cfg_mgr.clear_tmp()

        omega = self._cfg['StereoOffset']
        # Don't render the image if it exists and has size > 0.
        # This allows for breaking a simulation and restarting it without
        # having to recreate all the image.   This is helpful when filling in an
        # existing dataset.
        right_file_path = os.path.join(tmp_dir_path, 'right.png')
        self._blender_env.set_camera_location(theta + omega, radius, round(alpha - omega, 1))
        self._blender_env.render(right_file_path)

        # Left Image
        left_file_path = os.path.join(tmp_dir_path, 'left.png')
        self._blender_env.set_camera_location(theta - omega, radius, round(alpha + omega, 1))
        self._blender_env.render(left_file_path)

        img_l = Image.open(left_file_path)
        img_r = Image.open(right_file_path)

        # convert to np.array, concatentate (stack) them on top of each other
        # and convert back to PIL image.
        npl = np.array(img_l)
        npr = np.array(img_r)
        nps = np.concatenate((npl, npr), axis=0)
        img_stk = Image.fromarray(nps)
        img = img_stk.resize((self._image_size[0], self._image_size[1]))

        # Save the stereo stacked image.
        img.save(file_path)
