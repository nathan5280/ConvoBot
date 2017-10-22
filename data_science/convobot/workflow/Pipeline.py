import logging
from typing import List

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.processor.Processor import Processor
from convobot.processor.ProcessorLoader import ProcessorLoader

logger = logging.getLogger(__name__)


class Pipeline(object):
    """
    Process the stages specified in the configuration.
    """
    def __init__(self, global_cfg_mgr: GlobalCfgMgr) -> None:
        """

        :param global_cfg_mgr: Global configuration manager used to access
        the list of stages to process and their configurations.
        """
        self._global_cfg_mgr : GlobalCfgMgr = global_cfg_mgr

        # Build the pipeline from configurations.
        self._pipeline : List[Processor] = [None] * len(self._global_cfg_mgr.stage_names)
        for i, stage_name in enumerate(self._global_cfg_mgr.stage_names):
            stage_cfg = self._global_cfg_mgr.stage_cfg(stage_name)
            processor = ProcessorLoader.load(stage_name, stage_cfg)
            self._pipeline[i] = processor

    def process(self):
        """
        Run the stages
        :return: None
        """
        for processor in self._pipeline:
            self._global_cfg_mgr.clear_tmp()
            processor.process()
