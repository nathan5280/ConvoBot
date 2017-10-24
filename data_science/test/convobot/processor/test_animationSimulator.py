import os
import shutil
import json
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.workflow.CfgPipeline import CfgPipeline


class TestAnimationSimulator(TestCase):
    """
    Smoke tests for the AnimationSimulator.
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
                "animated": "animated"
            },
            "stages": {
                "animate-theta": {
                    "processor": {
                        "type": "generator",
                        "module": "convobot.processor.AnimationSimulator",
                        "class": "AnimationSimulator",
                        "dirs": {
                            "dst-dir-id": "animated"
                        },
                    },
                    "config": {
                        "movie-name": "theta.gif",
                        "reverse": False,
                        "radius": {
                            "fixed": 15.0
                        },
                        "theta": {
                            "range": {
                                "min": 0.0,
                                "max": 360.0,
                                "step": 30.0
                            }
                        },
                        "alpha": {
                            "fixed": 0.0
                        }
                    }
                },
                "animate-radius": {
                    "processor": {
                        "type": "generator",
                        "module": "convobot.processor.AnimationSimulator",
                        "class": "AnimationSimulator",
                        "dirs": {
                            "dst-dir-id": "animated"
                        },
                    },
                    "config": {
                        "movie-name": "radius.gif",
                        "reverse": True,
                        "radius": {
                            "range": {
                                "min": 15.0,
                                "max": 30.0,
                                "step": 1.0
                            }
                        },
                        "theta": {
                            "fixed": 45.0
                        },
                        "alpha": {
                            "fixed": 0.0
                        }
                    }
                },
                "animate-alpha": {
                    "processor": {
                        "type": "generator",
                        "module": "convobot.processor.AnimationSimulator",
                        "class": "AnimationSimulator",
                        "dirs": {
                            "dst-dir-id": "animated"
                        },
                    },
                    "config": {
                        "movie-name": "alpha.gif",
                        "reverse": True,
                        "radius": {
                            "fixed": 15.0
                        },
                        "theta": {
                            "fixed": 45.0
                        },
                        "alpha": {
                            "range": {
                                "min": -10.0,
                                "max": 10.0,
                                "step": 5.0
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
        Run animiation on Theta, Radius, Alpha and insure that the gif files are created.
        :return:
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-p', 'animate-theta',
                '-p', 'animate-radius',
                '-p', 'animate-alpha']

        self._write_cfg(self._sim_cfg)

        global_cfg_mgr = GlobalCfgMgr(argv)

        # Create the pipeline of the three animation processors and execute them.
        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        # Simple test to see if the three gif files were creates.
        animated_files = os.listdir(os.path.join(self._data_dir_path, 'animated'))
        self.assertTrue('alpha.gif' in animated_files, 'alpha.gif')
        self.assertTrue('theta.gif' in animated_files, 'theta.gif')
        self.assertTrue('radius.gif' in animated_files, 'radius.gif')
