import logging
import glob
from typing import List

import os

from convobot.processor.Processor import Processor

logger = logging.getLogger(__name__)


class ProcessorPipeline(object):
    """
    Process the stages specified in the configuration.
    """
    def __init__(self, tmp_dir_path: str) -> None:
        """
        Construct the Processor Pipeline.

        :param tmp_dir_path: Temporary data path that needs to be cleaned before processing.
        :return: None
        """
        # List of Processors in the pipeline.
        self._tmp_dir_path: str = tmp_dir_path
        self._pipeline: List[Processor] = []

    def add_processor(self, processor: Processor) -> None:
        """
        Add a processor to the end of the pipeline.
        :param processor: Processor to add.
        :return: None
        """
        self._pipeline.append(processor)

    def process(self):
        """
        Run the stages
        :return: None
        """
        for processor in self._pipeline:
            # Clear the temporary directory.
            files = glob.glob(os.path.join(self._tmp_dir_path, '*'))
            for file in files:
                os.remove(file)

            processor.process()
