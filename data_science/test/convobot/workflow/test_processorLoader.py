from unittest import TestCase
from convobot.processor.Processor import Processor
from convobot.processor.ProcessorLoader import ProcessorLoader


class SubProcessor(Processor):
    """
    Dummy Processor subclass to test the ProcessorLoader.
    """

    def __init__(self, name, cfg) -> None:
        super().__init__(name, cfg)

    def process(self):
        pass


class TestProcessorLoader(TestCase):
    """
    Smoke test the dynamic processor loader.
    """
    sim_cfg = \
        {
            "processor": {
                "type": "transformer",
                "module": "test.convobot.workflow.test_processorLoader",
                "class": "SubProcessor",
                "src-id": "simulated",
                "dst-id": "manipulated",
                "src-dir-path": "tmp/data/simulated",
                "dst-dir-path": "tmp/data/manipulated",
                "tmp-dir-path": "tmp/data/tmp"
            },
            "config": {}
        }

    def test_loader(self):
        """
        Dynamically load a SubProcessor class
        """
        processor = ProcessorLoader.load('processor1', self.sim_cfg)

        self.assertEqual('SubProcessor', processor.__class__.__name__, 'name')
