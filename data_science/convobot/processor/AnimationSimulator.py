import logging
import os
import shutil
import subprocess

from convobot.processor.LoopingSimulator import LoopingSimulator

logger = logging.getLogger(__name__)


class AnimationSimulator(LoopingSimulator):
    """
    Drive the simulation where only one of the 3 features varies and convert the
    still images to a gif.  If the configuration specifies that the image sequence
    needs to run forward and backwards (reverse) then read all the images back in
    and copy them out in reverse order.

    The images are named with a monotonically increasing id starting a 000 to
    support ffmpeg.
    """

    def __init__(self, name: str, cfg):
        """
        Construct the Processor.
        :param name: Name of the processor stage
        :param cfg: Processor configurtation.
        """
        logger.debug('Constructing: %s', self.__class__.__name__)
        super().__init__(name, cfg)
        self._index = 0

    def process(self) -> None:
        """
        Run the processor to complete the configured action.

        :return: None
        """

        # Call the LoopingSimulator to loop through Theta, Radius and Alpha
        # For this simulator the images are stored to the temporary directory for
        # post processing into the movies.
        super().process()

        # Create the movie from the rendered images.  If reverse is specified
        # let the make_movie method handle the duplication of the images.
        self._make_movie(self._index)

    def _render(self, theta: float, radius: float, alpha: float) -> None:
        """
        Render the images into the temporary directory for the given Theta, Radius, Alpha
        :param theta: Theta for camera location
        :param radius: Radius for camera location
        :param alpha: Alpha for camera location
        :return: None
        """
        file_path = os.path.join(self.tmp_dir_path, '{0:03d}'.format(self._index) + '.png')

        # Don't render the image if it exists and has size > 0.
        # This allows for breaking a simulation and restarting it without
        # having to recreate all the image.   This is helpful when filling in an
        # existing dataset.
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            self._blender_env.set_camera_location(float(theta), float(radius),
                                                  180 + float(round(alpha, 1)))
            self._blender_env.render(file_path)

        self._index += 1

    def _make_movie(self, index: int):
        """
        Build the movie from a sequence of images.  If the movie should play in a forward reverse loop
        create a reverse copy of the images to complete the loop.
        :param index: The index of the last file that was generated on the forward pass.  This is used to start the
        indexing of the reverse pass.
        :return: None
        """

        # If the movie plays forward and backwards then make copies of the
        # forward frames in reverse order with continuing indexes.
        if self._process_cfg['reverse']:
            frame_names = os.listdir(self.tmp_dir_path)
            frame_names.reverse()
            for frame_name in frame_names:
                src_file_path = os.path.join(self.tmp_dir_path, frame_name)
                dst_file_path = os.path.join(self.tmp_dir_path, '{0:03d}'.format(index) + '.png')
                shutil.copyfile(src_file_path, dst_file_path)
                index += 1

        # Create the movie using ffmpeg.
        dst_file_path = os.path.join(self.dst_dir_path, '{}'.format(self._process_cfg['movie-name']))
        src_file_pattern = os.path.join(self.tmp_dir_path, '%03d.png')

        # Run ffmpeg to convert the still png files to a movie.
        cmd_arr = ['ffmpeg', '-i', src_file_pattern, dst_file_path]
        subprocess.run(cmd_arr)
