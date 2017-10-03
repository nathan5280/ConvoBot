from convobot.model.ConvoBotModel import ConvoBotModel

models = {'convobot1': ConvoBotModel}

class ModelBuilderLoader(object):
    def __init__(self, cfg_mgr, predict=False, verbose=False):
        self._cfg_mgr = cfg_mgr
        self._cfg = cfg_mgr.get_cfg()
        self._verbose = verbose
        self._predict = predict

    def get_model_builder(self):
        name = self._cfg['Model']['ModelName']

        if self._verbose:
            print('Loading model: ', name)

        return models[name](self._cfg_mgr, self._predict, self._verbose)
