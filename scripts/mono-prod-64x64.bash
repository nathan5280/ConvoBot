#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
# python simulate.py -d mono-prod-64x64-data -e config -c mono-prod-64x64
# python transform.py -d mono-prod-64x64-data -e config -c mono-prod-64x64
python train.py -d mono-prod-64x64-data -e config -c mono-prod-64x64
