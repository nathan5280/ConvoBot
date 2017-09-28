#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
# Create the images in blender
python simulate_images.py -d convobot -e config -c movie-theta
rm $HOME/convobot/movies/theta/*.png
python index_files.py -s convobot/simulation/movie-theta/20.0/ -d convobot/movies/theta
rm $HOME/Projects/ConvoBot/documentation/images/theta.gif
ffmpeg -i $HOME/convobot/movies/theta/%03d.png $HOME/Projects/ConvoBot/documentation/images/theta.gif
