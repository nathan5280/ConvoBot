#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
# Create the images in blender
rm $HOME/Projects/ConvoBot/documentation/images/alpha.gif
rm $HOME/convobot/movies/alpha/*.png

python -m convobot.simulator.blender.SimulateImages -d convobot -e config -c movie-alpha
rm -r $HOME/convobot/simulation/movie-alpha/collection/*
find $HOME/convobot/simulation/movie-alpha -mindepth 2 -type f -print -exec mv {} $HOME/convobot/simulation/movie-alpha/collection \;
python index_files.py -s convobot/simulation/movie-alpha/collection -d convobot/movies/alpha -a True
python index_files.py -s convobot/simulation/movie-alpha/collection -d convobot/movies/alpha -a False

ffmpeg -i $HOME/convobot/movies/alpha/%03d.png $HOME/Projects/ConvoBot/documentation/images/alpha.gif
