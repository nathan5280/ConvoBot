import os, sys, getopt
# import Pyro4
# import time
# import numpy as np
# from convobot.util.FilenameManager import FilenameManager
# from convobot.workflow.Environment import Environment
from convobot.simulator.blender.StereoSimulator import StereoSimulator

def main(argv):
    data_root = None
    cfg_name = None  # Name of the configuration to load
    cfg_root = None  # Root director for the configuration files
    usage = 'SimulateImages.py -d <data_root> -e <cfg_root> -c <cfg_name>'
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
        simulator = StereoSimulator()
        simulator.process(data_root, cfg_root, cfg_name)

if __name__ == "__main__":
    main(sys.argv[1:])
