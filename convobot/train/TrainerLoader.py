import logging
from convobot.util.CfgMgr import CfgMgr
from convobot.train.TrackingTrainer import TrackingTrainer

logger = logging.getLogger(__name__)
trainers = {'tracking-trainer': TrackingTrainer}

class TrainerLoader(object):
    def __init__(self, cfg_mgr):
        logger.debug('Initializing')
        self._cfg_mgr = cfg_mgr
        self._cfg = self._cfg_mgr.get_train_cfg()

    def get_trainer(self):
        name = self._cfg['Trainer']['Name']
        logger.debug('Loading trainer: %s', name)
        return trainers[name](self._cfg_mgr)
