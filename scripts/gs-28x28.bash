#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

cd src
# Create the images in blender
# python convobot/simulator/blender/SimulateImages.py -d convobot -c color-256x256

# Convert the images to 28x28 grayscale
# python convobot/imageprocessor/PrepareImages.py -d convobot -c gs-28x28

# Run the model 1-run, 1-epoch on the grayscale images.
python convobot/model/mnist/model.py -d convobot -m mnist-gs -c gs-28x28
cd ..
