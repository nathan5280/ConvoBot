#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
cd src

# Create the images in blender

rm $HOME/Projects/ConvoBot/documentation/images/radius.gif
rm $HOME/convobot/movies/radius/*.png

rm -r $HOME/convobot/simulation/movie-radius/*
mkdir $HOME/convobot/simulation/movie-radius/collection
python -m convobot.simulator.blender.SimulateImages -d convobot -e ../config -c movie-radius-outbound
find $HOME/convobot/simulation/movie-radius -mindepth 2 -type f -print -exec mv {} $HOME/convobot/simulation/movie-radius/collection \;
python -m convobot.util.FilenameOrderer -s convobot/simulation/movie-radius/collection -d convobot/movies/radius

rm -r $HOME/convobot/simulation/movie-radius/*
mkdir $HOME/convobot/simulation/movie-radius/collection
python -m convobot.simulator.blender.SimulateImages -d convobot -e ../config -c movie-radius-inbound
find $HOME/convobot/simulation/movie-radius -mindepth 2 -type f -print -exec mv {} $HOME/convobot/simulation/movie-radius/collection \;
python -m convobot.util.FilenameOrderer -s convobot/simulation/movie-radius/collection -d convobot/movies/radius -i 151

ffmpeg -i $HOME/convobot/movies/radius/%03d.png $HOME/Projects/ConvoBot/documentation/images/radius.gif
cd ..
