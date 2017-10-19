# Blender API, and math helper methods
import bpy, mathutils
import os, math
import time

# Py Remote Object Module to support the RPC connection.
import Pyro4

'''
This is the working part of the Snake Shake implementation.  This is
the code is that runs inside of Blender.   Create methods here and expose them
through Pyro so that the client can call them as if they were local methods in
the same Python environment.

Be careful about what object are passed in the method calls as Pyro need to be
able to serialize them.  See the Pyro documentation for information on how to
set the serializer and security notices.
'''

# Expose this interface to external clients.
# Let Pyro manage the instance of this class.  (One per proxy connection.)
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Env(object):
    def __init__(self, auto_render=True):
    '''Set up the Environment.
    
        Input:
            - auto_render: Automatically render after scene change.

    Args:

    Returns:

    '''
        print('Env: Initializing')

        # Set the defualt camera parameters
        self._cam_height = 1
        self._cam_x_rotation = math.pi/2
        self._cam_y_rotation = 0
        self._cam_z_rotation = 0

        # Determine if we render each frame after a scene change or require
        # the client to call and request the render.
        self._auto_render = auto_render
        self._render_filename = 'img/n.png'

        # Information on how images rendered to disk will be named and indexed.
        self._image_idx = 1

        # Get the Environmentto a known state.
        self.reset()

    def register_quit_handler(self, quit_request):
        '''Register the method to call when client requests to quit.
        
        Input:
            - quit_request: Method to call.

        Args:
          quit_request: 

        Returns:
          None:

        '''
        self._quit_request = quit_request

    def get_env_name(self):
        ''' '''
        return 'BaseEnv'

    def ping(self, s):
        '''Respond to ping request from client to verify the Env is running.

        Args:
          s: 

        Returns:

        '''
        print('Env: Ping',s)
        return s

    def reset(self):
        ''' '''
        # This will all get replaced when we get the methods to create and
        # configure the Env from imported objects.
        print('Env: Resetting Camera')
        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x, cam_p.y, cam_p.z = 2, -15, self._cam_height
        cam_r.x, cam_r.y, cam_r.z = self._cam_x_rotation, self._cam_y_rotation, self._cam_z_rotation
        if self._auto_render:
            self.render(self._render_filename)
        return cam_p.x, cam_p.y, cam_r.z

    def get_camera_position(self):
        '''Get the x, y, z location of the camera.'''
        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler
        return cam_p.x, cam_p.y, cam_r.z

    def set_camera(self, x, y, rz):
        '''Set the camera at the specificed location and rotation in the XY plane.
        
        Input:
            - x: X location
            - y: Y location
            - rz: Rotation about the Z-axis

        Args:
          x: 
          y: 
          rz: 

        Returns:
          - x, y, rz: the new position of the camera.

        '''
        print('Env: Move dx={}, dy={}, rz={}'.format(x,y,rz))

        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x = x
        cam_p.y = y
        cam_p.z = self._cam_height

        cam_r.x = self._cam_x_rotation
        cam_r.y = self._cam_y_rotation
        cam_r.z = rz

        if self._auto_render:
            self.render(self._render_filename)

        return cam_p.x, cam_p.y, cam_r.z

    def move_camera(self, dx, dy, drz):
        '''Move the camera by the delta position and rotation in the
        XY plane.
        
        Input:
            - dx: Change along the X-axis
            - dy: Change along the Y-axis
            - drz: Change in rotation about the Z-axis

        Args:
          dx: 
          dy: 
          drz: 

        Returns:
          - x, y, rz: the new position of the camera.

        '''

        print('Env: Move dx={}, dy={}, rz={}'.format(dx,dy,drz))

        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x += dx
        cam_p.y += dy
        cam_p.z = self._cam_height

        cam_r.x = self._cam_x_rotation
        cam_r.y = self._cam_y_rotation
        cam_r.z += drz

        if self._auto_render:
            self.render(self._render_filename)

        return cam_p.x, cam_p.y, cam_r.z

    def get_render_resolution(self):
        '''Get the current render resolution settings.
        
        Input:
        
        Output:
            - x resolution
            - y resolution

        Args:

        Returns:

        '''
        return bpy.data.scenes["Scene"].render.resolution_x, \
                bpy.data.scenes["Scene"].render.resolution_y

    def set_render_resolution(self, new_x_resolution, new_y_resolution):
        '''Set the render resolution
        
        Input:
            - new_x_resolution:
            - new_y_resolution:

        Args:
          new_x_resolution: 
          new_y_resolution: 

        Returns:

        '''
        bpy.data.scenes["Scene"].render.resolution_x = new_x_resolution
        bpy.data.scenes["Scene"].render.resolution_y = new_y_resolution

    def quit(self):
        '''Request to shutdown the Env.'''
        print('Env: Quitting')
        # Call back to the server provided method to request it to quit.
        self._quit_request()

    def render(self, filename):
        '''Render the image to the specified filename
        
        Input:
            - filename:

        Args:
          filename: 

        Returns:
          - Time in ms to render the image

        '''
        t0 = time.time()
        bpy.ops.render.render(use_viewport=True)
        if self._auto_render:
            bpy.context.scene.render.filepath = self._render_filename
        else:
            bpy.context.scene.render.filepath = filename

        bpy.ops.render.render(write_still=True)
        return time.time() - t0
