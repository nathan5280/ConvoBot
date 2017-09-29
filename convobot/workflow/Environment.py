'''
Access all files in the environment in a consistent manner.
'''
import os, json

home_path = os.environ['HOME']
sim_path = 'simulation'
image_path = 'images'
model_path = 'models'
result_path = 'results'
file_ext = '.json'
label_filename = 'label.pkl'
image_filename = 'image.pkl'

verbose = True

class Environment(object):
    def __init__(self, cfg_root, data_root):
        self._data_root = data_root
        self._cfg_root = cfg_root
        self._cfg = None

    def get_simulation_cfg(self, config_name):
        path = os.path.join(self._cfg_root, sim_path, config_name) + file_ext
        with open(path, 'r') as f:
            self._cfg = json.load(f)

        if verbose:
            print('Simulation Configuration:')
            print(json.dumps(self._cfg, indent=4))

        return self._cfg

    def get_simulation_output_path(self):
        name = self._cfg['name']
        path = os.path.join(home_path, self._data_root, sim_path, name)
        return path

    def get_processing_cfg(self, config_name):
        path = os.path.join(self._cfg_root, image_path, config_name) + file_ext
        with open(path, 'r') as f:
            self._cfg = json.load(f)

        if verbose:
            print('Processing Configuration:')
            print(json.dumps(self._cfg, indent=4))

        return self._cfg

    def get_processing_path(self):
        src = self._cfg['src_dataset']
        src_path = os.path.join(home_path, self._data_root, sim_path, src)

        name = self._cfg['name']
        dest_path = os.path.join(home_path, self._data_root, image_path, name)

        return src_path, dest_path

    def get_np_array_path(self):
        name = self._cfg['name']
        dest_path = os.path.join(home_path, self._data_root, image_path, name)
        label_file_path = os.path.join(dest_path, label_filename)
        image_file_path = os.path.join(dest_path, image_filename)
        return label_file_path, image_file_path

    def get_model_cfg(self, model_name, config_name):
        self._model_name = model_name
        path = os.path.join(self._cfg_root,
                model_path, model_name, config_name) + file_ext
        with open(path, 'r') as f:
            self._cfg = json.load(f)

        if verbose:
            print('Model Configuration:')
            print(json.dumps(self._cfg, indent=4))

        return self._cfg

    def get_model_path(self):
        path = os.path.join(home_path, self._data_root, model_path,
                    self._model_name, self._cfg['name'], self._cfg['model_filename'])
        return path

    def get_result_path(self):
        filename = os.path.join(home_path, self._data_root, result_path,
                    self._model_name, self._cfg['name'], self._cfg['prediction_filename'])
        return filename

    def get_model_data_path(self):
        img_set_name = self._cfg['image_set_name']
        src_path = os.path.join(home_path, self._data_root, image_path, img_set_name)
        src_label_filename = os.path.join(src_path, label_filename)
        src_image_filename = os.path.join(src_path, image_filename)
        data_path = os.path.join(home_path, self._data_root, model_path,
                    self._model_name, self._cfg['name'])

        return src_label_filename, src_image_filename, data_path

    def get_tensorboard_path(self):
        tb_path = os.path.join(home_path, self._data_root, model_path,
                    self._model_name, self._cfg['name'], self._cfg['tensorboard'])
        return tb_path
