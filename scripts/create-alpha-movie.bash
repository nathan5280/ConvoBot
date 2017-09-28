#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
cd src

# Create the images in blender
rm $HOME/Projects/ConvoBot/documentation/images/alpha.gif
rm $HOME/convobot/movies/alpha/*.png

python -m convobot.simulator.blender.SimulateImages -d convobot -e ../config -c movie-alpha-outbound
rm -r $HOME/convobot/simulation/movie-alpha/collection/*
find $HOME/convobot/simulation/movie-alpha -mindepth 2 -type f -print -exec mv {} $HOME/convobot/simulation/movie-alpha/collection \;
python -m convobot.util.FilenameOrderer -s convobot/simulation/movie-alpha/collection -d convobot/movies/alpha

python -m convobot.simulator.blender.SimulateImages -d convobot -e ../config -c movie-alpha-inbound
rm -r $HOME/convobot/simulation/movie-alpha/collection/*
find $HOME/convobot/simulation/movie-alpha -mindepth 2 -type f -print -exec mv {} $HOME/convobot/simulation/movie-alpha/collection \;
python convobot/util/FilenameOrderer.py -s convobot/simulation/movie-alpha/collection -d convobot/movies/alpha -i 41

ffmpeg -i $HOME/convobot/movies/alpha/%03d.png $HOME/Projects/ConvoBot/documentation/images/alpha.gif
cd ..
