import logging
from convobot.manipulate.Manipulator import Manipulator
from convobot.util.TreeUtil import TreeUtil

logger = logging.getLogger(__name__)


class CountManipulator(Manipulator):
    '''
    The CountManipulator uses functional programming model to apply a count
    method across the tree of images.
    '''

    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        # Delegate the management of the manipulator configuration to the
        # Manipulator base class.
        super(CountManipulator, self).__init__(cfg_mgr)

        # Counter for the number of files as the image tree is traversed.
        self._count = 0

    def get_count(self):
        '''
        Return the count.

        Returns: Number of images counted during the tree traversal.
        '''
        return self._count

    # TODO: Coordinate changes with the TreeUtil class to create an apply_files
    # method that doesn't require a dst_path for manipulators that work in
    # place.
    def process(self):
        '''
        Count the files by functionally applying the converter method to the tree.
        '''
        def converter(src_path, dst_path, filename):
            '''
            The functional part of the manipulator that increments the count.

            Args:
              src_path: Root directory path where the recursive count should begin.
              dst_path: Not used for in place manipulator.
              filename: Not used by simple counter manipulator

            Returns: None

            '''
            self._count += 1

        # Create the TreeUtil to apply the convert function to the recursively to the
        # tree of images.
        tree_util = TreeUtil(self._cfg['SimDirPath'], self._cfg['ManDirPath'])
        tree_util.apply_files(converter, '*.png')
