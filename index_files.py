import sys, getopt, os
import convobot.util.FilenameIndexer as x

def main(argv):
    src_path = None
    dest_path = None
    ascending = True
    usage = 'FilenameOrderer.py -s <source_path> -d <desitnation_path> -a <ascending>'
    try:
        opts, args = getopt.getopt(argv,"hs:d:a:",["source_path=", "destination_path=", "ascending="])
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
        elif opt in ("-a", "--ascending"):
            if arg == 'False':
                ascending = False

    if not src_path or not dest_path:
        print(usage)
    else:
        root_path = os.environ['HOME']
        indexer = x.FilenameIndexer(root_path, src_path, dest_path)
        indexer.process(ascending)

if __name__ == "__main__":
    main(sys.argv[1:])
