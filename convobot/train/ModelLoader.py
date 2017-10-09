import logging
from convobot.train.ConvoBot1Model import ConvoBot1Model
from convobot.train.ConvoBot2Model import ConvoBot2Model

logger = logging.getLogger(__name__)
models = {'convobot1': ConvoBot1Model,
          'convobot2': ConvoBot2Model}

class ModelLoader(object):
    '''
    Dynamically access the model builder.
    '''

    def __init__(self, cfg_mgr):
        '''
        Args:
            cfg_mgr: Global configuration manager.
        '''
        logger.debug("Initializing")
        self._cfg_mgr = cfg_mgr
        self._cfg = cfg_mgr.get_train_cfg()

    def get_model_builder(self):
        '''
        Get the model builder.

        returns: model builder for the model specified in the configuration.
        '''
        name = self._cfg['Model']['Name']
        logger.debug('Loading model %s', name)
        return models[name](self._cfg_mgr)
