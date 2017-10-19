import logging, os, shutil, subprocess, time
import numpy as np

from convobot.simulate.blender.Simulator import Simulator

logger = logging.getLogger(__name__)

class AnimationSimulator(Simulator):
    '''
    Drive the simulation where only one of the 3 features varies and convert the
    still images to a gif.  If the configuration specifies that the image sequence
    needs to run forward and backwards (reverse) then read all the images back in
    and copy them out in reverse order.

    The images are named with a monotonically increasing id starting a 000 to
    support ffmpeg.
    '''
    def __init__(self, global_cfg_mgr):
        logger.debug('Initializing')
        super(AnimationSimulator, self).__init__(global_cfg_mgr)

    def _make_movie(self, tmp_dir_path, index):
        '''

        Args:
          tmp_dir_path: The location to store the images as they are created
                        in preparation for running ffmpeg.
          index: The index of the last file that was generated on the forward
                        pass.  This is used to start the indexing of the
                        reverse pass.

        Returns:  None

        '''
        # If the movied plays forward and backwards then make copies of the
        # forward frames in reverse order with continuing indexes.
        if self._cfg['Reverse']:
            frame_names = os.listdir(tmp_dir_path)
            frame_names.reverse()
            for frame_name in frame_names:
                src_file_path = os.path.join(tmp_dir_path, frame_name)
                dst_file_path = os.path.join(tmp_dir_path, '{0:03d}'.format(index) + '.png')
                shutil.copyfile(src_file_path, dst_file_path)
                index += 1

        # Create the movie using ffmpeg.
        src_file_pattern = os.path.join(tmp_dir_path, '%03d.png')
        dst_file_path = os.path.join(tmp_dir_path, '{}'.format(self._cfg['MovieName']))

        # Run ffmpeg to convert the still png files to a movie.
        cmd_arr = ['ffmpeg', '-i', src_file_pattern, dst_file_path]
        subprocess.run(cmd_arr)

        # Copy the movie to to the animation directory.
        src_file_path = dst_file_path
        dst_dir_path = os.path.join(self._global_cfg_mgr.animation_dir_path, self._cfg['MovieName'])
        shutil.copyfile(src_file_path, dst_dir_path)


    def process(self):
        '''
        Simulate the images where two features are held constant and the
        third is varied.  This is the current configuration.  This could be
        combined with the LoopingSimulator as the functionality has a fair
        amount of overlap.

        Write the images to files in a tree where images are in directories
        based on the Radius feature.  Use FilenameManager to convert from
        Radius, Theta, Alpha to a unique filename.

        Use the 'Fixed' configuration format to specify which features should
        be held constant.
        '''
        logging.debug('Processing')

        # Generate a sequence of images in the temporary directory.
        # Run ffmpeg on them to create the move and store it in
        # the movies directory.
        tmp_dir_path = self._global_cfg_mgr.tmp_dir_path
        self._global_cfg_mgr.clear_tmp()
        index = 0

        # Based on the configuraiton either generate a Range or Fixed set of
        # indexes for the simulation.
        if 'Range' in self._cfg['Radius']:
            radius_cfg = self._cfg['Radius']['Range']
            radius_range = np.arange(radius_cfg['Min'],
                                radius_cfg['Max'] + radius_cfg['Step'],
                                radius_cfg['Step'])
        else:
            radius_range = [self._cfg['Radius']['Fixed']]

        for radius in radius_range:
            if 'Range' in self._cfg['Alpha']:
                alpha_cfg = self._cfg['Alpha']['Range']
                alpha_range = np.arange(alpha_cfg['Min'],
                                    alpha_cfg['Max'] + alpha_cfg['Step'],
                                    alpha_cfg['Step'])
            else:
                alpha_range = [self._cfg['Alpha']['Fixed']]

            for alpha in alpha_range:
                if 'Range' in self._cfg['Theta']:
                    theta_cfg = self._cfg['Theta']['Range']
                    theta_range = np.arange(theta_cfg['Min'],
                                            theta_cfg['Max'] + theta_cfg['Step'],
                                            theta_cfg['Step'])
                else:
                    theta_range = [self._cfg['Theta']['Fixed']]

                for theta in theta_range:
                    t0 = time.time()

                    file_path = os.path.join(tmp_dir_path, '{0:03d}'.format(index)+'.png')

                    # Don't render the image if it exists and has size > 0.
                    # This allows for breaking a simulation and restarting it without
                    # having to recreate all the image.   This is helpful when filling in an
                    # existing dataset.
                    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
                        self._blender_env.set_camera_location(float(theta), float(radius), 180+float(round(alpha,1)))
                        render_time = self._blender_env.render(file_path)

                    process_time = time.time() - t0

                    if logger.isEnabledFor(logging.DEBUG):
                        file_path_parts = file_path.split('/')
                        logger.debug('File: {}, Process Time: {:.2f}'.format(file_path_parts[-1], process_time))

                    index += 1

        # Create the movie from the rendered images.  If reverse is specified
        # let the make_movie method handle the duplication of the images.
        self._make_movie(tmp_dir_path, index)
