import os, sys
import Pyro4
import time
from convobot.util.FilenameManager import FilenameManager

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

def init_blender(env):
    '''
    Initialize the blender environment for the simulation.

    Args:
      env: Remote object used to interact with blender

    Returns:

    '''
    env.set_render_resolution(128, 128)
    env.set_camera_height(1)
    env.set_camera_focal_length(30)
    env.set_camera_location(0, 15, 180)
    return

def main():
    '''
    Connect to blender and run the simulation.
    '''
    # Connect to the Snake Shake Server running in Blender.  See Readme
    # for the steps to get this up and running.
    sys.excepthook = Pyro4.util.excepthook
    env = Pyro4.Proxy("PYRONAME:Env")

    # Initialize Blender
    init_blender(env);

    # Set scale > 1 to create fractional decgree or spacing increments.
    # scale = 5 creates 0.2 degree increments.
    scale = 1
    camera_direction = 180
    fnm = FilenameManager()
    for radius in range(15 * scale, 16 * scale, 1):
        for theta in range(0, 360 * scale, 45):
            t0 = time.time()
            env.set_camera_location(theta / scale, radius / scale, 180)
            filename = fnm.label_to_radius_path('/Users/nathanatkins/datax', theta / scale, radius / scale, camera_direction)
            render_time = env.render(filename)
            process_time = time.time() - t0
            print('File: {}, Process Time: {:.2f}'.format(filename, process_time))

    # env.quit()

if __name__ == '__main__':
    main()
