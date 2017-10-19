import json, os, logging, shutil, glob

from convobot.environment.CmdLineCfgMgr import CmdLineCfgMgr
from convobot.util.Singleton import Singleton

logger = logging.getLogger(__name__)

class GlobalCfgMgr(metaclass=Singleton):
    '''
    Track the Global section of the configuration.

    Directory structure:

    data-dir
        tmp
        simulation
        animation
        manipulation
        training
        prediction
    '''
    def __init__(self):
        logger.debug('Instantiating %s', self.__class__.__name__)

    def configure(self, argv):
        '''
        Args:
            argv: Command line arguments.
        '''
        logger.debug('Configuring with command line: {cmd_line_args}'.format(cmd_line_args=argv))
        cmd_cfg = CmdLineCfgMgr(argv).cfg_dict

        # Load the configuration file specified on the command line
        cfg_file_path = cmd_cfg['CfgFilePath']

        with open(cfg_file_path) as cfg_file:
            app_cfg = json.load(cfg_file)

        # Explode the cmd line configuration and configuration file into a single dictionary.
        full_app_cfg = {**cmd_cfg, **app_cfg}
        logger.debug(json.dumps(full_app_cfg, indent=4))

        self._app_cfg = full_app_cfg
        self._global_cfg = self.get_stage_cfg('Global')

        # Create the root directory for the simulation.
        # Expand the user directory if it is specified with ~
        self._app_cfg['DataDirPath'] = os.path.expanduser(self._app_cfg['DataDirPath'])
        self._path_creator(self._data_dir_path, self._build_dirs)

        # Create the temporary directory and clear it in case it already existed.
        self._app_cfg['TmpDirPath'] = os.path.join(self._data_dir_path, 'tmp')
        self._path_creator(self.tmp_dir_path, self._build_dirs)
        self.clear_tmp()

        # Add the simulation directory path if run simulation is configured.
        self._add_simulation()

        # Add the animation directory path if run animation is configured.
        self._add_animation()

        # Add the manipulation directory paths if run manipulation is configured.
        self._add_manipulation()

        # Add the training directory paths if run training is configured.
        self._add_training()

    def get_stage_cfg(self, stage_name):
        '''
        Get a section of the configuration from the global configuration.

        Args:
            stage_name: Stage name for the requested configuration.

        Returns: Dictionary configuration for the requested stage.

        '''
        if not stage_name in self._app_cfg:
            msg = 'Configuration for stage {stage_name} missing.'.format(stage_name=stage_name)
            logger.error(msg)
            raise IndexError(msg)

        return self._app_cfg[stage_name]

    def _add_simulation(self):
        '''
        Create directories required to run simulation.

        Returns: None or exception if directory doesn't exist and build_dir is False

        '''
        if not self.run_simulation:
            return

        self._app_cfg['SimulationDirPath'] = os.path.join(self._data_dir_path, 'simulation')
        self._path_creator(self.simulation_dir_path, self._build_dirs)

    def _add_animation(self):
        '''
        Create directories required to run animation.

        Returns: None or exception if directory doesn't exist and build_dir is False

        '''
        if not self.run_animation:
            return

        self._app_cfg['AnimationDirPath'] = os.path.join(self._data_dir_path, 'animation')
        self._path_creator(self.animation_dir_path, self._build_dirs)

    def _add_manipulation(self):
        '''
        Create directories required to run manipulation.

        Returns: None or exception if directory doesn't exist and build_dir is False

        '''
        if not self.run_manipulation:
            return

        # Add the simulation directory as the source of the data files.
        self._app_cfg['SimulationDirPath'] = os.path.join(self._data_dir_path, 'simulation')
        self._path_creator(self.simulation_dir_path, self._build_dirs)

        # Add the manipulation directory as the target of the data files.
        self._app_cfg['ManipulationDirPath'] = os.path.join(self._data_dir_path, 'manipulation')
        self._path_creator(self.manipulation_dir_path, self._build_dirs)

    def _add_training(self):
        '''
        Create directories required to run training.

        Returns: None or exception if directory doesn't exist and build_dir is False

        '''
        if not self.run_training:
            return

        # Add the manipluation directory as the source of the data files.
        self._app_cfg['ManipulationDirPath'] = os.path.join(self._data_dir_path, 'manipulation')
        self._path_creator(self.manipulation_dir_path, self._build_dirs)

        # Target for training model and trace files.
        self._app_cfg['TrainingDirPath'] = os.path.join(self._data_dir_path, 'training')
        self._path_creator(self.training_dir_path, self._build_dirs)

        # Target for prediction traces.
        self._app_cfg['PredictionDirPath'] = os.path.join(self._data_dir_path, 'prediction')
        self._path_creator(self.prediction_dir_path, self._build_dirs)

    @property
    def _data_dir_path(self):
        '''

        Returns: The root directory for the data for the simulation.

        '''
        return self._app_cfg['DataDirPath']

    @property
    def simulation_dir_path(self):
        '''

        Returns: Simulation directory path.

        '''
        return self._app_cfg['SimulationDirPath']

    @property
    def animation_dir_path(self):
        '''

        Returns: Animation directory path.

        '''
        return self._app_cfg['AnimationDirPath']

    @property
    def manipulation_dir_path(self):
        '''

        Returns: Manipulation directory path.

        '''
        return self._app_cfg['ManipulationDirPath']

    @property
    def training_dir_path(self):
        '''

        Returns: Training directory path.

        '''
        return self._app_cfg['TrainingDirPath']

    @property
    def prediction_dir_path(self):
        '''

        Returns: Prediction directory path.

        '''
        return self._app_cfg['PredictionDirPath']

    @property
    def _build_dirs(self):
        '''

        Returns: Boolean indicating if directories should be automatically created if they don't exist.

        '''
        return self._app_cfg['BuildDirs']

    @property
    def tmp_dir_path(self):
        '''

        Returns: The path to the temporary directory for managing intermediate files.

        '''
        return self._app_cfg['TmpDirPath']

    @property
    def image_size(self):
        '''

        Returns: List of the images X and Y size.

        '''
        return self._global_cfg['Image']['Size']

    @property
    def image_channels(self):
        '''

        Returns: Number of channels in the image.

        '''
        return self._global_cfg['Image']['Channels']

    @property
    def run_simulation(self):
        '''

        Returns: True if simulation should be run.

        '''
        return self._app_cfg['RunSimulation']

    @property
    def run_animation(self):
        '''

        Returns: True if animation should be run.

        '''
        return self._app_cfg['RunAnimation']

    @property
    def run_manipulation(self):
        '''

        Returns: True if manipulation should be run.

        '''
        return self._app_cfg['RunManipulation']

    @property
    def run_training(self):
        '''

        Returns: True if training should be run.

        '''
        return self._app_cfg['RunTraining']


    def clear_tmp(self):
        '''

        Returns: Recursively remove any files and directories in the temporary directory.

        '''
        files = glob.glob(os.path.join(self.tmp_dir_path, '*'))
        for file in files:
            os.remove(file)

    @classmethod
    def _path_creator(cls, dir_path, build_dirs):
        '''
        Check to see if a directory exists.  If it doesn't and auto_create is true
        then create the directory.  Otherwise generate an exception.
        Args:
            dir_path: Path to directory to check.
            build_dirs: True to auto create the directory.

        Returns: None or exception.

        '''
        if os.path.exists(dir_path):
            return

        if build_dirs:
            logger.info('Creating directory: {dir_path}'.format(dir_path=dir_path))
            os.mkdir(dir_path)
        else:
            logger.error("Directory {dir_path} doesn't exist.  Create directory or specify -a".format(dir_path=dir_path))
            raise FileNotFoundError(1, "Required directory doesn't exist.", dir_path)

