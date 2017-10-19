import unittest

from convobot.environment.CmdLineCfgMgr import CmdLineCfgMgr


class TestCmdLineCfgMgr(unittest.TestCase):
    def test_all_parse(self):
        argv = ['-d', 'data-dir-path',
                '-c', 'cfg-file-path',
                '-s',
                '-a',
                '-m',
                '-t',
                '-r',
                '-b']
        parser = CmdLineCfgMgr(argv)
        arg_dict = parser.cfg_dict

        self.assertEqual('data-dir-path', arg_dict['DataDirPath'], 'DataDirPath')
        self.assertEqual('cfg-file-path', arg_dict['CfgFilePath'], 'CfgFilePath')
        self.assertTrue(arg_dict['RunSimulation'], 'RunSimulation')
        self.assertTrue(arg_dict['RunAnimation'], 'RunAnimation')
        self.assertTrue(arg_dict['RunManipulation'], 'RunManipulation')
        self.assertTrue(arg_dict['RunTraining'], 'RunTraining')
        self.assertTrue(arg_dict['RunReporting'], 'RunReporting')
        self.assertTrue(arg_dict['BuildDirs'], 'BuildDirs')

    def test_default_parse(self):
        argv = ['-d', 'data-dir-path',
                '-c', 'cfg-file-path']

        parser = CmdLineCfgMgr(argv)
        arg_dict = parser.cfg_dict

        self.assertEqual('data-dir-path', arg_dict['DataDirPath'], 'DataDirPath')
        self.assertEqual('cfg-file-path', arg_dict['CfgFilePath'], 'CfgFilePath')
        self.assertFalse(arg_dict['RunSimulation'], 'RunSimulation')
        self.assertFalse(arg_dict['RunAnimation'], 'RunAnimation')
        self.assertFalse(arg_dict['RunManipulation'], 'RunManipulation')
        self.assertFalse(arg_dict['RunTraining'], 'RunTraining')
        self.assertFalse(arg_dict['RunReporting'], 'RunReporting')
        self.assertFalse(arg_dict['BuildDirs'], 'BuildDirs')


if __name__ == '__main__':
    unittest.main()

