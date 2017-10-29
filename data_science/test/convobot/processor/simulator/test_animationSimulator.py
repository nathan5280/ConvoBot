import os
import shutil
import json
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.util.load_logging_cfg import load_logging_cfg
from convobot.workflow.CfgPipeline import CfgPipeline

load_logging_cfg('./logging-cfg.json')


class TestAnimationSimulator(TestCase):
    """
    Smoke tests for the AnimationSimulator.
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
        shutil.copy('./test/convobot/animation_test_cfg.json', self._cfg_file_path)

    def tearDown(self):
        """
        Remove any directories that a single test created.
        """
        shutil.rmtree(self._data_dir_path)

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

        global_cfg_mgr = GlobalCfgMgr(argv)

        # Create the pipeline of the three animation processors and execute them.
        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        # Simple test to see if the three gif files were creates.
        animated_files = os.listdir(os.path.join(self._data_dir_path, 'animated'))
        self.assertTrue('alpha.gif' in animated_files, 'alpha.gif')
        self.assertTrue('theta.gif' in animated_files, 'theta.gif')
        self.assertTrue('radius.gif' in animated_files, 'radius.gif')