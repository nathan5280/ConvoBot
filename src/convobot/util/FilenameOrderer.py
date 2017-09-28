import os, sys, getopt, shutil
import numpy as np

def process(root_path, src_path, dest_path, start_idx):
    src_full_path = os.path.join(root_path, src_path)
    dest_full_path = os.path.join(root_path, dest_path)
    print('Src: {}, Dest: {}, Idx:{}'.format(src_full_path, dest_full_path, start_idx))

    file_list = os.listdir(src_full_path)
    file_times = [[file_name, file_time] for file_name, file_time in
            zip(file_list, [os.path.getmtime(os.path.join(src_full_path, fn))
            for fn in file_list])]

    file_times = sorted(file_times, key=lambda row: row[1])

    for f in file_times:
        print(f)

    for i, fn in enumerate(file_times):
        src_file = os.path.join(src_full_path, fn[0])
        dest_file = os.path.join(dest_full_path, '{0:03d}'.format(start_idx + i) + '.png')
        shutil.copyfile(src_file, dest_file)
        print('Copy: {}, {}'.format(src_file, dest_file))

def main(argv):
    src_path = None
    dest_path = None
    start_idx = 0
    usage = 'FilenameOrderer.py -s <source_path> -d <desitnation_path> -i <start_index>'
    try:
        opts, args = getopt.getopt(argv,"hs:d:i:",["source_path=", "destination_path=", "start_index="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-s", "--source_path"):
            src_path = arg
        elif opt in ("-d", "--destination_path"):
            dest_path = arg
        elif opt in ("-i", "--start_idx"):
            start_idx = arg

    print(src_path, dest_path, start_idx)

    if not src_path or not dest_path:
        print(usage)
    else:
        root_path = os.environ['HOME']
        process(root_path, src_path, dest_path, int(start_idx))

if __name__ == "__main__":
    main(sys.argv[1:])
