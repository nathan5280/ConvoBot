import logging
import os
import numpy as np
import pandas as pd

from convobot.processor.manipulator.Manipulator import Manipulator

logger = logging.getLogger(__name__)


class CartesianManipulator(Manipulator):
    """
    The CartesianManipulator adds X, Y labels
    """

    def __init__(self, name: str, cfg):
        """
        Construct the cartesian manipulator.

        :param name: Name of the manipulator
        :param cfg: The stage configuration
        """
        logger.debug('Constructing: %s', self.__class__.__name__)

        super().__init__(name, cfg)

        self._out_label_file_path = os.path.join(self.dst_dir_path,
                                                 self.parameters['out-label-file-prefix'] + 'label.npy')

    def reset(self):
        """
        Remove all the numpy label files.
        :return: None
        """
        if os.path.exists(self._out_label_file_path):
            os.remove(self._out_label_file_path)

    def process(self) -> None:
        """
        Load the radial label file and add the X, Y columns.
        :return: None
        """

        logger.info('Processing stage: %s', self._name)

        if not os.path.exists(self._out_label_file_path):
            # Load the file
            in_label_file_path = os.path.join(self.src_dir_path, self.parameters['in-label-file-prefix'] + 'label.npy')
            label_arr = np.load(in_label_file_path)
            label_df = pd.DataFrame(label_arr, columns=['Theta', 'Radius', 'Alpha'])

            # Add the columns
            label_df['X'] = label_df.Radius * np.cos(np.radians(label_df.Theta))
            label_df['Y'] = label_df.Radius * np.sin(np.radians(label_df.Theta))

            # Write the file
            logger.debug("Writing XY Label File %s, %s", self._out_label_file_path, label_df.shape)
            np.save(self._out_label_file_path, label_df.values, allow_pickle=False)
