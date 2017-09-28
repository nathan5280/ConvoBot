#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
cd src

# Create the images in blender
python convobot/simulator/blender/SimulateImages.py -d convobot -e ../config -c movie-theta
rm $HOME/convobot/movies/theta/*.png
python convobot/util/FilenameOrderer.py -s convobot/simulation/movie-theta/20.0/ -d convobot/movies/theta
rm $HOME/Projects/ConvoBot/documentation/images/theta.gif
ffmpeg -i $HOME/convobot/movies/theta/%03d.png $HOME/Projects/ConvoBot/documentation/images/theta.gif
cd ..
