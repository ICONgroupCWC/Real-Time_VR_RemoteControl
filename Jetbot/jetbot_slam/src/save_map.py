#!/usr/bin/env python3
import os
import rospy
from std_msgs.msg import Bool


flag = False

def callback(message: Bool):
    global flag
    if(message.data==True):
        flag = True
    else:
        flag = False
        
   
    


    

def main():

    topic1 = '/save_map_cmd';
        
    rospy.init_node('save_map_node',anonymous=True);
   
    rospy.Subscriber(topic1,Bool, callback);
    
    my_check = True

    while not rospy.is_shutdown():

        if(flag==True and my_check==True):
            os.system("rosrun map_server map_saver -f ~/catkin_ws/src/demo_project/jetbot_slam/map/tellus_back")
            print("map saved")
            my_check=False

        elif(flag==False):
            my_check=True
        
            


   



if __name__ == '__main__':

    try:
        main()
       
    except rospy.ROSInterruptException:
        rospy.logerr('Subscriber is error');
        pass;
