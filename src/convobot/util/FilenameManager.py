import os

class FilenameManager(object):
    '''Consistently handle the conversion of labels and filenames across ConvoBot modules'''
    def __init__(self, separator='_', extension='png'):
        self._separator = separator
        self._extension = extension

    def label_to_filename(self, theta, radius, alpha):
        '''Encode label information in filenames.

        Args:
          theta: The angle from X-axis
          radius: The radiaus from center
          alpha: The camera angle relative to theta

        Returns:
          filename: The encoded filename.

        '''
        return '{:05.1f}{}{:04.1f}{}{:03.0f}.{}'\
                .format(theta, self._separator, radius, self._separator, alpha, self._extension)

    def label_to_path(self, path, theta, radius, alpha):
        '''Encode label information in path and filenames.

        Args:
          path: The path for the filename
          theta: The angle from X-axis
          radius: The radiaus from center
          alpha: The camera angle relative to theta

        Returns:
          path: The encoded path and filename.

        '''
        return os.path.join(path, self.label_to_filename(theta, radius, alpha))

    def label_to_radius_path(self, path, theta, radius, alpha):
        '''Encode label information in path, radius, filenames.

        Args:
          path: The path for the filename
          theta: The angle from X-axis
          radius: The radiaus from center
          alpha: The camera angle relative to theta

        Returns:
          path: The encoded path and filename.

        '''
        return os.path.join(path, '{:04.1f}'.format(radius), self.label_to_filename(theta, radius, alpha))

    def filename_to_labels(self, filename):
        '''Decode the labels from the filename.

        Args:
          filename:
                The filename to decode

        Returns:
          theta, radius, alpha:

        '''
        theta, radius, alpha = filename[:-len(self._extension)-1].split(self._separator)
        return theta, radius, alpha

    def filename_to_theta(self, filename):
        '''
        Decode theta from filename

        Args:
          filename:
                The filename to decode

        Returns:
            theta:
                The angle from X-axis

        '''
        theta, _, _ = self.filename_to_labels(filename)
        return theta

    def filename_to_radius(self, filename):
        '''
        Decode the radius from the filename

        Args:
          filename:
                The filename to decode
        Returns:
            radius:
                The radius

        '''
        _, radius, _ = self.filename_to_labels(filename)
        return radius

    def filename_to_alpha(self, filename):
        '''

        Args:
          filename:
                The filename to decode

        Returns:
            alpha:
                The camera angle relative to theta

        '''
        _ ,_ , alpha = self.filename_to_labels(filename)
        return alpha
