#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
import numpy as np
from geometry_msgs.msg import Twist
from numpy import interp
from std_msgs.msg import Bool

move_cmd = Twist()
save_map = False

def callback(message: Joy):
    global save_map,move_cmd
    push = message.buttons[7] 
    #print(push)
    if(push==1):
       
        save_map = True
    else:
        save_map = False


    lval = round(interp(message.axes[1],[-1,1],[-0.2,0.2]),2)
    move_cmd.linear.x = lval
    move_cmd.linear.y = 0.0
    move_cmd.linear.z = 0
    
    aval = round(interp(message.axes[2],[-1,1],[-1,1]),2)
    
    move_cmd.angular.x = 0.0
    move_cmd.angular.y = 0.0
    move_cmd.angular.z = aval
    
    stt = "linear_velocity = " + str(round(message.axes[1], 2)) + " Angular_velocity = " + str(aval)
    
    


    

def main():

    topic1 = '/joy';
    topic2 = '/cmd_vel';
    topic3 = '/save_map_cmd'
        
    rospy.init_node('joy_sub',anonymous=True);
    pub = rospy.Publisher(topic2, Twist,queue_size=10);
    pub2 = rospy.Publisher(topic3, Bool,queue_size=10);
    rospy.Subscriber(topic1,Joy, callback);
    
    while not rospy.is_shutdown():
        
        pub.publish(move_cmd)
        pub2.publish(save_map)
            


   



if __name__ == '__main__':

    try:
        main()
       
    except rospy.ROSInterruptException:
        rospy.logerr('Subscriber is error');
        pass;
