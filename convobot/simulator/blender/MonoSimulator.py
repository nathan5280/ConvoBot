# import os, sys, getopt
import time, sys
import numpy as np
from convobot.workflow.ConfigurationManager import ConfigurationManager
from convobot.util.FilenameManager import FilenameManager
from convobot.simulator.blender.Simulator import Simulator

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

class MonoSimulator(Simulator):
    def __init__(self, cfg_mgr, verbose=False):
        super(MonoSimulator, self).__init__(cfg_mgr, verbose)


    def process(self):
        '''
        Connect to blender and run the simulation.
        '''
        fnm = FilenameManager()

        simulation_cfg = self._cfg_mgr.get_cfg()['Simulation']
        radius_cfg = simulation_cfg['Radius']['Range']
        alpha_cfg = simulation_cfg['Alpha']['Range']
        theta_cfg = simulation_cfg['Theta']['Range']

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
            alpha_range_adj_factor =  b0 + b1 * radius
            alpha_adj_step = alpha_cfg['Step'] * alpha_range_adj_factor


            # Assume centered range. Scale relative to zero
            alpha_min = alpha_cfg['Min'] * alpha_range_adj_factor
            alpha_max = (alpha_cfg['Max']  + alpha_adj_step) * alpha_range_adj_factor
            alpha_range = np.arange(alpha_min, alpha_max, alpha_adj_step)

            # print('{:3.1f}\t{:3.1f}\t{:3.1f}\t{:3.1f}\t{}'\
            #         .format(radius, alpha_range_adj_factor, alpha_min, alpha_max, alpha_adj_step))


            for alpha in alpha_range:
                theta_range = np.arange(theta_cfg['Min'],
                                        theta_cfg['Max'] + theta_cfg['Step'],
                                        theta_cfg['Step'])

                for theta in theta_range:
                    t0 = time.time()

                    self._blender_env.set_camera_location(float(theta),
                                            float(radius), 180+float(round(alpha,1)))
                    # self._blender_env.set_camera_location(0, 15, 180)
                    # exit()

                    path = self._cfg_mgr.get_simulation_image_path()
                    filename = fnm.label_to_radius_path(path, theta, radius, 180+round(alpha,1))

                    render_time = self._blender_env.render(filename)
                    process_time = time.time() - t0

                    filename_parts = filename.split('/')
                    print('File: {}, Process Time: {:.2f}'.format(filename_parts[-1], process_time))
