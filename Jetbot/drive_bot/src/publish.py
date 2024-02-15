#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
import numpy as np
from std_msgs.msg import Bool

wifi_conct = True

def callback(message: Joy):
    global wifi_conct
    if(message.buttons[6]==1):
        wifi_conct = True
    elif(message.buttons[7]==1):
        wifi_conct = False
    
    
    

def main():

    topic1 = '/joy';
    topic2 = '/connection'
    
        
    rospy.init_node('check_connection',anonymous=True);
    rospy.Subscriber(topic1,Joy, callback);
    pub = rospy.Publisher(topic2, Bool,queue_size=10);
    
    while not rospy.is_shutdown():
        pub.publish(wifi_conct)
            


   



if __name__ == '__main__':

    try:
        main()
       
    except rospy.ROSInterruptException:
        rospy.logerr('Subscriber is error');
        pass;
