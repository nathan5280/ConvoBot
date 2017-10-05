#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
python simulate.py -d poster-stereo -e config -c poster-stereo
python transform.py -d poster-stereo -e config -c poster-stereo
