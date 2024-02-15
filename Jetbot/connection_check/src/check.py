#!/usr/bin/env python3


import rospy
import os 
import cv2
from std_msgs.msg import Bool

check_connection = True

def check_network_connection():
    global check_connection
    remote_host = "192.168.8.118"
    response = os.system("ping -c 1 " + remote_host)
    if response == 0:
        check_connection = True
        #print("Network connection is active.")
    else:
        check_connection = False
        #print("Network connection is down.")

def check_ros_master_status():
    try:
        rospy.get_master().getPid()
        print("ROS master is running and accessible.")
    except rospy.exceptions.MasterException:
        print("ROS master is not available.")


def main():
    rospy.init_node('network_checker', anonymous=True)
    topic = '/connection'
    pub = rospy.Publisher(topic, Bool,queue_size=10);
    # while not rospy.is_shutdown():
    #     check_network_connection()
        
    #     pub.publish(check_connection)
    #     # if cv2.waitKey(0) & 0xFF == ord('q'):
    #     #     break
        
    try:
        while not rospy.is_shutdown():
            check_network_connection()
            pub.publish(check_connection)
            # if cv2.waitKey(0) & 0xFF == ord('q'):
            #     break
    except KeyboardInterrupt:
        rospy.loginfo("KeyboardInterrupt detected. Stopping the network checker.")
    


if __name__ == '__main__':
    try:
        main()
       
    except rospy.ROSInterruptException:
        rospy.logerr('error');
        pass;

    
    
    
