#!/usr/bin/env bash

# Copy the Env class to a directory where Blender can find it.
# Uncomment the line to copy the correct Env.  Convobot uses RadialEnv
# cp snakeshake/env/Env.py /Applications/blender.app/Contents/Resources/2.78/python/lib/python3.5/site-packages/snakeshake/Env.py
cp convobot/simulate/blender/RadialEnv.py /Applications/blender.app/Contents/Resources/2.78/python/lib/python3.5/site-packages/snakeshake/Env.py

# Start blender in the background (-b) and run the background SnakeShakeServer code on startup.
/Applications/blender.app/Contents/MacOS/blender -b -P snakeshake/SnakeShakeBGServer.py
