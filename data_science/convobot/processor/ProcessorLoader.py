import logging
import importlib

from convobot.processor.Processor import Processor

logger = logging.getLogger(__name__)


class ProcessorLoader(object):
    """
    Dynamically load Processors based on the module and class name in the configuration.
    """

    @staticmethod
    def load(name, cfg) -> Processor:
        """
        Load the processor based on the configuration.
        :param name: Name of the processor.
        :param cfg: Processor configuration.
        :return:
        """

        # Load the module by name
        logger.debug('Loading Processor: %s: %s',name, cfg['configuration']['module'])
        mod_name = cfg['configuration']['module']
        mod = importlib.import_module(mod_name)
        logger.debug('Done Loading Processor: %s: %s',name, cfg['configuration']['module'])

        # Get the class definition
        cls = getattr(mod, cfg['configuration']['class'])

        # Instantiate the class
        processor = cls(name, cfg)

        return processor
