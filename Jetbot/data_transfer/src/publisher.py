#!/usr/bin/env python3

import rospy;
from geometry_msgs.msg import Twist

def publisher_hello():

    topic = '/cmd_vel';

    node = rospy.init_node("first_node1",anonymous=True);

    publisher = rospy.Publisher(topic, Twist,queue_size=10);

    rate = rospy.Rate(1000);

    while not rospy.is_shutdown():

        move_cmd = Twist()
        move_cmd.linear.x = 0
        move_cmd.linear.y = 0
        move_cmd.linear.z = 0
        
        move_cmd.angular.x = 0
        move_cmd.angular.y = 0
        move_cmd.angular.z = 1


        rospy.loginfo(move_cmd);
        publisher.publish(move_cmd);

        rate.sleep();

if __name__ == '__main__':
    try:
        publisher_hello();
    except:
        rospy.logerr('err in publishing');
        pass;