#!/usr/bin/env python3

import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from unity_robotics_demo_msgs.msg import Pose
    

lidar_data = None


    
def scan_callback(msg2):
    global lidar_data; 
    
    lidar_data = msg2 
    
    
def main():

    
    
    topic3 = '/scan'
    topic4 = '/ldata'
    
    rospy.init_node('lidar_subscriber')
    
    rospy.Subscriber(topic3, LaserScan, scan_callback)
    
    
    pub2 = rospy.Publisher(topic4, Pose,queue_size=10)

    
    while not rospy.is_shutdown():
        
        lower_bound = 0
        upper_bound = 13.0
        
        
        if lidar_data is not None:
            
            Z_data = []
            X_data = []
            for i in range(len(lidar_data.ranges)):
                angle = 0 + lidar_data.angle_increment*i
                
                if(lidar_data.ranges[i] >0 and lidar_data.ranges[i]<12):
                
                    zVal = lidar_data.ranges[i]*np.cos(angle)
                    xVal = lidar_data.ranges[i]*np.sin(angle)
                    
                    Z_data.append(zVal)
                    X_data.append(xVal)
                
        
            msg = Pose()
            msg.Xdata = X_data
            msg.Zdata = Z_data
            
            pub2.publish(msg)
           

            

   

if __name__ == '__main__':

    try:
        main();
    
    except Exception as e:
       rospy.logerr(e);
       pass;