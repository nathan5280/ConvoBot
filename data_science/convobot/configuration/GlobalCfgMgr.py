import json
import os
import logging
import glob
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

        # Create the temporary directory and clear it in case it already existed.
        self._tmp_dir_path: str = os.path.join(self._data_dir_path, 'tmp')
        self._validate_path(self._tmp_dir_path)
        self.clear_tmp()

        # Add the list of stages to run to the configuration.
        self._process_stages: List[str] = cmd_cfg['stage-ids']
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
        stage_cfg['config'].update(**global_cfg)
        return stage_cfg

    @property
    def stage_names(self) -> List[str]:
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

        if self._process_stages:
            for stage in self._process_stages:
                stage_cfg = self._app_cfg['stages'][stage]
                processor_cfg = stage_cfg['processor']

                # determine if the stage is a generator or transformer.
                # Generators only have destination directory.
                # Transformers have both destination and source.
                if processor_cfg['type'] == 'transformer':
                    source_id = processor_cfg['src-id']
                    source_rel_path = self._app_cfg['dir-paths'][source_id]

                    # Add the source directory to the configuration.
                    processor_cfg['src-dir-path'] = os.path.join(self._data_dir_path, source_rel_path)
                    self._validate_path(processor_cfg['src-dir-path'])

                destination_id = processor_cfg['dst-id']
                destination_rel_path = self._app_cfg['dir-paths'][destination_id]

                # Add the destination directory to the configuration.
                processor_cfg['dst-dir-path'] = os.path.join(self._data_dir_path, destination_rel_path)
                self._validate_path(processor_cfg['dst-dir-path'])

                # Add the temporary directory in case the stage needs it.
                processor_cfg['tmp-dir-path'] = self._tmp_dir_path

                logger.debug('Directory validate: stage: %s\n%s', stage, json.dumps(stage_cfg, indent=2))

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

    def clear_tmp(self) -> None:
        """
        Recursively remove any files and directories in the temporary directory.
        :return: None
        """
        files = glob.glob(os.path.join(self._tmp_dir_path, '*'))
        for file in files:
            os.remove(file)
