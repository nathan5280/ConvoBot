from convobot.util.TreeUtil import TreeUtil

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

class Transformer(object):
    def __init__(self, cfg_mgr, transform_index, verbose=False):
        self._cfg_mgr = cfg_mgr
        self._transform_index = transform_index

        self._transform_cfg = cfg_mgr.get_cfg()['Transformer']['Pipeline'][transform_index]
        self._verbose = verbose

        input_dir_name = self._transform_cfg['InputDirName']
        output_dir_name = self._transform_cfg['OutputDirName']

        self._input_path = cfg_mgr.get_absolute_path(input_dir_name)
        self._output_path = cfg_mgr.get_absolute_path(output_dir_name)
        self._tree_util = TreeUtil(self._input_path, self._output_path)
