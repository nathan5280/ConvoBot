import logging
import sys

from convobot.configuration.GlobalCfgMgr import GlobalCfgMgr

from convobot.util.load_logging_cfg import load_logging_cfg
from convobot.workflow.CfgPipeline import CfgPipeline

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
    global_cfg_mgr = GlobalCfgMgr(argv)

    # Build the processing pipeline based on the loaded configuration and command line arguments.
    pipeline = CfgPipeline(global_cfg_mgr)
    pipeline.process()

    # # Simulate/Animate images based on the Simulate/Animate parameters loaded from the configuration
    # # file.   Note that to attach to Blender using Pyro the SnakeShake package
    # # https://github.com/nathan5280/SnakeShake
    # # The Pyro Name Server and Blender must also be started before this stages
    # # can render images.
    # if global_cfg_mgr.run_simulation:
    #     logger.debug('Loading simulator')
    #     simulator_loader = SimulatorLoader(global_cfg_mgr)
    #     simulator = simulator_loader.get_simulator()
    #     logger.debug('Running simulator')
    #     simulator.process()
    #
    # if global_cfg_mgr.run_animation:
    #     logger.debug('Loading simulator')
    #     simulator_loader = SimulatorLoader(global_cfg_mgr)
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
