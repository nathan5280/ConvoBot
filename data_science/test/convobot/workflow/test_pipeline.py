import os
import json
import shutil
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.processor.Processor import Processor
from convobot.workflow.Pipeline import Pipeline

class SubProcessor1(Processor):
    """
    Dummy Processor subclass to test the ProcessorLoader.
    """

    def __init__(self, name, cfg) -> None:
        super().__init__(name, cfg)
        self._index = cfg['config']['start-idx']

    def process(self):
        self._index += 1

    @property
    def index(self):
        return self._index

class SubProcessor2(Processor):
    """
    Dummy Processor subclass to test the ProcessorLoader.
    """

    def __init__(self, name, cfg) -> None:
        super().__init__(name, cfg)

        self._index = cfg['config']['start-idx']

    def process(self):
        self._index += 1

    @property
    def index(self):
        return self._index


class TestPipeline(TestCase):
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
            "global": {},
            "dir-paths": {
                "simulated": "simulated",
                "manipulated": "manipulated"
            },
            "stages": {
                "stage1": {
                    "processor": {
                      "type": "generator",
                      "module": "test.convobot.workflow.test_pipeline",
                      "class": "SubProcessor1",
                      "dst-id": "simulated"
                    },
                    "config": {
                        "start-idx": 100
                    }
                },
                "stage2": {
                    "processor": {
                      "type": "transformer",
                      "module": "test.convobot.workflow.test_pipeline",
                      "class": "SubProcessor2",
                      "src-id": "simulated",
                      "dst-id": "manipulated"
                    },
                    "config": {
                        "start-idx": 200
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
        Test that the pipeline can load the SubProcessors
        :return:
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-s', 'stage1',
                '-s', 'stage2']

        self._write_cfg(self._sim_cfg)

        global_cfg_mgr = GlobalCfgMgr(argv)

        pipeline = Pipeline(global_cfg_mgr)
        pipeline.process()

        self.assertEqual(101, pipeline._pipeline[0].index, 'SubProcessor1')
        self.assertEqual(201, pipeline._pipeline[1].index, 'SubProcessor2')