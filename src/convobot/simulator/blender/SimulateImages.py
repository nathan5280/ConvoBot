import os, sys, getopt
import Pyro4
import time
import numpy as np
from convobot.util.FilenameManager import FilenameManager
from convobot.workflow.Environment import Environment

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

def init_blender(env, image_size):
    '''
    Initialize the blender environment for the simulation.

    Args:
      env: Remote object used to interact with blender

    Returns:

    '''
    env.set_render_resolution(image_size[0], image_size[1])
    env.set_camera_height(1)
    env.set_camera_focal_length(30)
    env.set_camera_location(0, 15, 180)
    return

def process(dataset_name, config_name):
    '''
    Connect to blender and run the simulation.
    '''
    # Connect to the Snake Shake Server running in Blender.  See Readme
    # for the steps to get this up and running.
    sys.excepthook = Pyro4.util.excepthook
    env = Pyro4.Proxy("PYRONAME:Env")

    # load the simulation configuration from the convobot environment.
    simulation_env = Environment(dataset_name)
    cfg = simulation_env.get_simulation_cfg(config_name)

    # Initialize Blender
    init_blender(env, cfg['image_size']);

    # Grid search the envrionment to create the images.
    camera_direction = 180
    fnm = FilenameManager()
    for radius in np.arange(cfg['radius_range']['min'],
                            cfg['radius_range']['max'] + cfg['radius_range']['step'],
                            cfg['radius_range']['step']):

        # Play with the alph angle to adjust for the larger change in image Location
        # of the target the farther we are away from it.
        alpha_min = cfg['alpha_range']['min'] * cfg['radius_range']['min'] / radius
        alpha_max = (cfg['alpha_range']['max'] + cfg['alpha_range']['step']) * \
                        cfg['radius_range']['min'] / radius
        for alpha in np.arange(alpha_min, alpha_max, cfg['alpha_range']['step']):

            for theta in np.arange(cfg['theta_range']['min'],
                                    cfg['theta_range']['max'] + cfg['theta_range']['step'],
                                    cfg['theta_range']['step']):
                t0 = time.time()
                env.set_camera_location(float(theta), float(radius), 180+float(round(alpha,1)))

                path = simulation_env.get_simulation_output_path(cfg)
                filename = fnm.label_to_radius_path(path,
                            theta, radius, 180+round(alpha,1))

                render_time = env.render(filename)
                process_time = time.time() - t0
                print('File: {}, Process Time: {:.2f}'.format(filename, process_time))

    # env.quit()

def main(argv):
    dataset_name = None
    config_name = None
    usage = 'SimulateImages.py -d <dataset_name> -c <config_name>'
    try:
        opts, args = getopt.getopt(argv,"hd:c:",["dataset_name=","config_name="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-d", "--dataset_name"):
            dataset_name = arg
        elif opt in ("-c", "--config_name"):
            config_name = arg

    if not dataset_name or not config_name:
        print(usage)
    else:
        process(dataset_name, config_name)

if __name__ == "__main__":
    main(sys.argv[1:])
