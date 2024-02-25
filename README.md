# Real-Time_VR_RemoteControl
This repository showcases a project aimed at addressing the challenge of efficient navigation and operation in semi-autonomous robotics, particularly in environments with limited connectivity between robots and humans. By integrating control systems, communication networks, and computation servers, we aim to create a user-friendly semi-autonomous system. Our approach involves remote control via a VR interface, allowing a human operator to control the robot in real time, even in dynamic environments. In instances of connectivity loss, the robot autonomously navigates towards its last known destination while avoiding obstacles until the connection is restored. Our results demonstrate the adaptability of our system, ensuring seamless transitions between remote control and autonomous navigation, thus promising improved human-robot interaction in challenging settings.

## System Architecture
The system architecture for this demonstration involves the integration of hardware and software components.

### Hardware
- Jetbot ROS Ai kit ​
- Two Server Computers
- Varjo VR-1 headset

### Software and frameworks​
- Opencv​
- Robot Operating System​ (ROS)
- Unity (game engine)
  
## Hardware Configuration
In this section, we will outline the setup process for the hardware components. The demo setup includes a robot, two server computers, and a VR headset. Let's delve into the specifics of setting up this hardware configuration.
### Jetbot robot
The robot utilized in this work is based on the open-source 'JetBot ROS AI Kit,' which is built on the NVIDIA Jetson Nano. It is equipped with a 360-degree laser-ranging LiDAR for observing the surroundings from the middle of the robot. Additionally, the robot integrates a RealSense D415 depth camera.For detailed instructions on setting up the robots, please refer to the [official page](https://www.waveshare.com/wiki/JetBot_ROS_AI_Kit).

Furthermore, the installation process involved setting up the RealSense SDK by downloading it from the [official Intel website](https://dev.intelrealsense.com/docs/nvidia-jetson-tx2-installation) and following the provided installation instructions. For OpenCV, the installation was done using the pip package manager with the following command in a terminal:
```
pip install opencv-python
```
Moreover, the TurtleBot3 ROS packages were downloaded and set up by following the instructions provided on the official page.Please refer to the [official page](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/#overview).Now, download this GitHub repository and copy the Jetbot folder to your ROS workspace. After copying the folder, build your workspace:
```
cd ~/<ros_workspace>/
catkin_make
source ~/<ros_workspace>/devel/setup.bash
```
Now insert the IP address of server B into the code located at 'Jetbot/connection_check/src/check.py'.

### Server A
Server A is an Ubuntu OS running machine equipped with ROS (Robot Operating System).To set up Server A, first, create a ROS workspace. Next, download this GitHub repository. Finally, copy the Server A folder into your ROS workspace and  build your workspace:
```
cd ~/<ros_workspace>/
catkin_make
source ~/<ros_workspace>/devel/setup.bash
```
### Server B

To configure server B, employ a machine equipped with the Windows 11 OS. Start by installing the Unity software. Next, import the Varjo XR plugin, the ROS TCP Connector plugin, and the URDF Importer plugin into the Unity game engine. Refer to the instructions provided on the official page below for guidance.
- [Varjo VR](https://github.com/varjocom/VarjoUnityXRPlugin)
- [Ros TCP connector](https://github.com/Unity-Technologies/ROS-TCP-Connector)
- [URDF importer](https://github.com/Unity-Technologies/URDF-Importer)

Next, add the Server B Asset folder to your Unity project.  

## Creating a 2D Map for Navigation
To generate the occupancy grid map for navigation purposes, begin by establishing a connection to the robot via server A using SSH.Once connected, execute the following command in the terminal to launch the SLAM (Simultaneous Localization and Mapping) module:
```
roslaunch jetbot_slam slam_run.launch
```
Next, switch to the terminal of server A and run the following command to visualize the SLAM output:
```
roslaunch turtle_jet jetbot_slam_view.launch
```
After exploring the designated area, ensure to save the resulting 2D map for navigation purposes.
## Real-Time Remote Control via VR over Limited Wireless Connectivity
Now, ensure that both the robot and the server computer are connected to the same Wi-Fi network.Set the robot’s initial position approximately the same on both the virtual map and the physical test area. Proceed to establish an SSH connection to the robot through server A. Execute the following command to initiate navigation:
```
roslaunch jetbot_nav nav_run.launch
```
Following this, open another terminal on server A and execute the command below to visualize the navigation output:
```
roslaunch turtle_jet jetbot_nav_view.launch
```
Finally, execute your Unity project on server B.
## Demo in action
[![Real-Time Remote Control via VR over Limited Wireless Connectivity](https://img.youtube.com/vi/1Hd78-bGPe0/0.jpg)](https://www.youtube.com/watch?v=1Hd78-bGPe0)
## Contributors
1. H.P. Madushanka ([madushanka.hewapathiranage@oulu.fi](madushanka.hewapathiranage@oulu.fi))
2. Rafaela Scaciota ([rafaela.scaciotatimoesdasilva@oulu.fi](rafaela.scaciotatimoesdasilva@oulu.fi))
3. Sumudu Samarakoon ([sumudu.samarakoon@oulu.fi](sumudu.samarakoon@oulu.fi))
4. Mehdi Bennis ([mehdi.bennis@oulu.fi](mehdi.bennis@oulu.fi))
