from PIL import Image
import os, re
import numpy as np
from convobot.util.TreeUtil import TreeUtil
from convobot.transformer.Transformer import Transformer

class StereoStacker(Transformer):
    def __init__(self, cfg_mgr, transform_index, verbose=False):
        super(StereoStacker, self).__init__(cfg_mgr, transform_index, verbose)

        self._img_size = self._cfg_mgr.get_cfg()['Environment']['ImageSize']

        if self._verbose:
            print('Loading StereoStacker Transfomer')

    def process(self):
        print(self._input_path, self._output_path)

        def converter(src_path, dst_path, filename):
            left_path = src_path
            right_path = re.sub('\/left', '', src_path)

            # Convert from RGBA to RGB
            img_l = Image.open(os.path.join(left_path, filename)).convert('RGB')
            img_r = Image.open(os.path.join(right_path, filename)).convert('RGB')

            # convert to np.array, concatentate (stack) them on top of each other
            # and convert back to PIL image.
            npl = np.array(img_l)
            npr = np.array(img_r)
            nps = np.concatenate((npl, npr), axis=0)
            img_stk = Image.fromarray(nps)
            img = img_stk.resize((self._img_size[0], self._img_size[1]))

            img.save(os.path.join(dst_path, filename))
            # print('Converting: {}, {}'.format(os.path.join(src_path, filename), os.path.join(dst_path, filename)))

        self._tree_util.apply_files(converter, '*.png')
