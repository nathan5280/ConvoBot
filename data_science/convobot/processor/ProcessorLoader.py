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
        :param cfg: Processor configuration.
        :return:
        """

        # Load the module by name
        print(cfg['processor']['module'])
        mod = importlib.import_module(cfg['processor']['module'])

        # Get the class definition
        cls = getattr(mod, cfg['processor']['class'])

        # Instantiate the class
        processor = cls(name, cfg)

        return processor
