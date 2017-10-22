import logging
import os
import time
from abc import ABCMeta, abstractmethod

import numpy as np

from convobot.processor.Simulator import Simulator
from convobot.util.FilenameManager import FilenameManager

logger = logging.getLogger(__name__)

class LoopingSimulator(Simulator, metaclass=ABCMeta):
    '''
    Core method for simulating images based on the configuration.  This class
    assumes that all features are varying.
    '''
    def __init__(self, global_cfg_mgr):
        logger.debug('Initializing')
        super(LoopingSimulator, self).__init__(global_cfg_mgr)

        self._filename_mgr = FilenameManager()


    def process(self):
        '''
        Iterate over all the ranges for Radius, Theta, Alpha and render the images.
        If the image already exists skip the rendering cycle.  This allows the creation
        of a dataset at a course level and then additional passes to fill in the
        points with finer divisions.
        '''
        logging.debug('Processing')
        image_dir_path = self._global_cfg_mgr.simulation_dir_path

        radius_cfg = self.stage_cfg['Radius']['Range']
        radius_range = np.arange(radius_cfg['Min'],
                                radius_cfg['Max'] + radius_cfg['Step'],
                                radius_cfg['Step'])

        for radius in radius_range:
            alpha_cfg = self.stage_cfg['Alpha']['Range']
            alpha_range = np.arange(alpha_cfg['Min'],
                                    alpha_cfg['Max'] + alpha_cfg['Step'],
                                    alpha_cfg['Step'])

            # Make sure the directory exist to store the image file.
            output_dir_path = os.path.join(image_dir_path, str(round(radius,1)))
            self._global_cfg_mgr.path_creator(output_dir_path, True)

            for alpha in alpha_range:
                theta_cfg = self.stage_cfg['Theta']['Range']
                theta_range = np.arange(theta_cfg['Min'],
                                        theta_cfg['Max'] + theta_cfg['Step'],
                                        theta_cfg['Step'])

                for theta in theta_range:
                    t0 = time.time()

                    image_dir_path = self._global_cfg_mgr.simulation_dir_path
                    file_path = self._filename_mgr.label_to_radius_path(image_dir_path, theta, radius, alpha)

                    # Don't render the image if it exists and has size > 0.
                    # This allows for breaking a simulation and restarting it without
                    # having to recreate all the image.   This is helpful when filling in an
                    # existing dataset.
                    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
                        # Call the render method in the subclass.
                        self._render(file_path, float(theta), float(radius), 180+float(alpha))

                    process_time = time.time() - t0

                    if logger.isEnabledFor(logging.DEBUG):
                        file_path_parts = file_path.split('/')
                        logger.debug('File: {}, Process Time: {:.2f}'.format(file_path_parts[-1], process_time))

    @abstractmethod
    def _render(self, file_path, theta, radius, alpha):
        pass