# Self-Driving-Car

## System Overview

This repository is an implementation of a very basic autonomous car using Python, ROS and OpenCV. This car is capable of lane following and detecting STOP signs. The car passes the images obtained from an onboard camera through a neural network to make a decision of its next control signal. This control signal is sent to an Arduino which drives the wheels. The car also uses a Haar feature-based cascade classifier to detect whether or not the current input image contains a STOP sign.

The Arduino code is currently not included in this repository.

I did this project a very long time ago when I did not realize the importance of structuring code (or making proper videos of results for that matter). The code in the repository can be a little difficult to understand and use but should be fairly straightforward if you go through this README file. I don't have the hardware I used to build the car anymore so I do not want to update the code too much. Feel free to send pull requests if you want to change something.

## Who this project is for?

This project is recommended for you if you want to learn how to use very basic neural networks to program a small car to drive autonomously in structured environments.

Prequisites - basics of Python, OpenCV, ROS, and Neural Networks. A basic understanding of cascade classifiers is also required for the STOP sign detection.

If you're interested in builing a more advanced system, I recommend you to look into [Duckietown](https://www.duckietown.org/).

## Hardware Requirements

You will need the following hardware to build your own autonomous car.

- Raspberry Pi (one of the newer versions is preferable)
- USB / Pi Camera
- Arduino controlled RC Car

You could do away with the Arduino by directly connecting the motor driver to the Raspberry Pi. If you do use an Arduino, you may find it easier to connect it to the Raspberry Pi using a USB cable rather than using the RX and TX pins.

## Code Organization

    .
    ├── cascade_xml             # XML file for STOP sign detection using a Haar Cascade Classifier
    ├── computer                # Scripts which would run on your laptop/desktop rather than the Raspberry Pi
    ├── mlp_xml                 # XML file which stores the neural network which is used for lane following
    └── pi                      # Scripts which would run on the Raspberry Pi

## Setup

Clone an instance of this repository on both your computer as well as the Pi using the following command:
```
git clone https://github.com/surirohit/Self-Driving-Car.git
```

You will also need to build a lane/arena to test the robot. [This](#results) video shows how I did it. 

<a name="results"></a>
## Results
You can find the video of the robot I developed on [YouTube](https://www.youtube.com/watch?v=7OizN14J0tI)
[![Self Driving Car using ROS Kinetic and Raspberry Pi](https://img.youtube.com/vi/7OizN14J0tI/0.jpg)](https://www.youtube.com/watch?v=7OizN14J0tI)
