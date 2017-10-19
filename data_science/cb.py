import json, logging, sys, os
from logging.config import dictConfig

from convobot.environment.CmdLineCfgMgr import CmdLineCfgMgr
from convobot.environment.GlobalCfgMgr import GlobalCfgMgr
from convobot.util.load_logging_cfg import load_logging_cfg

load_logging_cfg('./logging-cfg.json')
logger = logging.getLogger(__name__)

def main(argv):
    '''
    Control how convobot execution proceeds based on the command line arguments.

    Args:
      argv: Command Line arguments to pass to the CmdLineCfgMgr.
            -h to generate help message for valid arguments.

    Returns: None
    '''
    logger.info('ConvoBot application started')
    global_cfg_mgr = GlobalCfgMgr()
    global_cfg_mgr.configure(argv)


    # # In general convobot is designed be configurable and extensible through the
    # # configuration file.  All of the *Loader classes dynamicall load the
    # # actual processing classes based on names specified in the configuration
    # # file.
    #
    # # TODO: Replace the loaders with dynamic module loading so the Exampler lookup
    # # in the Loader classes isn't required.  This will truely make the applicaation
    # # configurable and dynamically extensible.
    #
    # # Parse the command line arguments and pass the results to the CfgMgr.
    # # The CfgMgr will load the json configuration file with all of the remaining
    # # parameters for each of the stages.
    # cmd_cfg_mgr = CmdLineCfgMgr(args)
    # cmd_cfg = cmd_cfg_mgr.get_cfg_dict()
    # cfg_mgr = CfgMgr(cmd_cfg)
    #
    # # Simulate images based on the Simulate parameters loaded from the configuration
    # # file.   Note that to attach to Blender using Pyro the SnakeShake package
    # # https://github.com/nathan5280/SnakeShake
    # # The Pyro Name Server and Blender must also be started before this stages
    # # can render images.
    # if cmd_cfg['RunSimulate']:
    #     logger.debug('Loading simulator')
    #     simulator_loader = SimulatorLoader(cfg_mgr)
    #     simulator = simulator_loader.get_simulator()
    #     logger.debug('Running simulator')
    #     simulator.process()
    #
    # # Manipulate images to get them from the rendered format of individual files
    # # on disk to large consolidated Numpy arrays.
    # # Currently this manipulation only includes conversion from RGBA to RGB and
    # # the stacking in the Numpy array.  If resizing needs to take place this
    # # is the stage where that would be performed.
    # if cmd_cfg['RunManipulate']:
    #     logger.debug('Loading manipulator')
    #     manipulator_loader = ManipulatorLoader(cfg_mgr)
    #     manipulator = manipulator_loader.get_manipulator()
    #     logger.debug('Running manipulator')
    #     manipulator.process()
    #
    # # Train the CNN on the images from the Numpy array.  The TrackingTrainer
    # # saves the TensorBoard files and the predition results as the training
    # # is performed.  While neither of these are required to perform the training
    # # they provide useful insites during training and post training
    # # visualization.
    # if cmd_cfg['RunTrain']:
    #     logger.debug('Loading trainer')
    #     trainer_loader = TrainerLoader(cfg_mgr)
    #     trainer = trainer_loader.get_trainer()
    #     logger.debug('Running trainer')
    #     trainer.process()


if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv[1:])
