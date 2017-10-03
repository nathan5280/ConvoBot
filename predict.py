import os, sys, getopt
from convobot.workflow.ConfigurationManager import ConfigurationManager
from convobot.model.ModelBuilderLoader import ModelBuilderLoader
from convobot.report.Predictor import Predictor

def main(argv):
    data_root = None
    cfg_name = None  # Name of the configuration to load
    cfg_root = None  # Root director for the configuration files
    usage = 'predict.py -d <data_root> -e <cfg_root> -c <cfg_name>'
    try:
        opts, args = getopt.getopt(argv,"hd:e:m:c:",["data_root=", "cfg_root=", "cfg_name="])
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
        cfg_mgr = ConfigurationManager(cfg_root, data_root, cfg_name, verbose=True)
        model_loader = ModelBuilderLoader(cfg_mgr, predict=True, verbose=True)
        model_builder = model_loader.get_model_builder()
        predictor = Predictor(cfg_mgr, model_builder)
        predictor.process()

if __name__ == "__main__":
    main(sys.argv[1:])
