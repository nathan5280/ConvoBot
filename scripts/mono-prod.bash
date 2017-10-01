#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
# python simulate.py -d mono-prod-data -e config -c mono-prod-128x128
# python transform.py -d mono-prod-data -e config -c mono-prod-128x128
python train.py -d mono-prod-data -e config -c mono-prod-128x128
