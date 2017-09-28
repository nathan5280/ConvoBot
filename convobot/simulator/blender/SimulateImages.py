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

def process(data_root, cfg_root, cfg_name):
    '''
    Connect to blender and run the simulation.
    '''
    # Connect to the Snake Shake Server running in Blender.  See Readme
    # for the steps to get this up and running.
    sys.excepthook = Pyro4.util.excepthook
    env = Pyro4.Proxy("PYRONAME:Env")

    # load the simulation configuration from the convobot environment.
    simulation_env = Environment(cfg_root, data_root)
    cfg = simulation_env.get_simulation_cfg(cfg_name)

    # Initialize Blender
    init_blender(env, cfg['image_size']);

    # Grid search the envrionment to create the images.
    camera_direction = 180
    fnm = FilenameManager()

    # set the range as fixed value or the dynamically created range.
    if 'fixed' in cfg['radius_range']:
        radius_range = range(cfg['radius_range']['fixed'], cfg['radius_range']['fixed']+1, 2)
        radius_min = cfg['radius_range']['fixed']
        radius_max = cfg['radius_range']['fixed']
    else:
        radius_range = np.arange(cfg['radius_range']['min'],
                                cfg['radius_range']['max'] + cfg['radius_range']['step'],
                                cfg['radius_range']['step'])
        radius_min = cfg['radius_range']['min']
        radius_max = cfg['radius_range']['max']

    for radius in radius_range:


        # set the ranges as a fixed value or the dynamically created range.
        if 'fixed' in cfg['alpha_range']:
            alpha_range = range(cfg['alpha_range']['fixed'],cfg['alpha_range']['fixed']+1,2)
        else:
            # Play with the alph angle to adjust for the larger change in image Location
            # of the target the farther we are away from it.


            alpha_min = cfg['alpha_range']['min'] * radius_min / radius
            alpha_max = (cfg['alpha_range']['max'] + cfg['alpha_range']['step']) * \
                            radius_min / radius
            alpha_range = np.arange(alpha_min, alpha_max, cfg['alpha_range']['step'])

        for alpha in alpha_range:

            # set the range as fixed value or the dynamically created range.
            if 'fixed' in cfg['theta_range']:
                theta_range = range(cfg['theta_range']['fixed'],cfg['theta_range']['fixed']+1,2)
            else:
                theta_range = np.arange(cfg['theta_range']['min'],
                                        cfg['theta_range']['max'] + cfg['theta_range']['step'],
                                        cfg['theta_range']['step'])

            for theta in theta_range:
                t0 = time.time()
                env.set_camera_location(float(theta), float(radius), 180+float(round(alpha,1)))

                path = simulation_env.get_simulation_output_path()
                filename = fnm.label_to_radius_path(path,
                            theta, radius, 180+round(alpha,1))

                render_time = env.render(filename)
                process_time = time.time() - t0
                print('File: {}, Process Time: {:.2f}'.format(filename, process_time))

    # env.quit()

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
        process(data_root, cfg_root, cfg_name)

if __name__ == "__main__":
    main(sys.argv[1:])
