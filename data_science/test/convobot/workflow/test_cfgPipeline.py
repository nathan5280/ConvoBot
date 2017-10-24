import os
import json
import shutil
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.processor.Processor import Processor
from convobot.util.load_logging_cfg import load_logging_cfg
from convobot.workflow.CfgPipeline import CfgPipeline

load_logging_cfg('./logging-cfg.json')

swept = False
reset = False

class SubProcessor1(Processor):
    """
    Dummy Processor subclass to test the ProcessorLoader.
    """

    def __init__(self, name, cfg) -> None:
        """
        Construct the SubProcessor
        :param name: Name of the Processor stage
        :param cfg: Processor configuration
        """
        super().__init__(name, cfg)

        # Get a dummy variable out of the configuration that can be checked in the test.
        self._index = cfg['parameters']['start-idx']

    def sweep(self):
        """
        Sweep the files that aren't needed for the next stage.
        :return: None
        """
        super().sweep()
        global swept
        swept = True

    def reset(self):
        """
        Reset the files that aren't needed for the next stage.
        :return: None
        """
        super().reset()
        global reset
        reset = True

    def process(self):
        """
        Concrete implementation of the process method.  Do something simple that
        can be check in the test.
        :return: None
        """
        self._index += 1

    @property
    def index(self):
        """
        Access the internal state for a check in the test.
        :return: The current index of the class.
        """
        return self._index


class SubProcessor2(Processor):
    """
    Dummy Processor subclass to test the ProcessorLoader.
    """

    def __init__(self, name, cfg) -> None:
        """
        Construct the SubProcessor
        :param name: Name of the Processor stage
        :param cfg: Processor configuration
        """
        super().__init__(name, cfg)

        # Get a dummy variable out of the configuration that can be checked in the test.
        self._index = cfg['parameters']['start-idx']

    def process(self):
        """
        Concrete implementation of the process method.  Do something simple that
        can be check in the test.
        :return: None
        """
        self._index += 1

    @property
    def index(self):
        """
        Access the internal state for a check in the test.
        :return: The current index of the class.
        """
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
    _cfg = \
        {
            "global": {},
            "dir-paths": {
                "simulated": "simulated",
                "manipulated": "manipulated"
            },
            "stages": {
                "stage1": {
                    "configuration": {
                        "module": "test.convobot.workflow.test_cfgPipeline",
                        "class": "SubProcessor1",
                        "dirs": {
                            "dst-id": "simulated"
                        },
                    },
                    "parameters": {
                        "start-idx": 100
                    }
                },
                "stage2": {
                    "configuration": {
                        "module": "test.convobot.workflow.test_cfgPipeline",
                        "class": "SubProcessor2",
                        "dirs": {
                            "src-id": "simulated",
                            "dst-id": "manipulated"
                        },
                    },
                    "parameters": {
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
        self._write_cfg(self._cfg)

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

    def test_sweep_reset(self):
        """
        Test that the pipeline can load the SubProcessors
        :return:
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-s', 'stage1',
                '-r', 'stage1']

        global_cfg_mgr = GlobalCfgMgr(argv)

        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        global swept
        self.assertTrue(swept, 'Swept')
        global reset
        self.assertTrue(reset, 'Reset')

    def test_process(self):
        """
        Test that the pipeline can load the SubProcessors
        :return:
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-p', 'stage1',
                '-p', 'stage2']

        global_cfg_mgr = GlobalCfgMgr(argv)

        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        self.assertEqual(101, pipeline._pipeline[0].index, 'SubProcessor1')
        self.assertEqual(201, pipeline._pipeline[1].index, 'SubProcessor2')
