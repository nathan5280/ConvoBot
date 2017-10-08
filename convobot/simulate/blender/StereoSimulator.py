import time, os, logging
from PIL import Image
import numpy as np
from convobot.simulate.blender.LoopingSimulator import LoopingSimulator

logger = logging.getLogger(__name__)

class StereoSimulator(LoopingSimulator):
    def __init__(self, cfg):
        logger.debug('Initializing')
        super(StereoSimulator, self).__init__(cfg)

    def _render(self, file_path, theta, radius, alpha):
        # Render the left and right images into a temporary directory.
        # Load and resize them to a stacked format and save to the filename
        # requested as if rendering a mono image.
        tmp_dir_path = self._cfg_mgr.initialize_temporary_dir_path()

        omega = self._cfg['StereoOffset']
        # Don't render the image if it exists and has size > 0.
        # This allows for breaking a simulation and restarting it without
        # having to recreate all the image.   This is helpful when filling in an
        # existing dataset.
        right_file_path = os.path.join(tmp_dir_path, 'right.png')
        self._blender_env.set_camera_location(theta + omega, radius, round(alpha - omega, 1))
        render_time = self._blender_env.render(right_file_path)

        # Left Image
        left_file_path = os.path.join(tmp_dir_path, 'left.png')
        self._blender_env.set_camera_location(theta - omega, radius, round(alpha + omega, 1))
        render_time = self._blender_env.render(left_file_path)

        img_l = Image.open(left_file_path)
        img_r = Image.open(right_file_path)

        # convert to np.array, concatentate (stack) them on top of each other
        # and convert back to PIL image.
        npl = np.array(img_l)
        npr = np.array(img_r)
        nps = np.concatenate((npl, npr), axis=0)
        img_stk = Image.fromarray(nps)
        img = img_stk.resize((self._image_size[0], self._image_size[1]))

        img.save(file_path)
