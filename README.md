# CHRISLab Flexible Manipulation Demo using Kinova Robot Arm
===================

This package contains at collection of demonstration behaviors for the Kinova Mico
robot arm using the CHRISLab [Flexible Manipulation] system, which is a collection
of [FlexBE] compatible state implementations that interface with ROS [MoveIt!] capabilities.

## Install
-------

The Flexible Manipulation system has been tested using the latest version of ROS Kinetic. You
should first follow the [ROS Install Guide] and get that set up before proceeding.

To use this demonstration, we assume that a catkin workspace is created, and the ```$WORKSPACE_ROOT``` environment variable is defined.  
On a new system, this can be accomplished by following the first six steps of the initial installation directions at [CHRISLab Install].

Change to the ```$WORKSPACE_ROOT/src``` folder (e.g. with ```roscd``` if the workspace is set up correctly), clone this repository, and then run
<pre>
chris_kinova_flexible_manipulation/install/install_chris_kinova_flexible_manipulation.sh
</pre>
This script can be applied to an existing workspace if desired.

This will clone all of the necessary packages for our demonstration.
After the script completes, do a ```catkin build``` and re-source the environment setup before running the programs.

## Usage
-------

### Simulation

* Kinova simulation

<pre>
roscore
roslaunch gazebo_ros empty_world.launch
roslaunch chris_kinova_bringup chris_kinova_robot_gazebo.launch
roslaunch chris_kinova_bringup chris_kinova_trajectory_controllers.launch
roslaunch chris_kinova_bringup chris_moveit_demo.launch
roslaunch chris_kinova_flexible_manipulation chris_kinova_behavior_testing.launch
</pre>


For a hardware based demonstration, see the ```chris_kinova_bringup``` README, and add the
<pre>
roslaunch chris_kinova_flexible_manipulation chris_kinova_behavior_testing.launch
</pre>
The current kinova hardware driver does not properly handle the FollowJointTrajectoryAction, and returns a success result prematurely.


## License
-------

Copyright (c) 2018
Capable Humanitarian Robotics and Intelligent Systems Lab (CHRISLab)
Christopher Newport University

	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:

	  1. Redistributions of source code must retain the above copyright notice,
	     this list of conditions and the following disclaimer.

	  2. Redistributions in binary form must reproduce the above copyright
	     notice, this list of conditions and the following disclaimer in the
	     documentation and/or other materials provided with the distribution.

	  3. Neither the name of the copyright holder nor the names of its
	     contributors may be used to endorse or promote products derived from
	     this software without specific prior written permission.

	     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
	     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
	     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
	     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
	     COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
	     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
	     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
	     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
	     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
	     WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
	     POSSIBILITY OF SUCH DAMAGE.

[FlexBE]: https://flexbe.github.io
[MoveIt!]: http://moveit.ros.org
[ROS Install Guide]: http://wiki.ros.org/kinetic/Installation
[Flexible Manipulation]: https://github.com/CNURobotics/flexible_manipulation
[CHRISLab Install]: https://github.com/CNURobotics/chris_install
