import Pyro4, time, sys

# Simple client to drive the camera around in the Blender simulated environment to
# generate labeled images.

class Simulator(object):
    def __init__(self, cfg_mgr, verbose=False):
        self._cfg_mgr = cfg_mgr
        self._verbose = verbose
        self._init_blender()

    def _init_blender(self):
        '''
        Initialize the blender environment for the simulation.

        Args:
          env: Remote object used to interact with blender

        Returns:

        '''
        if self._verbose:
            print('Initializing Blender environment')

        # Connect to the Snake Shake Server running in Blender.  See Readme
        # for the steps to get this up and running.
        sys.excepthook = Pyro4.util.excepthook
        self._blender_env = Pyro4.Proxy("PYRONAME:Env")

        cfg = self._cfg_mgr.get_cfg()
        img_size = cfg['Environment']['ImageSize']

        # Grid search the envrionment to create the images.
        camera_direction = 180
        self._blender_env.set_render_resolution(img_size[0], img_size[1])
        self._blender_env.set_camera_height(cfg['Simulation']['CameraHeight'])
        self._blender_env.set_camera_focal_length(30)
        self._blender_env.set_camera_location(0, 15, 180)
