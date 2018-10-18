# Self-Driving-Car

Documentation is under progress. Thank you for your patience.

### System Overview

This repository is an implementation of a very basic autonomous car using Python, ROS and OpenCV. This car is capable of lane following and detecting STOP signs. The car passes the images obtained from an onboard camera through a neural network to make a decision of its next control signal. This control signal is sent to an Arduino which drives the wheels. The car also uses a Haar feature-based cascade classifier to detect whether or not the current input image contains a STOP sign.

The Arduino code is currently not included in this repository.

### Hardware
- Raspberry Pi 3 (Model B)
- Sony PS3 Eye Camera
- Arduino controlled RC Car

### Results
You can find the video of the robot I developed on [YouTube](https://www.youtube.com/watch?v=7OizN14J0tI)
[![Self Driving Car using ROS Kinetic and Raspberry Pi](https://img.youtube.com/vi/7OizN14J0tI/0.jpg)](https://www.youtube.com/watch?v=7OizN14J0tI)
