# AY21_IGVC
Inteligent Ground Vehicle Competition: Self-Drive AY2021
## Autonomous Vehicle Research and Development

<img src="/Images/Logo.png"
     alt="Logo"
     style="float: left; margin-right: 10px;" />

### Mission Statement
The USMA Autonomous Vehicle Research and Development (AVRAD) team develops, incorporates, and tests urban navigation modules to compete and win in the Intelligent Ground Vehicle Competition (IGVC) and integrates these functionalities within the Robotic Technology Kernel (RTK). ​
### Team Members
* Brian Probert - Team Lead, Model & Simulation
* HyunJin Lim   - SOftware Development and Testing
* Joobon Maeng  - Software Lead, Dev. and Testing
* Chloe DeWees  - Software Development and Testing
* Donte Harris  - Networking/Hardware and Interface
* Jack Whalen   - Model and Simulation
* Hunter Ray    - Project Mangement 
* Chamberlin Liddell-Patacsil - Project Mangement

## Getting Started

### Documentation:
* A.V.R.A.D Vehicle Manual
* Code and Other Resources:
     * West Point Robotics: https://github.com/westpoint-robotics
			*A.V.R.A.D: https://github.com/westpoint-robotics/AY21_IGVC
		
* Other Documentation:
	* Project Management (Trello): https://trello.com/b/WJdc2Lcn/self-drive
	* Project Documentation (Sharepoint/MS Teams):
		* "EECS DSE CME Self-Drive" Teams Channel/Sharepoint: https://teams.microsoft.com/l/channel/19%3aed0981dffe88450b9228be0a464d2360%40thread.skype/General?groupId=e7fafb92-6061-4a25-963e-7a4e181ee339&tenantId=99ff8811-3517-40a9-bf10-45ea0a321f0b
		* "EECS Xe401/402 AY21" Self-Drive Channel/Sharepoint: https://usarmywestpoint.sharepoint.com/:f:/r/sites/EECSXE401XE402AY21-Self-Drive/Shared%20Documents/Self-Drive?csf=1&web=1&e=bM5HNa
			
	* Websites:
		* CME Projects Day Website: https://sites.google.com/view/cme-projects-day-2021/auto-robotics/self-driving-car-v3-0?authuser=0
			
	* Poster: https://drive.google.com/file/d/12V6r1gYFjzf-0YoZLpMXm2YH-bDcwgK3/view?usp=sharing
			
	* Videos:
		* YouTube:
			* Hype Video: https://www.youtube.com/watch?v=CIum67LiaWE
			* Prototype Test: https://www.youtube.com/watch?v=5vBCpxiEXXg

### Launching Current Project
* Navigate to primary working directory: >Home/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw
* roslaunch master.launch

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
