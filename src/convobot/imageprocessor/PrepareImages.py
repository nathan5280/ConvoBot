from convobot.imageprocessor.ColorSizeConverter import ColorSizeConverter
from convobot.imageprocessor.ImageCounter import ImageCounter
from convobot.imageprocessor.ImageToNumpy import ImageToNumpy
from convobot.workflow.Environment import Environment
import pickle
import os
import pandas as pd
import sys, getopt

c2g = True
cnt = False
i2n = True

def process(dataset_name, config_name):
    # load the simulation configuration from the convobot environment.
    processing_env = Environment(dataset_name)
    cfg = processing_env.get_processing_cfg(config_name)

    src_path, dest_path = processing_env.get_processing_path(cfg)

    size = cfg['size']
    grayscale = not cfg['color']

    if c2g:
        target_size = None
        if cfg['resize']:
            target_size = size

        converter = ColorSizeConverter(src_path, dest_path,
                            grayscale=grayscale, resize=target_size)
        converter.process()

    if cnt:
        converter = ImageCounter(dest_path, dest_path)
        converter.process()
        img_cnt = converter.get_count()
        print('Images in dataset: ', img_cnt)

    if i2n:
        converter = ImageToNumpy(dest_path, dest_path, grayscale=grayscale, size=size)
        converter.process()
        label, image = converter.get_data()

        label_file_path, image_file_path = processing_env.get_np_array_path(cfg)
        print('Label: ', label.shape)
        print('Image: ', image.shape)

        with open(label_file_path, 'wb') as f:
            pickle.dump(label, f)

        with open(image_file_path, 'wb') as f:
            pickle.dump(image, f)

def main(argv):
    dataset_name = None
    config_name = None
    usage = 'PrepareImages.py -d <dataset_name> -c <config_name>'
    try:
        opts, args = getopt.getopt(argv,"hd:c:",["dataset_name=","config_name="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--dataset_name"):
            dataset_name = arg
        elif opt in ("-c", "--config_name"):
            config_name = arg

    if not dataset_name or not config_name:
        print(usage)
    else:
        process(dataset_name, config_name)

if __name__ == "__main__":
    main(sys.argv[1:])
