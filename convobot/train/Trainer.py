import logging
import json

logger = logging.getLogger(__name__)

# TODO: Make this an abstract base class.
# TODO: Consider moving the SimulatorLoaer functionality in to this class as
# static class method.


class Trainer(object):
    '''
    Base class for trainers.  Provide access to the configuration information.
    '''

    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: Global configuration manager.
        '''
        
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_train_cfg()

        logger.debug(json.dumps(self._cfg, indent=4))

        self._image_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']

    # TODO: Implement abstract method
    # def process(self)
