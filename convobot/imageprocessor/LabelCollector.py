class LabelCollector(object):
    '''
    Collect a list of files that have a parsed value in the value list.

    Input:
        values: the values to look for matches against.
        parser: the parser to extract the value from the filename.
    '''
    def __init__(self, values, parser):
        self._values = values
        self._parser = parser
        self._filenames = []

    def _match(self, filename):
        '''
        Test the file name against the values list.

        Input:
            filename: the name to test.

        Return:
            True if the filename matches.
        '''
        return self._parser(filename) in self._values

    def collect(self, src_path, dst_path, filename):
        '''
        Method called by the TreeUtil for each of the files.

        Input:
            src_path: source path for the file.
            dst_path: not used.
            filename: filename to test.

        Return:
            None
        '''
        if self._match(filename):
            self._filenames.append((src_path, filename))

    def get_filenames(self):
        '''
        Return the list of the files that were collected.   Each entry
        is a tuple of (src_path, filename)
        '''
        return self._filenames

    def get_collector_funct(self):
        '''
        Get the collector function to pass to TreeUtil
        '''
        return self.collect
