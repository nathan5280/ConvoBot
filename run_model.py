import os, sys, getopt
from convobot.model.ModelRunner import ModelRunner

def main(argv):
    data_root = None
    cfg_name = None  # Name of the configuration to load
    cfg_root = None  # Root director for the configuration files
    model_name = None  # Directory where to run the model.
    usage = 'ModelRunner.py -d <data_root> -e <cfg_root> -m <model_name> -c <cfg_name>'
    try:
        opts, args = getopt.getopt(argv,"hd:e:m:c:",["data_root=", "cfg_root=", "model_name=", "cfg_name="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--data_root"):
            data_root = arg
        elif opt in ("-e", "--cfg_root"):
            cfg_root = arg
        elif opt in ("-m", "--model_name"):
            model_name = arg
        elif opt in ("-c", "--cfg_name"):
            cfg_name = arg

    if not data_root or not cfg_root or not model_name or not cfg_name:
        print(usage)
    else:
        runner = ModelRunner()
        runner.process(data_root, cfg_root, model_name, cfg_name)

if __name__ == "__main__":
    main(sys.argv[1:])
