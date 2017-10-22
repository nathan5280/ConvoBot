import logging
import os
import shutil
import subprocess
import time

import numpy as np

from convobot.processor.Simulator import Simulator

logger = logging.getLogger(__name__)


class AnimationSimulator(Simulator):
    """
    Drive the simulation where only one of the 3 features varies and convert the
    still images to a gif.  If the configuration specifies that the image sequence
    needs to run forward and backwards (reverse) then read all the images back in
    and copy them out in reverse order.

    The images are named with a monotonically increasing id starting a 000 to
    support ffmpeg.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the Processor.
        :param name: Name of the processor stage
        :param cfg: Processor configurtation.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)

    def process(self) -> None:
        """
        Simulate the images where two features are held constant and the
        third is varied.  This is the current configuration.  This could be
        combined with the LoopingSimulator as the functionality has a fair
        amount of overlap.

        Write the images to files in a tree where images are in directories
        based on the radius feature.  Use FilenameManager to convert from
        radius, theta, alpha to a unique filename.

        Use the 'fixed' configuration format to specify which features should
        be held constant.

        :return: None
        """

        logger.info('Processing stage: %s', self._name)

        # Generate a sequence of images in the temporary directory.
        # Run ffmpeg on them to create the move and store it in
        # the movies directory.
        index = 0

        # Based on the configuration either generate a range or fixed set of
        # indexes for the simulation.
        if 'range' in self._process_cfg['radius']:
            radius_cfg = self._process_cfg['radius']['range']
            radius_range = np.arange(radius_cfg['min'],
                                     radius_cfg['max'] + radius_cfg['step'],
                                     radius_cfg['step'])
        else:
            radius_range = [self._process_cfg['radius']['fixed']]

        for radius in radius_range:
            if 'range' in self._process_cfg['alpha']:
                alpha_cfg = self._process_cfg['alpha']['range']
                alpha_range = np.arange(alpha_cfg['min'],
                                        alpha_cfg['max'] + alpha_cfg['step'],
                                        alpha_cfg['step'])
            else:
                alpha_range = [self._process_cfg['alpha']['fixed']]

            for alpha in alpha_range:
                if 'range' in self._process_cfg['theta']:
                    theta_cfg = self._process_cfg['theta']['range']
                    theta_range = np.arange(theta_cfg['min'],
                                            theta_cfg['max'] + theta_cfg['step'],
                                            theta_cfg['step'])
                else:
                    theta_range = [self._process_cfg['theta']['fixed']]

                for theta in theta_range:
                    t0 = time.time()

                    file_path = os.path.join(self.tmp_dir_path, '{0:03d}'.format(index) + '.png')

                    # Don't render the image if it exists and has size > 0.
                    # This allows for breaking a simulation and restarting it without
                    # having to recreate all the image.   This is helpful when filling in an
                    # existing dataset.
                    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
                        self._blender_env.set_camera_location(float(theta), float(radius),
                                                              180 + float(round(alpha, 1)))
                        self._blender_env.render(file_path)

                    process_time = time.time() - t0

                    if logger.isEnabledFor(logging.DEBUG):
                        file_path_parts = file_path.split('/')
                        logger.debug('File: {}, Process Time: {:.2f}'.format(file_path_parts[-1], process_time))

                    index += 1

        # Create the movie from the rendered images.  If reverse is specified
        # let the make_movie method handle the duplication of the images.
        self._make_movie(index)

    def _make_movie(self, index: int):
        """
        Build the movie from a sequence of images.  If the movie should play in a forward reverse loop
        create a reverse copy of the images to complete the loop.
        :param index: The index of the last file that was generated on the forward pass.  This is used to start the
        indexing of the reverse pass.
        :return: None
        """

        # If the movie plays forward and backwards then make copies of the
        # forward frames in reverse order with continuing indexes.
        if self._process_cfg['reverse']:
            frame_names = os.listdir(self.tmp_dir_path)
            frame_names.reverse()
            for frame_name in frame_names:
                src_file_path = os.path.join(self.tmp_dir_path, frame_name)
                dst_file_path = os.path.join(self.tmp_dir_path, '{0:03d}'.format(index) + '.png')
                shutil.copyfile(src_file_path, dst_file_path)
                index += 1

        # Create the movie using ffmpeg.
        dst_file_path = os.path.join(self.dst_dir_path, '{}'.format(self._process_cfg['movie-name']))
        src_file_pattern = os.path.join(self.tmp_dir_path, '%03d.png')

        # Run ffmpeg to convert the still png files to a movie.
        cmd_arr = ['ffmpeg', '-i', src_file_pattern, dst_file_path]
        subprocess.run(cmd_arr)
