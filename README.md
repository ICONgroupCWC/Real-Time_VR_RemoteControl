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
### Server A
### Server B
