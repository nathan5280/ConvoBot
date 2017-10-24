import logging
import time
from abc import abstractmethod

import numpy as np

from convobot.processor.simulator.Simulator import Simulator

logger = logging.getLogger(__name__)


class LoopingSimulator(Simulator):
    """
    Simulate images by looping through Theta, Radius and Alpha and rendering the image from that camera location
    in Blender.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the Processor.
        :param name: Name of the processor stage
        :param cfg: Processor configuration.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)

    def process(self) -> None:
        """
        Iterate over all the ranges for Radius, Theta, Alpha and render the images.
        If the image already exists skip the rendering cycle.  This allows the creation
        of a dataset at a course level and then additional passes to fill in the
        points with finer divisions.

        Call the render method in the subclass for the details of what and how to render the images.

        :return: None
        """

        logger.info('Processing stage: %s', self._name)

        # Based on the configuration either generate a range or fixed set of
        # indexes for the simulation.
        if 'range' in self._parameters['radius']:
            radius_cfg = self._parameters['radius']['range']
            radius_range = np.arange(radius_cfg['min'],
                                     radius_cfg['max'] + radius_cfg['step'],
                                     radius_cfg['step'])
        else:
            radius_range = [self._parameters['radius']['fixed']]

        for radius in radius_range:
            if 'range' in self._parameters['alpha']:
                alpha_cfg = self._parameters['alpha']['range']
                alpha_range = np.arange(alpha_cfg['min'],
                                        alpha_cfg['max'] + alpha_cfg['step'],
                                        alpha_cfg['step'])
            else:
                alpha_range = [self._parameters['alpha']['fixed']]

            for alpha in alpha_range:
                if 'range' in self._parameters['theta']:
                    theta_cfg = self._parameters['theta']['range']
                    theta_range = np.arange(theta_cfg['min'],
                                            theta_cfg['max'] + theta_cfg['step'],
                                            theta_cfg['step'])
                else:
                    theta_range = [self._parameters['theta']['fixed']]

                for theta in theta_range:
                    t0 = time.time()

                    self._render(theta, radius, 180 + alpha)

                    process_time = time.time() - t0

                    if logger.isEnabledFor(logging.DEBUG):
                        logger.debug(
                            'Radius: %s, Theta: %s, Alpha: %s, Time: %s' %
                                (radius, theta, 180 + alpha, round(process_time, 3)))

    @abstractmethod
    def _render(self, theta, radius, alpha):
        """
        Override this method in the subclass for the specifics of the render action.
        :param theta: Theta for camera location
        :param radius: Radius for camera location
        :param alpha: Alpha for camera location
        :return: None
        """
        pass
