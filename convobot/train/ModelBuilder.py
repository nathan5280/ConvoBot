import logging

logger = logging.getLogger(__name__)

class ModelBuilder(object):
    def __init__(self, cfg_mgr):
        logger.debug('Initialize')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_train_cfg()
        self._image_size = self._cfg['Image']['Size']
        self._channels = self._cfg['Image']['Channels']
        self._model = None

    def save_model(self):
        logger.info('Saving model')
        self._model.save(self._model_path)
