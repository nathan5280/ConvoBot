'''
Access all files in the environment in a consistent manner.
'''
import os, json

home_path = os.environ['HOME']
sim_path = 'simulation'
image_path = 'images'
model_path = 'models'
file_ext = '.json'
label_filename = 'label.pkl'
image_filename = 'image.pkl'

verbose = True

class Environment(object):
    def __init__(self, root):
        self._root = root

    def get_simulation_cfg(self, config_name):
        path = os.path.join(home_path, self._root, sim_path, config_name) + file_ext
        with open(path, 'r') as f:
            cfg = json.load(f)

        if verbose:
            print('Simulation Configuration:')
            print(json.dumps(cfg, indent=4))

        return cfg

    def get_simulation_output_path(self, cfg):
        name = cfg['name']
        path = os.path.join(home_path, self._root, sim_path, name)
        return path

    def get_processing_cfg(self, config_name):
        path = os.path.join(home_path, self._root, image_path, config_name) + file_ext
        with open(path, 'r') as f:
            cfg = json.load(f)

        if verbose:
            print('Processing Configuration:')
            print(json.dumps(cfg, indent=4))

        return cfg

    def get_processing_path(self, cfg):
        src = cfg['src_dataset']
        src_path = os.path.join(home_path, self._root, sim_path, src)

        name = cfg['name']
        dest_path = os.path.join(home_path, self._root, image_path, name)

        return src_path, dest_path

    def get_np_array_path(self, cfg):
        name = cfg['name']
        dest_path = os.path.join(home_path, self._root, image_path, name)
        label_file_path = os.path.join(dest_path, label_filename)
        image_file_path = os.path.join(dest_path, image_filename)
        return label_file_path, image_file_path

    def get_model_cfg(self, model_name, config_name):
        self._model_name = model_name
        path = os.path.join(home_path,
                self._root, model_path, model_name, config_name) + file_ext
        with open(path, 'r') as f:
            cfg = json.load(f)

        if verbose:
            print('Model Configuration:')
            print(json.dumps(cfg, indent=4))

        return cfg

    def get_model_name(self, cfg):
        path = os.path.join(home_path, self._root, model_path,
                    self._model_name, cfg['name'], cfg['model_filename'])
        return path

    def get_model_data_path(self, cfg):
        img_set_name = cfg['image_set_name']
        src_path = os.path.join(home_path, self._root, image_path, img_set_name)
        src_label_filename = os.path.join(src_path, label_filename)
        src_image_filename = os.path.join(src_path, image_filename)
        data_path = os.path.join(home_path, self._root, model_path,
                    self._model_name, cfg['name'])

        return src_label_filename, src_image_filename, data_path

    def get_tensorboard_path(self, cfg):
        tb_path = os.path.join(home_path, self._root, model_path,
                    self._model_name, cfg['name'], cfg['tensorboard'])
        return tb_path
