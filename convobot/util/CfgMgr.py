import json, os, logging, shutil

logger = logging.getLogger(__name__)

class CfgMgr(object):
    def __init__(self, cmd_line_cfg):
        logger.debug('Initializing configuration, cmd_line_cfg %s', cmd_line_cfg)
        self._cmd_line_cfg = cmd_line_cfg

        # Load the configuration file specified on the command line
        cfg_file_path = os.path.join(self._cmd_line_cfg['CfgDirPath'],
                            self._cmd_line_cfg['CfgFilename'])

        with open(cfg_file_path) as cfg_file:
            self._cfg = json.load(cfg_file)

        # Verify that there is a Global section
        if 'Global' in self._cfg:
            self._global_cfg = self._cfg['Global']
        else:
            logger.error('No Global section found in %s', cfg_file_path)
            exit()

        # If running simulate make sure we have a configuration section.
        if self._cmd_line_cfg['RunSimulate']:
            if 'Simulate' in self._cfg:
                logger.info('Loading simulate configuration')
                self._simulate_cfg = self._cfg['Simulate']
                logger.debug('Simulate cfg: \n %s', json.dumps(self._simulate_cfg, indent=4))
            else:
                logger.error('No Simulate section found in %s', cfg_file_path)
                exit()

        # If running manipulate make sure we have a configuration section.
        if self._cmd_line_cfg['RunManipulate']:
            if 'Manipulate' in self._cfg:
                logger.info('Loading manipulate configuration')
                self._manipulate_cfg = self._cfg['Manipulate']
                logger.debug('Manipulate cfg: %s', json.dumps(self._manipulate_cfg, indent=4))
            else:
                logger.error('No Manipulate section found in %s', cfg_file_path)
                exit()

        # If running train make sure we have a configuration section.
        if self._cmd_line_cfg['RunTrain']:
            if 'Train' in self._cfg:
                logger.info('Loading train configuration')
                self._train_cfg = self._cfg['Train']
                logger.debug('Train cfg: %s', json.dumps(self._train_cfg, indent=4))
            else:
                logger.error('No Train section found in %s', cfg_file_path)
                exit()

    def _get_simulate_dir_path(self):
        dir_path = os.path.join(self._cmd_line_cfg['DataDirPath'], 'simulate')

        # Make sure the path exists
        if not os.path.exists(dir_path):
            logger.warn('Simulate SimDirPath does not exist: {}'.format(dir_path))
            exit()

        return dir_path

    def get_simulate_cfg(self):
        # Copy any global information required for simulation to the simulate config.
        self._simulate_cfg['Image'] = self._global_cfg['Image']

        # Location to store the simulated images.
        self._simulate_cfg['SimDirPath'] = self._get_simulate_dir_path()

        # Location to store the movies if this is an animation simulation
        self._simulate_cfg['MovieDirPath'] = \
                os.path.join(self._cmd_line_cfg['DataDirPath'], 'movies')

        # Make sure the path exists
        if not os.path.exists(self._simulate_cfg['MovieDirPath']):
            logger.warn('Simulate MovieDirPath does not exist: {}'.
                    format(self._simulate_cfg['MovieDirPath']))
            exit()

        return self._simulate_cfg

    def _get_manipulate_dir_path(self):
        dir_path = os.path.join(self._cmd_line_cfg['DataDirPath'], 'manipulate')

        # Make sure the path exists
        if not os.path.exists(dir_path):
            logger.warn('Manipulate ManDirPath does not exist: {}'.format(dir_path))
            exit()

        return dir_path

    def get_manipulate_cfg(self):
        # Copy any global information required for simulation to the manipulate config.
        self._manipulate_cfg['Image'] = self._global_cfg['Image']

        # Location of the stored simulated images.
        self._manipulate_cfg['SimDirPath'] = self._get_simulate_dir_path()

        # Location to store the manipulated images.
        self._manipulate_cfg['ManDirPath'] = self._get_manipulate_dir_path()

        return self._manipulate_cfg

    def _get_train_dir_path(self):
        dir_path = os.path.join(self._cmd_line_cfg['DataDirPath'], 'train')

        # Make sure the path exists
        if not os.path.exists(dir_path):
            logger.warn('Train TrnDirPath does not exist: {}'.format(dir_path))
            exit()

        return dir_path

    def get_train_cfg(self):
        # Copy any global information required for simulation to the manipulate config.
        self._train_cfg['Image'] = self._global_cfg['Image']

        # Location to store the manipulated images.
        self._train_cfg['ManDirPath'] = self._get_manipulate_dir_path()

        # Location of the stored simulated images.
        self._train_cfg['TrnDirPath'] = self._get_train_dir_path()

        # Location of the prediction results.
        dir_path = os.path.join(self._cmd_line_cfg['DataDirPath'], 'prediction')

        # Make sure the path exists
        if not os.path.exists(dir_path):
            logger.warn('Prediction PredDirPath does not exist: {}'.format(dir_path))
            exit()

        self._train_cfg['PredDirPath'] = dir_path

        return self._train_cfg

    def initialize_temporary_dir_path(self):
        tmp_dir_path = os.path.join(self._cmd_line_cfg['DataDirPath'], 'tmp')
        if os.path.exists(tmp_dir_path):
            shutil.rmtree(tmp_dir_path)

        os.makedirs(tmp_dir_path)
        return tmp_dir_path

    def insure_dir_path(self, file_path):
        # split off the filename and work with the absolute path.
        dir_path = os.path.split(file_path)[0]

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
