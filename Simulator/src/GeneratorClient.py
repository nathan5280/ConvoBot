import os, sys
import Pyro4
import time

'''
Simple client to drive the camera around in the Blender simulated environment to
generate labeled images.
'''


def init_blender(env):
    env.set_render_resolution(128, 128)
    env.set_camera_height(1)
    env.set_camera_focal_length(30)
    env.set_camera_location(0, 15, 180)
    return

def main():
    # Connect to the Snake Shake Server running in Blender.  See Readme
    # for the steps to get this up and running.
    sys.excepthook = Pyro4.util.excepthook
    env = Pyro4.Proxy("PYRONAME:Env")

    # Initialize Blender
    init_blender(env);

    scale = 1
    camera_direction = 180
    for radius in range(15 * scale, 16 * scale, 1):
        for theta in range(0, 360 * scale, 45):
            t0 = time.time()
            env.set_camera_location(theta / scale, radius / scale, 180)

            filename = os.path.join('data', '{:04.1f}'.format(radius / scale), \
                    '{:05.1f}_{:04.1f}_{:05.1f}'.format(theta / scale, radius / scale, camera_direction))
            render_time = env.render(filename)
            process_time = time.time() - t0
            print('File: {}, Theta: {}, Radius: {}, Camera: {}, Process Time: {:.2f}' \
                    .format(filename, theta / scale, radius / scale, camera_direction, process_time))

    # env.quit()

if __name__ == '__main__':
    main()
