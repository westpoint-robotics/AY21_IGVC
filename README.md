# AY21_IGVC
Inteligent Ground Vehicle Competition: Self-Drive AY2021
## Autonomous Vehicle Research and Development Team

<img src="/Images/Logo.png"
     alt="Logo"
     style="float: left; margin-right: 10px;" />

### Mission Statement
The USMA Autonomous Vehicle Research and Development (AVRAD) team develops, incorporates, and tests urban navigation modules to compete and win in the Intelligent Ground Vehicle Competition (IGVC) and integrates these functionalities within the Robotic Technology Kernel (RTK). ​
### Members
* Brian Probert - Team Lead
* HyunJin Lim
* Joobon Maeng
* Chloe DeWees
* Donte Harris
* Jack Whalen
* Chamberlin Liddell-Patacsil

## Getting Started
### Getting ROS to recognize a new workspace (for example, catkin_ws):
* In terminal, run 'sudo gedit ~/.bashrc'
* At the bottom of the file, add the line 'source [YOUR PATH]/catkin_ws/devel/setup.bash'
* Save and exit, then new terminal windows

### Getting darknet to run on a ROS machine:

* In terminal, run 'sudo gedit /etc/ld.so.conf.d/darknetLib.conf'
* Then, paste the path to the libdarknet.so file, e.g., '/home/user1/catkin_ws/src/AY20_IGVC/src/object_recognition/darknet_test'
* Save and exit, then run 'sudo ldconfig' in the terminal.
* Now new terminal windows will work with it.

### Running whiteline controller:
* In terminal, run 'fm_camera.launch'
* In terminal, run 'whiteline_detector.py'
* In terminal, run 'whiteLineController.py'
* In terminal, run appropriate rosbag (I suggest IGVCStopsSign.bag) 'rosbag play bagfile'
* In terminal, run 'rostopic echo /speed_applied'

### Running lane finder and following controller:
* In terminal, run 'fr_camera.launch'
* In terminal, run 'rightLaneDetector.py'
* In terminal, run 'steeringController.py'

### Running darknet controller:
* In terminal, run 'roscore'
* In terminal, run 'darknet.py'
* In terminal, run 'signController.py'
* In terminal, run appropriate rosbag (I suggest IGVCStopsSign.bag) 'rosbag play bagfile'
* In terminal, run 'rostopic echo /detection_status'

### Final Stop Sign Detection Stuff:
* Follow above insrtuctions for whiteline and darknet controller
* In terminal, run 'constVelocity.py'
* The vehicle should now send brake commands to pacmod as is appropriate

### Launching the main package:

* Run 'roslaunch AY20_IGVC gem_e2.launch
<img src="/Images/IGVC.png"
     alt="IGVC Cadets"
     style="float: left; margin-right: 10px;" />