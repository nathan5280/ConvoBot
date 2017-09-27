# Convolutional Neural Network + Robotics = ConvoBot
ConvoBot brings together a number of related areas of interest for me in Robotics _(Hobby)_; engineering, software development _(Work Experience)_; solving problems using data _(Data Science)_.  The overarching goal of the project is to enable autonomous location and control of a robot relative to it's environment using Convolutional Neural Networks (CNN).  My Capstone work during the Galvanize Data Science Immersive Program provided an opportunity to get the Data Science side of the project kicked off.  It also opened up a very interesting opportunity to explore how simulated environments can be used to explore feature space, better understand the dynamics of neural networks, and decouple knowledge and skills learning from the dynamics and slow pace of the physical world.

<p align=“center”>
<img alt="Hierarchy of topics in scope for ConvoBot and focus on Simulated Labeled Data." src="documentation/images/Overview.png" width='600'>
</p>
<sub><b>Figure 1: </b>Hierarchy of topics in scope for ConvoBot.</sub>

## Table of Contents
1. [Overview](#overview)
2. [Convolutional Neural Networks](#convolutional-neural-networks)

## Overview
ConvoBot will be equipped with a fixed camera facing forward.  Based on the images captured and the well know red and blue target blocks, the CNN should be able to predict the location of ConvoBot.  Position is defined by:
* <b>Radius</b> - distance from the center of the environment.
* <b>Theta</b> - the angular displacement from the X-axis.
* <b>Alpha</b> - The angular displacement of the forward facing camera from the radial line back to the center of the environment.

<p align=“center”>
<img alt="ConvoBot environment and location parameters." src="documentation/images/ConvoBot-Location.png" width='600'>
</p>
<sub><b>Figure 2: </b>Environment and location parameters.</sub>

## Convolutional Neural Networks
Convolutional Neural Networks (CNN) are a powerful machine learning tool that has become very powerful and popular in the last decade.  Highly visible research combine with increases in computer power, labeled datasets, prize based competitions are all driving exponential growth in CNN research and applications. CNN are widely used in some of these fields:
* <b>Voice Recognition</b> - Siri, Cortana, Alexa
* <b>Text Translation and Transcribing</b> - Google Translate
* <b>Autonomous Cars</b>
* <b>Biology & Drug Discovery</b>
* <b>Finance, Fraud Detection</b>
* <b>Astronomy</b>
* <b>Robotics</b>
