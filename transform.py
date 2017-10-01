import os, sys, getopt
from convobot.workflow.ConfigurationManager import ConfigurationManager
from convobot.transformer.TransformerLoader import TransformerLoader

def main(argv):
    data_root = None
    cfg_name = None  # Name of the configuration to load
    cfg_root = None  # Root director for the configuration files
    usage = 'transform.py -d <data_root> -e <cfg_root> -c <cfg_name>'
    try:
        opts, args = getopt.getopt(argv,"hd:e:c:",["data_root=", "cfg_root=", "cfg_name="])
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
        elif opt in ("-c", "--cfg_name"):
            cfg_name = arg

    if not data_root or not cfg_root or not cfg_name:
        print(usage)
    else:
        # load the simulation configuration from the convobot environment.
        cfg_mgr = ConfigurationManager(cfg_root, data_root, cfg_name, verbose=True)
        for i in range(len(cfg_mgr.get_cfg()['Transformer']['Pipeline'])):
            transform = TransformerLoader(cfg_mgr, i, verbose=True).get_transformer()
            transform.process()

if __name__ == "__main__":
    main(sys.argv[1:])
