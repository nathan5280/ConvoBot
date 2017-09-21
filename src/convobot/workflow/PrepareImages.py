from convobot.imageprocessor.ColorToGrayScale import ColorToGrayScale
from convobot.imageprocessor.ImageCounter import ImageCounter
from convobot.imageprocessor.ImageToNumpy import ImageToNumpy
import pickle
import os
import pandas as pd

# root_path = '../../../datax'
root_path = '../../../dataf'
raw_path = os.path.join(root_path, 'raw')
processed_path = os.path.join(root_path, 'gs_28x28')
label_file_path = os.path.join(root_path, 'gs_28x28_lable.pkl')
image_file_path = os.path.join(root_path, 'gs_28x28_image.pkl')

c2g = True
cnt = False
i2n = True

def main():

    if c2g:
        converter = ColorToGrayScale(raw_path, processed_path, (28, 28))
        converter.process()

    if cnt:
        converter = ImageCounter(processed_path, processed_path)
        converter.process()
        img_cnt = converter.get_count()
        print('Images in dataset: ', img_cnt)

    if i2n:
        converter = ImageToNumpy(processed_path, processed_path)
        converter.process()
        label, image = converter.get_data()

        with open(label_file_path, 'wb') as f:
            pickle.dump(label, f)

        with open(image_file_path, 'wb') as f:
            pickle.dump(image, f)

if __name__ == '__main__':
    main()
