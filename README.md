This package handles the recording of RGB and depth images from the ZED 2 cameras.

# Requirements

To use this code ROS and Python 2.7 should be installed on your computer.

# Installation

Clone the repository in the src folder of your workspace (if you do not a workspace check https://wiki.ros.org/catkin/Tutorials/create_a_workspace)

```
git clone https://github.com/index-manipulation/zed2_recording.git
```

move to the zed2_recording/src folder and allow execution right to the recording_node.py script

```bat
cd src
chmod +x recording_node.py
```

go back to the main folder of you workspace and run catkin_make

```bat
cd ../../..
catkin make
```

now you are ready to use the code.

### Usage 
It is possible to record data from multiple camera running

```bat
roslaunch zed2_recording multiple_recording.launch
```

two instances of the recording_node.py are instantiated. Each node saves the data in the path specified in the launch file. It is possible to modify the path passing the experiment_name argument.

```bat
roslaunch zed2_recording multiple_recording.launch experimenter_name:="volunteer_1_1"
```

This argument is meant to give an unique name to each data folder.

**Note: If the recording folder already exist the two nodes will return an error message an terminate.**

# Testing

The code has been tested for the following combinations of ROS and Ubuntu:

- ROS Kinetic - Ubuntu 16.04