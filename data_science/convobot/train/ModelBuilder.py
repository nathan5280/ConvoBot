import logging

logger = logging.getLogger(__name__)

class ModelBuilder(object):
    '''
    Base class for all the model builders.  This class provides access to
    the global configuration manager, model configuration and common configuration
    items.
    '''

    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: Global configuration manager.
        '''
        logger.debug('Initialize')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_train_cfg()
        self._image_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']
        self._model = None

    def save_model(self):
        '''
        Persist the model to disk.
        '''
        logger.info('Saving model')
        self._model.save(self._model_path)
