import logging
from typing import List

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr
from convobot.processor.Processor import Processor
from convobot.processor.ProcessorLoader import ProcessorLoader
from convobot.workflow.ProcessorPipeline import ProcessorPipeline

logger = logging.getLogger(__name__)


class CfgPipeline(ProcessorPipeline):
    """
    Process the stages specified in the configuration.
    """

    def __init__(self, global_cfg_mgr: GlobalCfgMgr) -> None:
        """
        Construct all the Processors and add them to the Pipeline.
        Run any sweep and reset methods specified on the command line.

        :param global_cfg_mgr: Global configuration manager used to access
        the list of stages to process and their configurations.
        """
        super().__init__(global_cfg_mgr.tmp_dir_path)
        self._global_cfg_mgr: GlobalCfgMgr = global_cfg_mgr

        # Build all the processors that have some action.
        processors = dict()
        for stage_name in self._global_cfg_mgr.sweep_stages:
            self._get_processor(processors, stage_name).sweep()

        for stage_name in self._global_cfg_mgr.reset_stages:
            self._get_processor(processors, stage_name).reset()

        # Build the processor pipeline.
        for stage_name in self._global_cfg_mgr.process_stages:
            processor = self._get_processor(processors, stage_name)
            self.add_processor(processor)

    def _get_processor(self, processors, stage_name):
        """
        Return the processor from the processors dictionary if it exists or create it.

        :param processors: Dictionary of all currrently loaded processors.
        :param stage_name: Stage name for the processor.
        :return: Processor
        """
        if stage_name not in processors:
            stage_cfg = self._global_cfg_mgr.stage_cfg(stage_name)
            processor = ProcessorLoader.load(stage_name, stage_cfg)
            processors[stage_name] = processor

        return processors[stage_name]
