import shutil, os
import numpy as np

class FilenameIndexer(object):
    def __init__(self, root_path, src_path, dest_path):
        self._root_path = root_path
        self._src_path = src_path
        self._dest_path = dest_path

    def process(self, ascending=True):
        src_full_path = os.path.join(self._root_path, self._src_path)
        dest_full_path = os.path.join(self._root_path, self._dest_path)
        print('Src: {}, Dest: {}'.format(src_full_path, dest_full_path))

        # Get the list of files in the source directory and attach their timestamps.
        # Sort the files in ascending order
        src_file_list = os.listdir(src_full_path)
        file_times = [[file_name, file_time] for file_name, file_time in
                zip(src_file_list, [os.path.getmtime(os.path.join(src_full_path, fn))
                for fn in src_file_list])]

        # specify if sort is ascending or descending.  Sort on timestamp.
        sort_direction = 1 if ascending else -1
        file_times = sorted(file_times, key=lambda row: sort_direction * row[1])

        # Get the list of files in the destination directory to determine where
        # to start indexing.
        dst_file_list = os.listdir(dest_full_path)
        start_idx = len(dst_file_list)
        print('Starting at index: ', start_idx)
        print('Ascending: ', ascending)

        for i, fn in enumerate(file_times):
            src_file = os.path.join(src_full_path, fn[0])
            dest_file = os.path.join(dest_full_path, '{0:03d}'.format(start_idx + i) + '.png')
            shutil.copyfile(src_file, dest_file)
            print('Copy: {}, {}'.format(src_file, dest_file))
