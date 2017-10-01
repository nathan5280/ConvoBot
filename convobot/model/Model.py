class Model(object):
    def __init__(self, cfg_mgr, verbose=False):
        self._cfg_mgr = cfg_mgr

        self._model_cfg = cfg_mgr.get_cfg()['Model']
        self._verbose = verbose

        input_dir_name = self._model_cfg['InputDirName']
        output_dir_name = self._model_cfg['OutputDirName']

        self._input_path = cfg_mgr.get_absolute_path(input_dir_name)
        self._output_path = cfg_mgr.get_absolute_path(output_dir_name)
