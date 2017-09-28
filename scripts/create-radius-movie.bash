#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
# Create the images in blender
rm $HOME/Projects/ConvoBot/documentation/images/radius.gif
rm $HOME/convobot/movies/radius/*.png

python -m convobot.simulator.blender.SimulateImages -d convobot -e config -c movie-radius
rm -r $HOME/convobot/simulation/movie-radius/collection/*
find $HOME/convobot/simulation/movie-radius -mindepth 2 -type f -print -exec mv {} $HOME/convobot/simulation/movie-radius/collection \;
python index_files.py -s convobot/simulation/movie-radius/collection -d convobot/movies/radius -a True
python index_files.py -s convobot/simulation/movie-radius/collection -d convobot/movies/radius -a False

ffmpeg -i $HOME/convobot/movies/radius/%03d.png $HOME/Projects/ConvoBot/documentation/images/radius.gif
