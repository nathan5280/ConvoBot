import sys, json, logging
from logging.config import dictConfig

from convobot.util.CmdLineCfgMgr import CmdLineCfgMgr
from convobot.util.CfgMgr import CfgMgr
from convobot.simulate.blender.SimulatorLoader import SimulatorLoader
from convobot.manipulate.ManipulatorLoader import ManipulatorLoader
from convobot.train.TrainerLoader import TrainerLoader
from convobot.train.ModelLoader import ModelLoader

with open('logging-cfg.json', 'r') as f:
    logging_cfg = json.load(f)

dictConfig(logging_cfg)
logger = logging.getLogger(__name__)

def main(args):
    logger.debug('Application started')

    cmd_cfg_mgr = CmdLineCfgMgr(args)
    cmd_cfg = cmd_cfg_mgr.get_cfg_dict()
    cfg_mgr = CfgMgr(cmd_cfg)

    if cmd_cfg['RunSimulate']:
        logger.debug('Loading simulator')
        simulator_loader = SimulatorLoader(cfg_mgr)
        simulator = simulator_loader.get_simulator()
        logger.debug('Running simulator')
        simulator.process()

    if cmd_cfg['RunManipulate']:
        logger.debug('Loading manipulator')
        manipulator_loader = ManipulatorLoader(cfg_mgr)
        manipulator = manipulator_loader.get_manipulator()
        logger.debug('Running manipulator')
        manipulator.process()

    if cmd_cfg['RunTrain']:
        logger.debug('Loading trainer')
        trainer_loader = TrainerLoader(cfg_mgr)
        trainer = trainer_loader.get_trainer()
        logger.debug('Running trainer')
        trainer.process()

if __name__ == '__main__':
    main(sys.argv[1:])
