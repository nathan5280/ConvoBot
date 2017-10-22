import logging

from convobot.processor.Processor import Processor

logger = logging.getLogger(__name__)

class NumpyManipulator(Processor):
    def __init__(self, name, cfg):
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)

    def process(self):
        logger.info('Processing: %s', self._name)