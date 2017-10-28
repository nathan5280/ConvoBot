from convobot.model import ModelMgr
from convobot.processor.manipulator import SplitDataMgr
from convobot.processor.predictors.Predictor import Predictor


class TrainPredictor(Predictor):
    def __init__(self, name: str, cfg, model, split_data_mgr: SplitDataMgr) -> None:
        super().__init__(name, cfg)
        self._model = model
        self._split_data_mgr = split_data_mgr
