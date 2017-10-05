#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
# python simulate.py -d stereo-prod-64x64-data -e config -c stereo-prod-64x64
# python transform.py -d stereo-prod-64x64-data -e config -c stereo-prod-64x64
python train.py -d stereo-prod-64x64-data -e config -c stereo-prod-64x64
