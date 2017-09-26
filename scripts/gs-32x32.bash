#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

cd src
# Create the images in blender
# python convobot/simulator/blender/SimulateImages.py -d convobot -e ../config -c color-256x256

# Convert the images to 32x32 grayscale
# python convobot/imageprocessor/PrepareImages.py -d convobot -e ../config -c gs-32x32

# Run the model 1-run, 1-epoch on the grayscale images.
python convobot/model/mnist/model.py -d convobot -e ../config -m mnist-gs -c gs-32x32
cd ..
