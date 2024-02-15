#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

def callback(message: Int32):
    print(message.data)

def subscriber_hello():

    topic = '/motor/rset';

    rospy.init_node('first_subscriber',anonymous=True);

    rospy.Subscriber(topic,Int32, callback);

    rospy.spin();

if __name__ == '__main__':

    try:
        subscriber_hello();
    except:
        rospy.logerr('Subscriber is error');
        pass;