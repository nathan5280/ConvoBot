# Blender API, and math helper methods
import bpy, mathutils
import os, math
import time

# Py Remote Object Module to support the RPC connection.
import Pyro4

'''
Radial Environment to support generation of images for ConvoBot.
'''

# Expose this interface to external clients.
# Let Pyro manage the instance of this class.  (One per proxy connection.)
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RadialEnv(object):
    def __init__(self):
        '''
        Set up the Environment.

        Input:
            - quit_request: Server method to request shutdown.
        '''
        print('Env: Initializing')

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
        Register the method to call when client requests to quit.

        Input:
            - quit_request: Method to call.

        Return:
            None:
        '''
        self._quit_request = quit_request

    def _deg_2_rad(self, d):
        '''
        Convert between degrees and radians.

        Input:
            d: Degrees to convert

        Output:
            Radian representation of the input
        '''
        return d/180*math.pi

    def _rad_2_deg(self, r):
        '''
        Convert radians to degrees.

        Input:
            r: Radians to convert

        Output:
            Degree representation of the input
        '''
        return r*180/math.pi

    def _radial_2_cartesian(self, theta, radius):
        '''
        Convert radial coordinates to cartesian coordiantes.  Angles are spcified in degrees.

        Input:
            - theta: Angle from origin relative to X-axis
            - radius: Distince from origin

        Rturn:
            (x, y)
        '''
        x = math.cos(self._deg_2_rad(theta)) * radius
        y = math.sin(self._deg_2_rad(theta)) * radius
        return x, y

    # def _cartesian_2_radial(self, cartesian):
    #     '''
    #     Convert cartesian coordianates to radial coordinates. Angles are specified in degrees.
    #
    #     Input:
    #         tuple(x, y)
    #
    #     Return:
    #         tuple(theta, radius)
    #     '''
    #     theta = self._rad_2_deg(atan(cartesian[1] /  cartesian[0]))
    #     radius = (cartesian[0] ** 2 + cartesian[1] ** 2) ** 0.5
    #     return (theta, radius)

    def ping(self, s):
        '''
        Respond to ping request from client to verify the Env is running.
        '''
        print('Env: Ping',s)
        return s

    def reset(self):
        # This will all get replaced when we get the methods to create and
        # configure the Env from imported objects.
        print('Env: Resetting Camera')
        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x, cam_p.y, cam_p.z = 2, -15, self._cam_loc_height
        cam_r.x, cam_r.y, cam_r.z = self._cam_x_rotation, self._cam_y_rotation, self._cam_z_rotation
        return cam_p.x, cam_p.y, cam_r.z

    def set_camera_height(self, height):
        '''
        Set the camera height so we don't need to specify it in every call.

        Input:
            - height:

        Return:
            None
        '''
        self._cam_loc_height = height

    def set_camera_focal_length(self, focal_length):
        '''
        Set camera focal length.  This is the same as on a physical camera.

        Input:
            - focal_length:

        Return:
            None
        '''
        self._cam_focal_length = focal_length
        bpy.data.cameras['Camera'].lens = self._cam_focal_length

    def set_camera_location(self, theta, radius, alpha):
        '''
        Set the camera at the specificed location and rotation in the XY plane.

        Input:
            - theta: Camera rotation angle from X-axis
            - radius: Camera position from origin of X and Y-axis
            - alpha: Camera direction relative to vector from origin to camera (theta)

        Return:
            - None
        '''
        print('Env: Set theta={}, radius={}, alpha={}'.format(theta, radius, alpha))

        cam = bpy.data.objects['Camera']
        x,y = self._radial_2_cartesian(theta, radius)

        cam_p = cam.location
        cam_p.x = x
        cam_p.y = y + 1         # Alignment offset to adjust for the center of the different sized cubes.
        cam_p.z = self._cam_loc_height

        cam_r = cam.rotation_euler
        cam_r.x = self._cam_x_rotation
        cam_r.y = self._cam_y_rotation
        cam_r.z = self._deg_2_rad(theta + alpha + 270)

        print('Env: Set x={}, y={}, r={}'.format(cam_p.x, cam_p.y, cam_r.z))

    def get_render_resolution(self):
        '''
        Get the current render resolution settings.

        Input:

        Output:
            - x resolution
            - y resolution
        '''
        return bpy.data.scenes["Scene"].render.resolution_x, \
                bpy.data.scenes["Scene"].render.resolution_y

    def set_render_resolution(self, new_x_resolution, new_y_resolution):
        '''
        Set the render resolution

        Input:
            - new_x_resolution:
            - new_y_resolution:
        '''
        bpy.data.scenes["Scene"].render.resolution_x = new_x_resolution
        bpy.data.scenes["Scene"].render.resolution_y = new_y_resolution

    def quit(self):
        '''
        Request to shutdown the Env.
        '''
        print('Env: Quitting')
        # Call back to the server provided method to request it to quit.
        self._quit_request()

    def render(self, filename):
        '''
        Render the image to the specified filename

        Input:
            - filename:

        Return:
            - Time in seconds to render the image
        '''
        t0 = time.time()
        bpy.ops.render.render(use_viewport=True)
        bpy.context.scene.render.filepath = filename

        bpy.ops.render.render(write_still=True)
        return time.time() - t0
