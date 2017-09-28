#!/usr/bin/env bash

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
python simulate_images.py -d convobot -e config -c test

# Convert the images to 28x28 grayscale
python prepare_images.py -d convobot -e config -c test-gs

# Run the model 1-run, 1-epoch on the grayscale images.
python run_model.py -d convobot -e config -m mnist-gs -c test-gs
