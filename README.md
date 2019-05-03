# Human detection package through two LaserScans 2D points.

 - This package listens to the leg_detection and torso_detection topics.
 - Tested on *ROS Kinetic* and *Python2.7*
 - Human detection markers publishes on `/HumanMarker` topic.

## Usage:

 - Clone agn_leg_detection package and make it.
 - Clone agn_torso_detection package and make it.
 - Clone this repo.
 - `catkin_make`
 - `rosrun agn_leg_detection agn_leg_detection.py `
 - `rosrun agn_torso_detection agn_torso_detection.py `
 - `rosrun agn_human_detection agn_human_detection.py `

### TODO:
 - Refactoring (I wrote this node, when I was a newbie in Python.)
 - Make it as parametric-able by ros-param.
