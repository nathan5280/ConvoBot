from convobot.processor.predictors.Predictor import Predictor


class StandalonePredictor(Predictor):
    def __init__(self, name: str, cfg) -> None:
        super().__init__(name, cfg)
