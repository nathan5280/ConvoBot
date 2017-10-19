import json, shutil, logging, os
import unittest

from convobot.environment.GlobalCfgMgr import GlobalCfgMgr
from convobot.util.load_logging_cfg import load_logging_cfg

load_logging_cfg('./logging-cfg.json')
logger = logging.getLogger(__name__)

class TestGlobalCfgMgr(unittest.TestCase):
    _tmp_dir_path = 'tmp'
    _data_dir_path = os.path.join(_tmp_dir_path, 'data')
    _cfg_file_path = os.path.join(_tmp_dir_path, 'config.json')

    @classmethod
    def setUpClass(cls):
        '''
        Create a test temporary directory for the tests to create their directories in.
        '''
        if not os.path.exists(cls._tmp_dir_path):
            os.mkdir(cls._tmp_dir_path)

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the test temporary directory.
        '''
        if os.path.exists(cls._tmp_dir_path):
            shutil.rmtree(cls._tmp_dir_path)

    def setUp(self):
        pass

    def tearDown(self):
        '''
        Remove any directories that a single test created.
        '''
        shutil.rmtree(self._data_dir_path)

    def _write_cfg(self, cfg):
        '''
        Write the configuration file to the temporary directory.
        Args:
            cfg: The configuration dictionary to write.
        '''
        with open(self._cfg_file_path, 'w') as cfg_file:
            json.dump(cfg, cfg_file)

    def test_root_dir(self):
        '''
        Test the most basic configuration.  Load the Global configuration section.
        '''
        os.mkdir(self._data_dir_path)
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-b']
        sim_cfg = \
        {
            "Global": {
                "Image": {
                    "Size": [32, 32],
                    "Channels": 3
                }
            }
        }
        self._write_cfg(sim_cfg)

        global_cfg_mgr = GlobalCfgMgr()
        global_cfg_mgr.configure(argv)

        self.assertEqual('tmp/data/tmp', global_cfg_mgr.tmp_dir_path, 'Temparary Directory')
        self.assertEqual([32,32], global_cfg_mgr.image_size, 'Image size')
        self.assertEqual(3, global_cfg_mgr.image_channels, 'Image channels')

    def test_dir_build(self):
        '''
        Test to see if all the required directories are correctly created.
        '''
        os.mkdir(self._data_dir_path)
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-s',
                '-m',
                '-t',
                '-b']
        sim_cfg = \
        {
            "Global": {
                "Image": {
                    "Size": [32, 32],
                    "Channels": 3
                }
            }
        }
        self._write_cfg(sim_cfg)

        global_cfg_mgr = GlobalCfgMgr()
        global_cfg_mgr.configure(argv)

        self.assertTrue(os.path.exists(global_cfg_mgr.simulation_dir_path), 'Simulation dir path')
        self.assertTrue(os.path.exists(global_cfg_mgr.manipulation_dir_path), 'Manipulation dir path')
        self.assertTrue(os.path.exists(global_cfg_mgr.animation_dir_path), 'Animation dir path')
        self.assertTrue(os.path.exists(global_cfg_mgr.training_dir_path), 'Training dir path')
        self.assertTrue(os.path.exists(global_cfg_mgr.prediction_dir_path), 'Prediction dir path')

if __name__ == '__main__':
    unittest.main()