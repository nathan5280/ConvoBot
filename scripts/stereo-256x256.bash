#!/usr/bin/env bash

# Generate 256x256 images for the left and right camera of a stereo image.

# Before running this script make sure Blender and name server are running.
# ./scripts/nameserver.bash
# ./scripts/snake-shake-background.bash

# Create the images in blender
# python stereo_simulate_images.py -d convobot -e config -c stereo-r-256x256
# python stereo_simulate_images.py -d convobot -e config -c stereo-l-256x256

# Convert the images to 32x32 grayscale
python stereo_prepare_images.py -d convobot -e config -c cv-32x32

# Run the model 1-run, 1-epoch on the grayscale images.
# python run_model.py -d convobot -e config -m mnist-color -c color-32x32
