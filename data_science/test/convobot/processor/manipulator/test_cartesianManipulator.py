import os
import shutil
import json
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.processor.manipulator.CountManipulator import CountManipulator
from convobot.util.load_logging_cfg import load_logging_cfg
from convobot.workflow.CfgPipeline import CfgPipeline

load_logging_cfg('./logging-cfg.json')

class TestCartesianManipulator(TestCase):
    """
    Smoke tests for the NumpySimulator.
    """
    _tmp_dir_path = 'tmp'
    _data_dir_path = os.path.join(_tmp_dir_path, 'data')
    _cfg_file_path = os.path.join(_tmp_dir_path, 'config.json')

    @classmethod
    def setUpClass(cls):
        """
        Create a test temporary directory that is used for all of the tests in this class.
        :return: None
        """
        if not os.path.exists(cls._tmp_dir_path):
            print('Creating tmp')
            os.mkdir(cls._tmp_dir_path)

    @classmethod
    def tearDownClass(cls):
        """
        Remove the test temporary directory to clean things up.
        :return: None
        """
        if os.path.exists(cls._tmp_dir_path):
            print('Removing tmp')
            shutil.rmtree(cls._tmp_dir_path)

    def setUp(self):
        shutil.copy('./test/convobot/base_test_cfg.json', self._cfg_file_path)

    def tearDown(self):
        """
        Remove any directories that a single test created.
        """
        shutil.rmtree(self._data_dir_path)

    def test_process(self):
        """
        Run simulation.
        :return:
        """
        argv = ['-d', self._data_dir_path,
                '-c', self._cfg_file_path,
                '-p', 'simulate',
                '-p', 'manipulate',
                '-p', 'cartesian']

        global_cfg_mgr = GlobalCfgMgr(argv)

        # Create the pipeline of the three animation processors and execute them.
        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        xy_label_file_path = os.path.join(self._data_dir_path, 'manipulated', 'full-xy-label.npy')
        self.assertTrue(os.path.exists(xy_label_file_path), 'image exists')
        self.assertTrue(os.stat(xy_label_file_path).st_size>0, 'image size')
