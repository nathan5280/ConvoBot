from convobot.transformer.StereoStacker import StereoStacker
from convobot.transformer.ColorConverter import ColorConverter
# from convobot.transformer.ImageCounter import ImageCounter
# from convobot.transformer.ImageToNumpy import ImageToNumpy
# from convobot.workflow.ConfigurationManager import ConfigurationManager

# transformers = {'stereo-stacker': StereoStacker, 'color-converter': ColorConverter,
#                 'counter': ImageCounter, 'image-to-nparray': ImageToNumpy}
transformers = {'stereo-stacker': StereoStacker, 'color-converter': ColorConverter}

class TransformerLoader(object):
    def __init__(self, cfg_mgr, transform_index, verbose=False):
        self._cfg_mgr = cfg_mgr
        self._cfg = cfg_mgr.get_cfg()
        self._verbose = verbose
        self._transform_index = transform_index

    def get_transformer(self):
        name = self._cfg['Transformer']['TransformerName']

        if self._verbose:
            print('Loading transformer: ', name)

        return transformers[name](self._cfg_mgr, self._transform_index)
