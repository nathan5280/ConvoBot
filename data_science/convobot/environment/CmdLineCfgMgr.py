import argparse, sys, os
import logging

logger = logging.getLogger(__name__)

class CmdLineCfgMgr(object):
    '''
    Command line parser.
    '''
    def __init__(self, argv):
        '''
        Build the commandline argument parser for the convobot applications.

        Args:
            argv: The commandline arguments to parse.
        '''
        logger.debug('Parsing command line arguments: %s', argv)

        parser = argparse.ArgumentParser(description='Run ConvoBot CNN stages.')
        parser.add_argument('-d', dest='DataDirPath', required=True,
                            help='Root path for data storage')

        parser.add_argument('-c', dest='CfgFilePath', required=True,
                            help='Path to configuration file relative application run directory.')

        parser.add_argument('-s', dest='RunSimulation', action='store_true', default=False,
                            help='Specify if the simulation stage should be run.')

        parser.add_argument('-a', dest='RunAnimation', action='store_true', default=False,
                            help='Specify if the animation stage should be run.')

        parser.add_argument('-m', dest='RunManipulation', action='store_true', default=False,
                            help='Specify if the image manipulation stage should be run.')

        parser.add_argument('-t', dest='RunTraining', action='store_true', default=False,
                            help='Specify if the training stage should be run.')

        parser.add_argument('-r', dest='RunReporting', action='store_true', default=False,
                            help='Specify if the reporting stage should be run.')

        parser.add_argument('-b', dest='BuildDirs', action='store_true', default=False,
                            help='Specifiy if missing directories should be auto created.')

        self._cfg = parser.parse_args(argv)

    @property
    def cfg_dict(self):
        '''
        Get the commandline arguments as a dictionary.

        Returns: dictionary of commandline arguments
        '''
        return vars(self._cfg)
