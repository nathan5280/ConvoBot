import json
import os
import logging
from typing import List, Dict

from convobot.configuration.CmdLineCfgMgr import CmdLineCfgMgr

logger = logging.getLogger(__name__)


class GlobalCfgMgr(object):
    """
    Manage the overall configuration of the application.  Merge
    the command line configuration and the application config.json.
    Create directories as required.

    Stage configurations are constructed from the application configuration with
    specified substitutions.

    1) Global section is always provided.
    2) source, destination and temporary directories are created
    3) stage/config section
    """

    def __init__(self, argv: List[str]) -> None:
        """
        Construct the global configuration from the command line arguments
        and the config.json.

        :param argv: Command line arguments to parse.
        :return: None
        """
        logger.debug('Constructor %s', self.__class__.__name__)

        # Parse argv into configuration parameter dictionary.
        cmd_cfg: Dict[str, str] = CmdLineCfgMgr().parse(argv)

        # Load the configuration file specified on the command line
        # Path is specified relative to the application run directory.
        cfg_file_path = cmd_cfg['cfg-file-path']
        with open(cfg_file_path) as cfg_file:
            self._app_cfg = json.load(cfg_file)

        logger.debug('Argv: \n%s', json.dumps(cmd_cfg, indent=2))
        logger.debug('App Config: \n%s', json.dumps(self._app_cfg, indent=2))

        # Create the root directory for the simulation.
        # Expand the user directory if it is specified with ~
        self._data_dir_path: str = os.path.expanduser(cmd_cfg['data-dir-path'])
        self._validate_path(self._data_dir_path)

        # Create the temporary directory.
        self._tmp_dir_path = os.path.join(self._data_dir_path, 'tmp')
        self._validate_path(self._tmp_dir_path)

        # Add the list of stages to sweep, reset, and process to the configuration.
        # Test to see if there were any ids specified on the command line first.
        # If none were specified the key is still in the dictionary, but has a value of None.
        if cmd_cfg['sweep-stage-ids']:
            self._sweep_stages: List[str] = cmd_cfg['sweep-stage-ids']
        else:
            self._sweep_stages: List[str] = []

        if cmd_cfg['reset-stage-ids']:
            self._reset_stages: List[str] = cmd_cfg['reset-stage-ids']
        else:
            self._reset_stages: List[str] = []

        if cmd_cfg['process-stage-ids']:
            self._process_stages: List[str] = cmd_cfg['process-stage-ids']
        else:
            self._process_stages: List[str] = []

        # If there are any macros defined, explode them into the lists of actions to execute.
        self._expand_macros(cmd_cfg['macro-ids'])

        # Explode all the lists into a set.
        self._all_stages = {*[*self._sweep_stages, *self._reset_stages, *self._process_stages]}
        self._check_required_directories()

    def stage_cfg(self, stage_name: str):
        """
        Get stage configuration including the global section, temporary, source and destination directories.
        :param stage_name: Stage to build the configuration for.
        :return: Stage configuration dictionary
        """
        stage_cfg = self._app_cfg['stages'][stage_name]
        global_cfg = self._app_cfg['global']

        # Copy all of the global configuration items into the stage config section
        stage_cfg['parameters'].update(**global_cfg)
        return stage_cfg

    @property
    def sweep_stages(self) -> List[str]:
        """
        Get the list of stages to sweep.
        :return: Names of the stages to sweep.
        """
        return self._sweep_stages

    @property
    def reset_stages(self) -> List[str]:
        """
        Get the list of stages to reset.
        :return: Names of the stages to reset.
        """
        return self._reset_stages

    @property
    def process_stages(self) -> List[str]:
        """
        Get the list of stages to process.
        :return: Names of the stages to process.
        """
        return self._process_stages

    def _check_required_directories(self) -> None:
        """
        Create any directories that are required for the stages configured to run.
        :return: None
        """

        if self._all_stages:
            for stage in self._all_stages:
                stage_cfg = self._app_cfg['stages'][stage]
                processor_cfg = stage_cfg['configuration']

                # Populate all the directories requested in the configuration.
                for dir_key, dir_id in processor_cfg['dirs'].items():
                    dir_path_value = os.path.join(self._data_dir_path, self._app_cfg['dir-paths'][dir_id])
                    # Rebuild the key by replacing 'id' with 'path'
                    dir_path_key = dir_key.replace('id', 'path')
                    processor_cfg[dir_path_key] = dir_path_value

                    # Create the directory if it doesn't exist.
                    self._validate_path(dir_path_value)

                # Add the temporary directory.
                processor_cfg['tmp-dir-path'] = self._tmp_dir_path

                del processor_cfg['dirs']

    def _expand_macros(self, macro_ids) -> None:
        """
        Expand the macros onto the action lists for the sweep, reset, and process.

        :param macro_ids: List of macros from the command line to expand.

        :return: None
        """
        if macro_ids is None:
            return

        for macro_id in macro_ids:
            macro_cfg = self._app_cfg['macros'][macro_id]

            self._sweep_stages.extend(macro_cfg.get('sweeps', []))
            self._reset_stages.extend(macro_cfg.get('resets', []))
            self._process_stages.extend(macro_cfg.get('processes', []))


    @staticmethod
    def _validate_path(dir_path: str) -> None:
        """
        Validate that a path exists.  If not create it.
        :param dir_path: Path to validate.
        :return: None
        """
        if os.path.exists(dir_path):
            return

        logger.info('Creating directory: %s', dir_path)
        os.mkdir(dir_path)

    @property
    def tmp_dir_path(self) -> str:
        """
        Path to the temporary directory
        :return: Path
        """
        return self._tmp_dir_path
