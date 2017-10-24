import json
import shutil
import logging
import os
import unittest

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.util.load_logging_cfg import load_logging_cfg

load_logging_cfg('./logging-cfg.json')
logger = logging.getLogger(__name__)


class TestGlobalCfgMgr(unittest.TestCase):
    """
    Smoke tests for GlobalCfgMgr.  Creates a tmp directory to create configuration files
    in for the different test cases.
    """
    _tmp_dir_path = 'tmp'
    _data_dir_path = os.path.join(_tmp_dir_path, 'data')
    _cfg_file_path = os.path.join(_tmp_dir_path, 'config.json')

    # Partial configuration to test with.
    _sim_cfg = \
        {
            "global": {
                "description": "Convobot Test",
                "date": "Sat Oct 21 08:53:36 MDT 2017",
                "image": {
                    "size": [
                        32,
                        32
                    ],
                    "channels": 3
                },
                "camera-height": 5
            },
            "dir-paths": {
                "simulated": "simulated",
                "manipulated": "manipulated",
                "trained": "trained",
                "animated": "animated"
            },
            "stages": {
                "stage1": {
                    "processor": {
                        "type": "generator",
                        "module": "convobot.processor.MonoSimulator",
                        "class": "MonoSimulator",
                        "dirs": {
                            "dst-dir-id": "simulated"
                        },
                    },
                    "config": {}
                },
                "stage2": {
                    "processor": {
                        "type": "transformer",
                        "module": "convobot.processor.NumpyManipulator",
                        "class": "NumpyManipulator",
                        "dirs": {
                            "src-dir-id": "simulated",
                            "dst-dir-id": "manipulated"
                        },
                    },
                    "config": {
                        "processor-cfg-item1": "item1"
                    }
                }
            }
        }

    @classmethod
    def setUpClass(cls):
        """
        Create a test temporary directory that is used for all of the tests in this class.
        :return: None
        """
        if not os.path.exists(cls._tmp_dir_path):
            os.mkdir(cls._tmp_dir_path)

    @classmethod
    def tearDownClass(cls):
        """
        Remove the test temporary directory to clean things up.
        :return: None
        """
        if os.path.exists(cls._tmp_dir_path):
            shutil.rmtree(cls._tmp_dir_path)

    def setUp(self):
        pass

    def tearDown(self):
        """
        Remove any directories that a single test created.
        """
        shutil.rmtree(self._data_dir_path)

    def _write_cfg(self, cfg):
        """
        Helper method to write the configuration to the test temp directory as a json file.
        :param cfg: Configuration to write.
        :return: None
        """
        with open(self._cfg_file_path, 'w') as cfg_file:
            json.dump(cfg, cfg_file)

    def test_root_dir(self):
        """
        Test the most basic configuration.  Load the Global configuration section.

        :return: None
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path]
        self._write_cfg(self._sim_cfg)

        GlobalCfgMgr(argv)
        self.assertTrue(os.path.exists(self._data_dir_path), 'data-dir-path')

    def test_stage_cfg(self):
        """
        Test to see if configuration contains the directory paths..

        :return: None
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-p', 'stage2']

        self._write_cfg(self._sim_cfg)

        global_cfg_mgr = GlobalCfgMgr(argv)
        stage_cfg = global_cfg_mgr.stage_cfg('stage2')

        print(json.dumps(stage_cfg, indent=2))

        self.assertEqual(os.path.join(self._data_dir_path, 'simulated'), stage_cfg['processor']['src-dir-path'],
                         'simulated')
        self.assertEqual(os.path.join(self._data_dir_path, 'manipulated'), stage_cfg['processor']['dst-dir-path'],
                         'manipulated')
        self.assertEqual(os.path.join(self._data_dir_path, 'tmp'), stage_cfg['processor']['tmp-dir-path'],
                         'temporary')
        self.assertEqual('item1', stage_cfg['config']['processor-cfg-item1'], 'item1')
        self.assertEqual(5, stage_cfg['config']['camera-height'])

        if __name__ == '__main__':
            unittest.main()
