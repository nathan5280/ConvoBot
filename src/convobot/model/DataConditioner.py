import numpy as np

class DataConditioner(object):
    def __init__(self, img_size, color_layers, add_xy=False):
        self._add_xy = add_xy
        self._img_size = img_size
        self._img_color_layers = color_layers

    def condition_labels(self, labels):
        print('Condition labels')
        return labels

    def condition_images(self, images):
        print('Condition images')
        images = images.astype('float32')/255
        return images

    def reshape_images(self, images):
        images = images.reshape(images.shape[0], self._img_size[0],
                                self._img_size[1], self._img_color_layers)
        return images
