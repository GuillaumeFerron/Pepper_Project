pepper_teleop
================


This directory is a copy of Fabrice Jumel repo, to be able to access it in our project the git directory(so the git remote) has been removed and thus the current directory isn't linked to Fabrice Jumel's repo anymore. To be able to get any updates you can find his repo to : https://github.com/fabricejumel/pepper-ros-teleop.git

Simple Pepper Teleoperation implementation based on turtlebot one.

raw version. Test only in ubuntu 14.04, ros indigo

##add to your catkin_ws and compile
dependecies to roscpp, geometry_msgs, naoqi_bridge_msgs, joy

##Launch joy for teleop 
roslaunch pepper_teleop pepper_ps3_teleop.launch


Default configuration :
to move pepper, press continiously the right bouton shoulder
D-Pad Left and right to tangential move
Left analog sticks for angle and orthogonal move

Left analog sticks for Move head (absolute control)
toogle pause of the head with left bottom shoulder 







##you  need a naoqi_driver running with your pepper, classicaly :
roslaunch pepper_bringup pepper_full.launch 

configuration can be change in launch file with parameter
by default joy    has to be mount as /dev/input/js0

Example to install joy for indigo ROS :
sudo apt-get install ros-indigo-joy ros-indigo-joystick-drivers

naoqi_bridge_msgs:
naoqi_bridge_msgs is part of https://github.com/ros-naoqi/naoqi_bridge

pepper_bringup is part of: 
https://github.com/ros-naoqi/pepper_robot
