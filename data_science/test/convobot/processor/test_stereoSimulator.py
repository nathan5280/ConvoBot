import glob
import os
import shutil
import json
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.util.load_logging_cfg import load_logging_cfg
from convobot.workflow.CfgPipeline import CfgPipeline

load_logging_cfg('./logging-cfg.json')


class TestStereoSimulator(TestCase):
    """
    Smoke tests for the StereoSimulator.
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
                "camera-height": 5,
                "stereo-offset": 3
            },
            "dir-paths": {
                "simulated": "simulated"
            },
            "stages": {
                "simulate": {
                    "configuration": {
                        "type": "generator",
                        "module": "convobot.processor.StereoSimulator",
                        "class": "StereoSimulator",
                        "dirs": {
                            "dst-dir-id": "simulated"
                        },
                    },
                    "parameters": {
                        "movie-name": "theta.gif",
                        "reverse": False,
                        "radius": {
                            "range": {
                                "min": 15.0,
                                "max": 16.0,
                                "step": 1.0
                            },
                        },
                        "theta": {
                            "range": {
                                "min": 0.0,
                                "max": 360.0,
                                "step": 30.0
                            },
                        },
                        "alpha": {
                            "range": {
                                "min": -10.0,
                                "max": 10.0,
                                "step": 10.0
                            }
                        }
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

    def test_process(self):
        """
        Run simulation.
        :return:
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-p', 'simulate']

        self._write_cfg(self._sim_cfg)

        global_cfg_mgr = GlobalCfgMgr(argv)

        # Create the pipeline of the three animation processors and execute them.
        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        dst_dir_path = os.path.join(self._data_dir_path, 'simulated', '15.0', '*')
        self.assertEqual(39, len(glob.glob(dst_dir_path)), '15.0')

        dst_dir_path = os.path.join(self._data_dir_path, 'simulated', '16.0', '*')
        self.assertEqual(39, len(glob.glob(dst_dir_path)), '16.0')