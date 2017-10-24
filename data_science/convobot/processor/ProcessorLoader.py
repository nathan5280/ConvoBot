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
        print(cfg['configuration']['module'])
        mod = importlib.import_module(cfg['configuration']['module'])

        # Get the class definition
        cls = getattr(mod, cfg['configuration']['class'])

        # Instantiate the class
        processor = cls(name, cfg)

        return processor
