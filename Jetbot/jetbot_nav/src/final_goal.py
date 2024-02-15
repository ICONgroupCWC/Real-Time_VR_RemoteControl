#!/usr/bin/env python3

import os
import rospy
import numpy as np
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Path


wifi_conct = True
goal_pos = None
current_pos = PoseWithCovarianceStamped()

current_goal = PoseStamped()

flag1 = False
flag2 = False

pathDta = None

def callback1(message1: PoseStamped):
    global goal_pos ,flag1
    goal_pos = message1
    flag1 = True

   
def callback2(message1: Bool):
    global wifi_conct
    wifi_conct = message1.data
   


def callback3(message1: Odometry):
    global current_pos
    current_pos.header.frame_id = "map"
    current_pos.pose.pose.position.x = message1.pose.pose.position.x
    current_pos.pose.pose.position.y = message1.pose.pose.position.y
    current_pos.pose.pose.orientation.x = message1.pose.pose.orientation.x
    current_pos.pose.pose.orientation.y = message1.pose.pose.orientation.y
    current_pos.pose.pose.orientation.z = message1.pose.pose.orientation.z
    current_pos.pose.pose.orientation.w = message1.pose.pose.orientation.w


def callback4(message1):
    global pathDta, flag2
    if len(message1.poses)>10:
        flag2 = True
        pathDta = message1

    

def main():
    goal_reach = True

    corection = True
    current_location_flag1 = True

    topic1 = '/move_base_simple/final_goal';
    topic2 = '/move_base_simple/goal';
    topic3 = '/connection'
    topic4 = '/odom'
    topic5 = '/initialpose'

    topic6 = '/move_base/NavfnROS/plan'
    topic7 = '/PathData'
    
    rospy.init_node('target_pos',anonymous=True);
    
    rospy.Subscriber(topic1,PoseStamped, callback1);
    rospy.Subscriber(topic3,Bool, callback2);
    rospy.Subscriber(topic4,Odometry,callback3)
    rospy.Subscriber(topic6,Path,callback4)
  
    
    pub1 = rospy.Publisher(topic2, PoseStamped,queue_size=10);
    pub2 = rospy.Publisher(topic5,PoseWithCovarianceStamped,queue_size=10)
    pub3 = rospy.Publisher(topic7, Path,queue_size=10);
    global flag1, pathDta, flag2
    while not rospy.is_shutdown():
        
        if(wifi_conct == True):

            if(flag1==True and goal_pos is not None ):
                pub1.publish(goal_pos)

                while(flag2 == False):
                    print("wait...")

                if(flag2 == True):
                    print(len(pathDta.poses))
                    print("ok")
                    pub3.publish(pathDta)

                current_goal.header = current_pos.header
                current_goal.pose = current_pos.pose.pose
                pub1.publish(current_goal)
                print("set goal");
                flag1 = False
                flag2 = False


            #pub2.publish(current_pos)
            
            if(current_location_flag1==False):
                current_goal.header = current_pos.header
                current_goal.pose = current_pos.pose.pose
                pub1.publish(current_goal)

                
            corection = True
            current_location_flag1 = True
            # print("connection ok")
        elif(wifi_conct==False and goal_pos is not None):
            if(corection==True):
                pub2.publish(current_pos)
                pub1.publish(goal_pos)
                print("connection loss")
           
            if(current_pos.pose.pose==goal_pos.pose):
                print("target reach now")
                if(goal_reach==True):
                    os.system("aplay -D hw:2,0 ~/final.wav")
                    print("target reach now")
                    goal_reach = False
            else:
                goal_reach = True

            corection = False
            current_location_flag1 = False
            
            


   



if __name__ == '__main__':

    try:
        main()
       
    except rospy.ROSInterruptException:
        rospy.logerr('Subscriber is error');
        pass;
