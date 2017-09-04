from convobot.imageprocessor.ColorToGrayScale import ColorToGrayScale
from convobot.imageprocessor.ThetaSorter import ThetaSorter
from convobot.imageprocessor.FileLinker import FileLinker

def main():
    converter = ColorToGrayScale('../../../datax/raw', '../../../datax/gs_28x28', (28, 28))
    converter.process()

    sorter = ThetaSorter('../../../datax/gs_28x28', '*.png', 90, 45, 2, '{:05.1f}')
    linker = FileLinker('../../../datax/theta', sorter)
    linker.process()

if __name__ == '__main__':
    main()
