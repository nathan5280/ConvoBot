from convobot.util.TreeUtil import TreeUtil
from convobot.imageprocessor.LabelCollector import LabelCollector

class ThetaSorter(object):
    def __init__(self, src_path, pattern, theta_step, span_step, span_count, fmt):
        self._filenames = []
        self._src_path = src_path
        self._dst_path = '.'
        self._pattern = pattern
        self._theta_step = theta_step
        self._span_step = span_step
        self._span_count = span_count
        self._fmt = fmt
        self._tree_util = TreeUtil(self._src_path, self._dst_path)

    def generate_theta_list(self, theta):
        '''
        Generate a list of the angles included in a range.

        Input:
            theta: angle to build the list around.
            step: size of the step.
            count: number of steps.
            self._fmt: for the items in the list.

        Return:
            list of angles.
        '''
        values = sorted([theta + self._span_step * x for x in range(-self._span_count, self._span_count+1)])
        normalized_values = [0.0] * len(values)
        for i, value in enumerate(values):
            if value < 0:
                normalized_values[i] = 360 + value
            elif value >= 360:
                normalized_values[i] = value - 360
            else:
                normalized_values[i] = value
        string_values = [self._fmt.format(value) for value in normalized_values]
        return string_values

    def filename_theta_parser(filename):
        '''
        parse the filename for theta.
        '''
        return filename.split('_')[0]

    def collect_filenames(self):
        '''
        Generator of filenames that fit into each of the labeled groups.

        Return:
            tuple of (theta, files) where files is a tuple of (src_path, filename)
        '''
        for theta in range(0, 360, self._theta_step):
            print('Processing Theta: ', theta)
            values = self.generate_theta_list(theta)
            collector = LabelCollector(values, ThetaSorter.filename_theta_parser)
            self._tree_util.apply_files(collector.get_collector_funct(), self._pattern, copy_dir=False)
            yield (theta, collector.get_filenames())


def main():
    sorter = ThetaSorter('../../../datax/gs_28x28', '*.png', 90, 45, 2, '{:05.1f}')
    for file_set in sorter.collect_filenames():
        print(file_set[0], file_set[1][:3])


if __name__ == '__main__':
    main()
