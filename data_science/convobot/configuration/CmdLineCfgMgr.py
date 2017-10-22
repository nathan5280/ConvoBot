import argparse, logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class CmdLineCfgMgr(object):
    """
    Command line parser.
    """

    def __init__(self):
        """
        Build the commandline argument parser for the convobot applications.
        """
        logger.debug('Constructor: %s', self.__class__.__name__)

        self._parser = argparse.ArgumentParser(description='Run ConvoBot CNN stages.')
        self._parser.add_argument('-d', dest='data-dir-path', required=True,
                                  help='Root path for data storage')

        self._parser.add_argument('-c', dest='cfg-file-path', required=True,
                                  help='Path to configuration file relative application run directory.')

        self._parser.add_argument('-s', dest='stage-ids', action='append',
                                  help='Specify if the simulation stage should be run.')

    def parse(self, argv: List[str]) -> Dict[str, str]:
        """
        Parse the command line arguments per the parser configuration.

        :param argv: Command line arguments to parse.
        :return: dictionary of configuration parameters.
        """
        logger.debug('Argv: %s', argv)
        return vars(self._parser.parse_args(argv))
