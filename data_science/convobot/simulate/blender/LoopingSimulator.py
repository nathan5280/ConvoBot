import time, sys, os, logging
import numpy as np
from convobot.simulate.blender.Simulator import Simulator
from convobot.util.FilenameManager import FilenameManager
from convobot.util.CfgMgr import CfgMgr

logger = logging.getLogger(__name__)

# TODO: Make this an abstract base class
# TODO: Put the abstract method Render in this class to make sure subclasses implement it.
# TODO: Consider consilidating this with the AnnimationSimulator class.

class LoopingSimulator(Simulator):
    '''
    Core method for simulating images based on the configuration.  This class
    assumes that all features are varying.
    '''
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        super(LoopingSimulator, self).__init__(cfg_mgr)

        self._filename_mgr = FilenameManager()


    def process(self):
        '''
        Iterate over all the ranges for Radius, Theta, Alpha and render the images.
        If the image already exists skip the rendering cycle.  This allows the creation
        of a dataset at a course level and then additional passes to fill in the
        points with finer divisions.
        '''
        logging.debug('Processing')

        # Get the configurations for each feature.
        radius_cfg = self._cfg['Radius']['Range']
        alpha_cfg = self._cfg['Alpha']['Range']
        theta_cfg = self._cfg['Theta']['Range']

        # Calculate Alpha decay fator to reduce alpha as we get further away
        # and we want to turn less to keep the target in the image.
        b1 = (alpha_cfg['MaxFactor'] - alpha_cfg['MinFactor']) / (radius_cfg['Max'] - radius_cfg['Min'])
        b0 = alpha_cfg['MinFactor'] - b1 * radius_cfg['Min']

        # set the range as fixed value or the dynamically created range.
        radius_range = np.arange(radius_cfg['Min'],
                                radius_cfg['Max'] + radius_cfg['Step'],
                                radius_cfg['Step'])

        for radius in radius_range:
            # Decay the alpha linearly by the radius with a slope of decay
            # TODO: Remove this as it doesn't agree with the images from the
            # physical camera and makes it hard for the CNN to learn the radius
            # parameter.
            alpha_range_adj_factor =  b0 + b1 * radius
            alpha_adj_step = alpha_cfg['Step'] * alpha_range_adj_factor

            # Assume centered range. Scale relative to zero
            alpha_min = alpha_cfg['Min'] * alpha_range_adj_factor
            alpha_max = (alpha_cfg['Max']  + alpha_adj_step) * alpha_range_adj_factor
            alpha_range = np.arange(alpha_min, alpha_max, alpha_adj_step)

            for alpha in alpha_range:
                theta_range = np.arange(theta_cfg['Min'],
                                        theta_cfg['Max'] + theta_cfg['Step'],
                                        theta_cfg['Step'])

                for theta in theta_range:
                    t0 = time.time()

                    image_dir_path = self._cfg['SimDirPath']
                    file_path = self._filename_mgr.label_to_radius_path(image_dir_path, theta, radius, round(alpha,1))
                    self._cfg_mgr.insure_dir_path(file_path)

                    # Don't render the image if it exists and has size > 0.
                    # This allows for breaking a simulation and restarting it without
                    # having to recreate all the image.   This is helpful when filling in an
                    # existing dataset.
                    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
                        # Call the render method in the subclass.
                        self._render(file_path, float(theta), float(radius), 180+float(round(alpha,1)))

                    process_time = time.time() - t0

                    # if logger.isEnabledFor(logging.DEBUG):
                    #     file_path_parts = file_path.split('/')
                    #     logger.debug('File: {}, Process Time: {:.2f}'.format(file_path_parts[-1], process_time))
