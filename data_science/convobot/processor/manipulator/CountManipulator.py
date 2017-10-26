import logging

from convobot.util.TreeUtil import TreeUtil
from convobot.processor.manipulator.Manipulator import Manipulator

logger = logging.getLogger(__name__)


class CountManipulator(Manipulator):
    """
    The CountManipulator uses functional programming model to apply a count
    method across the tree of images.
    """

    def __init__(self, root_dir_path: str, file_pattern: str):
        """
        Construct the count manipulator.

        :param root_dir_path: Root directory to apply manipulator.
        :param file_pattern: Filename pattern to count.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)

        super().__init__('counter', {})
        self._root_dir_path: str = root_dir_path
        self._file_pattern: str = file_pattern

        # Counter for the number of files as the image tree is traversed.
        self._count: int = 0

    def get_count(self) -> int:
        """
        Count of images counted by the counter.
        :return: Count of images.
        """
        return self._count

    def process(self) -> None:
        """
        Count the files by functionally applying the converter method to the tree.

        :return: None
        """

        def converter(src_path: str, dst_path: str, filename: str):
            """
            The functional part of the manipulator that increments the count.

            :param src_path: Not used by this manipulator.
            :param dst_path: Not used by this manipulator.
            :param filename: Not used by this manipulator.
            :return: None
            """

            # Ignore these parameters.  Assign them so they don't cause a static inspection warning.
            _, _, _ = src_path, dst_path, filename

            self._count += 1

        # Create the TreeUtil to apply the convert function to the recursively to the
        # tree of images.
        tree_util = TreeUtil(self._root_dir_path, self._root_dir_path)
        tree_util.apply_files(converter, self._file_pattern)
