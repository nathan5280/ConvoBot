import logging
import unittest
from typing import Dict

from convobot.configuration.CmdLineCfgMgr import CmdLineCfgMgr
from convobot.util.load_logging_cfg import load_logging_cfg

load_logging_cfg('./logging-cfg.json')
logger = logging.getLogger(__name__)


class TestCmdLineCfgMgr(unittest.TestCase):
    """
    Test cases for the command configuration manager.  Objective is to
    insure that the parser is populating the correct fields in the configuration
    dictionary.
    """

    def test_all_parse(self):
        """
        Check to make sure that passing multiple stage-ids generates a list.
        :return:
        """
        argv = ['-d', 'data-dir-path',
                '-c', 'cfg-file-path',
                '-p', 'simulate',
                '-p', 'manipulate']
        parser = CmdLineCfgMgr()
        config: Dict[str, str] = parser.parse(argv)

        self.assertEqual('data-dir-path', config['data-dir-path'], 'data-dir-path')
        self.assertEqual('cfg-file-path', config['cfg-file-path'], 'cfg-file-path')
        self.assertEqual(2, len(config['process-stage-ids']), 'len process-stage-ids')
        self.assertEqual('simulate', config['process-stage-ids'][0], 'process-stage-id[0]')
        self.assertEqual('manipulate', config['process-stage-ids'][1], 'process-stage-id[1]')


if __name__ == '__main__':
    unittest.main()
