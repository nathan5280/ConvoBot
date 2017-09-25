#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

cd src
# Create the images in blender
python convobot/simulator/blender/SimulateImages.py -d convobot -c test

# Convert the images to 32x32 grayscale
python convobot/imageprocessor/PrepareImages.py -d convobot -c test-gs

# Run the model 1-run, 1-epoch on the grayscale images.
python convobot/model/mnist/model.py -d convobot -m mnist-gs -c test-gs

# Convert the images to 32x32 RGB
python convobot/imageprocessor/PrepareImages.py -d convobot -c test-color

# Run the model 1-run, 1-epoch on the color images.
python convobot/model/mnist/model.py -d convobot -m mnist-color -c test-color
cd ..
