# Blender API, and math helper methods
import bpy, mathutils
import os, math, logging
import time

# Py Remote Object Module to support the RPC connection.
import Pyro4

logger = logging.getLogger(__name__)

# TODO: Replace radians to degrees and degrees to radians with math.degrees
# and math.radians

# Expose this interface to external clients.
# Let Pyro manage the instance of this class.  (One per proxy connection.)
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Env(object):
    '''
    Radial Environment to support generation of images for ConvoBot.
    This is the object that is running in Blender and Pyro creates the
    http RPC to expose this interface as a local object.
    '''
    def __init__(self):
        logger.debug('xInitializing Blender environment')

        # Set camera focal length
        self._cam_focal_length = 35

        # Set the default camera location
        self._cam_loc_height = 1
        self._cam_loc_angle = 0
        self._cam_loc_radius = 15

        # Set the defualt camera parameters
        self._cam_x_rotation = math.pi/2
        self._cam_y_rotation = 0
        self._cam_z_rotation = 180

        # Get the Environment to a known state.
        self.reset()

    def register_quit_handler(self, quit_request):
        '''

        Args:
          quit_request: Function to call in SnakeShake server when client requests quit.

        Returns:

        '''
        self._quit_request = quit_request

    def get_env_name(self):
        '''Name of the environment that SnakeShake is loading and remoting.'''
        return 'RadialEnv'

    def _deg_2_rad(self, d):
        '''Convert degrees to radians.

        Args:
          d: Degree value to convert.

        Returns:
          : Radian representation of d.

        '''
        return d/180*math.pi

    def _rad_2_deg(self, r):
        '''Convert radians to degrees.

        Args:
          r: Radian value to convert.

        Returns:
          : Degree represenation of r.

        '''
        return r*180/math.pi

    def _radial_2_cartesian(self, theta, radius):
        '''Convert radial coordinates to cartesian coordianates.

        Args:
          theta: The angle from X-axis.
          radius: The distance from the origin.

        Returns:
          : Cartesian X, Y representation of (theta, radius)

        '''
        x = math.cos(self._deg_2_rad(theta)) * radius
        y = math.sin(self._deg_2_rad(theta)) * radius
        return x, y

    def ping(self, s):
        '''Ping request to make sure the server is running.

        Args:
          s: Ping string that is returned to the client.

        Returns:
          : string s.

        '''
        logging.info('Env: Ping',s)
        return s

    def reset(self):
        '''Reset the blender environment to some known state.  All of this should
        be overridden by the client with they initialize the environment.

        Args:

        Returns:


        '''
        # This will all get replaced when we get the methods to create and
        # configure the Env from imported objects.
        logging.debug('Resetting Camera')
        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x, cam_p.y, cam_p.z = 2, -15, self._cam_loc_height
        cam_r.x, cam_r.y, cam_r.z = self._cam_x_rotation, self._cam_y_rotation, self._cam_z_rotation
        return cam_p.x, cam_p.y, cam_r.z

    def set_camera_height(self, height):
        '''Set the height of the camera above the X, Y plane.

        Args:
          height: Height in inches

        Returns:

        '''
        logging.debug('Setting camera height: %s', height)
        self._cam_loc_height = height

    def set_camera_focal_length(self, focal_length):
        '''Set the focal length of the camera.  This works just like a real camera.

        Args:
          focal_length: Focal length in mm

        Returns:

        '''
        self._cam_focal_length = focal_length
        bpy.data.cameras['Camera'].lens = self._cam_focal_length

    def set_camera_location(self, theta, radius, alpha):
        '''Set the camera location in radial coordinates.

        Args:
          theta: The angle from X-axis
          radius: The distance from the center of the scene
          alpha: The direction of the camera relative to the radial line along theta.

        Returns:

        '''
        logging.debug('Set camera location: theta=%s, radius=%s, alpha=%s', theta, radius, alpha)

        cam = bpy.data.objects['Camera']
        x,y = self._radial_2_cartesian(theta, radius)

        cam_p = cam.location
        cam_p.x = x
        cam_p.y = y
        cam_p.z = self._cam_loc_height

        cam_r = cam.rotation_euler
        cam_r.x = self._cam_x_rotation
        cam_r.y = self._cam_y_rotation
        cam_r.z = self._deg_2_rad(theta + alpha + 270)


    def get_render_resolution(self):
        '''Query the blender for the current render resolution.

        Args:

        Returns:
          x_resolution, y_resolution: Current render resolution.

        '''
        return bpy.data.scenes["Scene"].render.resolution_x, \
                bpy.data.scenes["Scene"].render.resolution_y

    def set_render_resolution(self, new_x_resolution, new_y_resolution):
        '''Set the render resolution in blender.

        Args:
          new_x_resolution: x resolution for rendered images.
          new_y_resolution: y resolution for rendered images.

        Returns:

        '''
        bpy.data.scenes["Scene"].render.resolution_x = new_x_resolution
        bpy.data.scenes["Scene"].render.resolution_y = new_y_resolution

    def quit(self):
        '''Request that the blender environment and SnakeShake servers shutdown.'''
        logger.debug('Quitting Blender')
        # Call back to the server provided method to request it to quit.
        self._quit_request()

    def render(self, filename):
        '''Render the scene to the specified filename.

        Args:
          filename: Name and location to render the file.

        Returns:

        '''
        t0 = time.time()
        bpy.ops.render.render(use_viewport=True)
        bpy.context.scene.render.filepath = filename

        bpy.ops.render.render(write_still=True)
        return time.time() - t0
