import os
import shutil
import numpy as np
from unittest import TestCase

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.processor.manipulator.CountManipulator import CountManipulator
from convobot.util.load_logging_cfg import load_logging_cfg
from convobot.workflow.CfgPipeline import CfgPipeline

load_logging_cfg('./logging-cfg.json')

class TestSplitManipulator(TestCase):
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
                '-p', 'cartesian',
                '-p', 'split']

        global_cfg_mgr = GlobalCfgMgr(argv)

        # Create the pipeline of the three animation processors and execute them.
        pipeline = CfgPipeline(global_cfg_mgr)
        pipeline.process()

        # build the split file names.
        train_label_file_path = os.path.join(self._data_dir_path, 'modeled', 'train-label.npy')
        self.assertTrue(os.path.exists(train_label_file_path))
        arr = np.load(train_label_file_path)
        self.assertEqual((149, 3), arr.shape, 'train-label')

        train_image_file_path = os.path.join(self._data_dir_path, 'modeled', 'train-image.npy')
        self.assertTrue(os.path.exists(train_image_file_path))
        arr = np.load(train_image_file_path)
        self.assertEqual((149,16,16,3), arr.shape, 'train-image')

        test_label_file_path = os.path.join(self._data_dir_path, 'modeled', 'test-label.npy')
        self.assertTrue(os.path.exists(test_label_file_path))

        test_image_file_path = os.path.join(self._data_dir_path, 'modeled', 'test-image.npy')
        self.assertTrue(os.path.exists(test_image_file_path))

        validation_label_file_path = os.path.join(self._data_dir_path, 'modeled', 'validation-label.npy')
        self.assertTrue(os.path.exists(validation_label_file_path))

        validation_image_file_path = os.path.join(self._data_dir_path, 'modeled', 'validation-image.npy')
        self.assertTrue(os.path.exists(validation_image_file_path))
