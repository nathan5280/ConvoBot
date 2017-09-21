from convobot.imageprocessor.ColorToGrayScale import ColorToGrayScale
from convobot.imageprocessor.ImageToNumpy2 import ImageToNumpy
import pickle
import os
import pandas as pd

root_path = '../../../datax'
raw_path = os.path.join(root_path, 'raw')
processed_path = os.path.join(root_path, 'gs_28x28')
label_file_path = os.path.join(root_path, 'gs_28x28_lable.pkl')
image_file_path = os.path.join(root_path, 'gs_28x28_image.pkl')

def main():
    converter = ColorToGrayScale(raw_path, processed_path, (28, 28))
    converter.process()

    converter = ImageToNumpy(processed_path, processed_path)
    converter.process()
    label, image = converter.get_data()

    with open(label_file_path, 'wb') as f:
        pickle.dump(label, f)

    with open(image_file_path, 'wb') as f:
        pickle.dump(image, f)

if __name__ == '__main__':
    main()
