#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from unity_robotics_demo_msgs.msg import Img
import cv2
import numpy as np
import warnings

img_np = np.zeros((480,640,3), np.uint8)

def callback(message: Img):
    
    global img_np
    np_arr = np.fromstring(message.data,np.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #img_np = cv2.resize(img_np,(640,480), interpolation=cv2.INTER_LINEAR)
    
    
    

def subscriber_hello():

    #warnings.simplefilter("ignore",DeprecationWarning)
    topic = '/img_c';

    rospy.init_node('img_subscriber',anonymous=True);

    rospy.Subscriber(topic,Img, callback);
    
    while not rospy.is_shutdown():
        print(img_np.shape)
        cv2.imshow('img',img_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

   

if __name__ == '__main__':

    try:
        subscriber_hello();
    except:
        rospy.logerr('Subscriber is error');
        pass;