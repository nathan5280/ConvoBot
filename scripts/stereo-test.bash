#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
python simulate.py -d stereo-test-data -e config -c stereo-test-32x32

python transform.py -d stereo-test-data -e config -c stereo-test-32x32
