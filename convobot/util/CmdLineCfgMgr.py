import argparse, sys, os
import logging

logger = logging.getLogger(__name__)

class CmdLineCfgMgr(object):
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

        parser.add_argument('-c', dest='CfgDirPath', default='config',
                                help='Root path for loading configuration files. Defaults to "config"')

        parser.add_argument('-n', dest='CfgFilename',
                                    help='Name of the configuration file.  Defaults to the last directory name in the DataDirPath.')

        parser.add_argument('-s', dest='RunSimulate', action='store_true', default=False,
                                help='Specify if the simulation stage should be run.')

        parser.add_argument('-m', dest='RunManipulate', action='store_true', default=False,
                                help='Specify if the image manipulation stage should be run.')

        parser.add_argument('-t', dest='RunTrain', action='store_true', default=False,
                                help='Specify if the training stage should be run.')

        # TODO: Implement this and connect it to the QuiverError reporting class.
        parser.add_argument('-r', dest='RunReport', action='store_true', default=False,
                                help='Specify if the reportin stage should be run.')

        self._cfg = parser.parse_args(argv)

        # Check to see if a configuration file name was specified.  If not then
        # get the name from the last directory name in the DataDirPath argument.
        if not self._cfg.CfgFilename:
            self._cfg.CfgFilename = os.path.split(self._cfg.DataDirPath)[1] + '.json'


    def get_cfg_dict(self):
        '''
        Get the commandline arguements as a dictionary.

        Returns: dictionary of commandline arguments
        '''
        return vars(self._cfg)

if __name__ == '__main__':
    cfg_mgr = CmdLineCfgMgr(['-d', '/Users/nathanatkins/convobot'])
    cfg_dict = cfg_mgr.get_cfg_dict()
    print(cfg_dict)
