#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from unity_robotics_demo_msgs.msg import Pose


path_data = None
flag1 = True
def callback1(msg):
    global path_data ,flag1
    path_data = msg
    print("sub")
    flag1 = True
    
# def callback2():
#     global flag1
#     flag1 = True    


def main():

    
    topic1 = "/PathData"
    
    topic2 = "/pathPlan"
    topic3 = "/move_base_simple/final_goal"
    
    rospy.init_node('pose_subscriber')
    rospy.Subscriber(topic1, Path, callback1)
    # rospy.Subscriber(topic3, PoseStamped, callback2)
    
    pub = rospy.Publisher(topic2,Pose,queue_size=10);

    global flag1
    msg = Pose()
    
    while not rospy.is_shutdown():
        
        if path_data is not None and flag1 == True:
            print(len(path_data.poses))
            Z_point = []
            X_point = []
            for i in range(len(path_data.poses)):
                
                Z_point.append(path_data.poses[i].pose.position.x)
                X_point.append(path_data.poses[i].pose.position.y)
                
            
            msg.Xdata = X_point;
            msg.Zdata = Z_point;
            
            flag1 = False
            
        pub.publish(msg)
                
            
        
 
            

   

if __name__ == '__main__':

    try:
        main();
    
    except Exception as e:
       rospy.logerr(e);
       pass;