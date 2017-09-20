from convobot.imageprocessor.ColorToGrayScale import ColorToGrayScale
from convobot.imageprocessor.ImageCounter import ImageCounter
# from convobot.imageprocessor.ThetaSorter import ThetaSorter
# from convobot.imageprocessor.FileLinker import FileLinker

raw_path = '../../../datax/raw'
processed_path = '../../../datax/gs_28x28'

def main():
    converter = ColorToGrayScale(raw_path, processed_path, (28, 28))
    converter.process()

    converter = ImageCounter(processed_path, processed_path)
    converter.process()
    print('Images Found: ', converter.get_count())

    # sorter = ThetaSorter('../../../datax/gs_28x28', '*.png', 90, 45, 2, '{:05.1f}')
    # linker = FileLinker('../../../datax/theta', sorter)
    # linker.process()

if __name__ == '__main__':
    main()
