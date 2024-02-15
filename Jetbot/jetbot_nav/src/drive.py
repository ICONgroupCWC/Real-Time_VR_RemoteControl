#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
import numpy as np
from geometry_msgs.msg import Twist
from numpy import interp
from std_msgs.msg import Bool

move_cmd = Twist()
save_map = False

wifi_conct = True

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
    
    
def callback2(message1: Bool):
    global wifi_conct
    wifi_conct = message1.data

    

def main():

    topic1 = '/joy';
    topic2 = '/cmd_vel';
    topic3 = '/connection'
        
    rospy.init_node('joy_sub',anonymous=True);
    pub = rospy.Publisher(topic2, Twist,queue_size=10);
   
    rospy.Subscriber(topic1,Joy, callback);
    rospy.Subscriber(topic3,Bool, callback2);
    
    while not rospy.is_shutdown():
        if(wifi_conct == True):
            # print("run")
        
            pub.publish(move_cmd)
        
            


   



if __name__ == '__main__':

    try:
        main()
       
    except rospy.ROSInterruptException:
        rospy.logerr('Subscriber is error');
        pass;
