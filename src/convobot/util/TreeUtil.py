import os, fnmatch
from shutil import copyfile

class TreeUtil(object):
    '''
    Recursively apply method to directory trees of files.
    '''
    def __init__(self, src_root, dst_root):
        '''
        Create the TreeUtil with the source and target directories where it will
        apply methods.

        Input:
            src_root: Source root directory
            dst_root: Target root directory.   This will always be created.
        '''
        self._src_root = src_root
        self._dst_root = dst_root

        # Create the target directory if it doesn't exist.
        if os.path.exists(dst_root):
            self._cur_dst_dir = dst_root
        else:
            os.makedirs(dst_root)


    def _traverse_dir(self):
        '''
        Traverse the directory tree using os.walk.
        '''
        for os_entry in os.walk(self._src_root):
            # Add logic here if we want to be selective about which directories.
            yield os_entry


    def apply_dir(self, funct):
        '''
        Apply the function to the directory tree.  Function will be called with:
            src_path
            dst_paty
            filename

        Input:
            funct: function to apply to all directories in the tree.
        '''
        [funct(os_entry[0]) for os_entry in self._traverse_dir()]


    def apply_files(self, funct, pattern='*', copy_dir=True):
        '''
        Apply the function to the all files that match the pattern.

        Input:
            funct: function to apply to matching files.
            pattern: pattern to mach the files against.
        '''
        # Duplicate the directory structure so the files have a place to go.
        if copy_dir:
            self.dup_tree()

        for os_entry in self._traverse_dir():
            src_path = os_entry[0]
            rel_path = os_entry[0][len(self._src_root)+1:]
            dst_path = os.path.join(self._dst_root, rel_path)

            for filename in os_entry[2]:
                if fnmatch.fnmatch(filename, pattern):
                    funct(src_path, dst_path, filename)


    def dup_tree(self):
        '''
        Duplicate the directory tree.
        '''
        def create_dir(dir):
            '''
            Helper method to crete the directories in the target tree if they
            don't already exist.
            '''
            # Get the path to create by removing the src_root from the path and
            # then adding it back onto the dst_root.
            rel_path = dir[len(self._src_root)+1:]
            new_path = os.path.join(self._dst_root, rel_path)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        self.apply_dir(create_dir)


    def copy_files(self, fn_pattern):
        '''
        Copy all the files that

        Input:
            fn_pattern: The glob like pattern for the files to copy.
        '''
        def copy_file(src_path, dst_path, filename):
            '''
            Helper method to copy the files that match the pattern.
            '''
            copyfile(os.path.join(src_path, filename), os.path.join(dst_path, filename))

        self.apply_files(copy_file, '*.png')

def main():
    tree = TreeUtil('../Data/gen', './junk')
    # tree.dup_tree();
    tree.copy_files('*.png')

if __name__ == '__main__':
    main()
