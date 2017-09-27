#!/usr/bin/env bash

# Create sorted list of files to create the theta movie.
cd src

python convobot/util/FilenameOrderer.py -s convobot/simulation/movie-theta/20.0/ -d convobot/movies/theta

cd ..
