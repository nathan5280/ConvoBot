import logging
from convobot.manipulate.Manipulator import Manipulator
from convobot.util.TreeUtil import TreeUtil

logger = logging.getLogger(__name__)

class CountManipulator(Manipulator):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        super(CountManipulator, self).__init__(cfg_mgr)

        self._count = 0

    def get_count(self):
        return self._count

    def process(self):
        def converter(src_path, dst_path, filename):
            self._count += 1

        tree_util = TreeUtil(self._cfg['SimDirPath'], self._cfg['ManDirPath'])
        tree_util.apply_files(converter, '*.png')
