import os, json
from logging.config import dictConfig


def load_logging_cfg(logging_cfg_file_path):
    '''
    Simple function to load the logging configuration file if it exists.
    Otherwise print a notification that the logging configuration couldn't be found.
    '''
    if os.path.exists(logging_cfg_file_path):
        with open(logging_cfg_file_path, 'r') as f:
            logging_cfg = json.load(f)
            dictConfig(logging_cfg)
    else:
        print('Unable to load {file_path} logging configuration.  Proceeding with default configuration.'.format(
            file_path=logging_cfg_file_path))
