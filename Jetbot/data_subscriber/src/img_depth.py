#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import warnings
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from unity_robotics_demo_msgs.msg import Img

img_np = np.zeros((480,640,3), np.uint8)
img_np_d = np.zeros((480,640,3), np.uint8)

def callback1(message):
    
    global img_np
    np_arr = np.fromstring(message.data,np.uint8)
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img_np = cv2.resize(img_np,(640,480), interpolation=cv2.INTER_LINEAR)

def callback2(message):
    
    global img_np_d
    np_arr = np.fromstring(message.data,np.uint8)
    img_np_d = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img_np_d = cv2.resize(img_np_d,(640,480), interpolation=cv2.INTER_LINEAR)    
    
    

def subscriber_hello():

    warnings.simplefilter("ignore",DeprecationWarning)
    topic1 = '/img_c';
    topic2 = '/img_d'
    topic3 = '/img_pub'
    topic4 = '/img_2'

    rospy.init_node('img_subscriber',anonymous=True);

    rospy.Subscriber(topic1,CompressedImage, callback1);
    rospy.Subscriber(topic2,CompressedImage, callback2);
    pub = rospy.Publisher(topic3, Img,queue_size=10)
    pub2 = rospy.Publisher(topic4, Image,queue_size=10)
    
    bridge = CvBridge()

    
    while not rospy.is_shutdown():
        
        rgb_image = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        ros_image = bridge.cv2_to_imgmsg(rgb_image, encoding='rgb8')
        #print(img_np_d.shape)
        
        img_h = cv2.hconcat([img_np,img_np_d])
        
        
        # img_com = cv2.resize(img_np_d,(160,120), interpolation=cv2.INTER_LINEAR) 
        msg = Img()#CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg',img_np)[1]).tostring()
        print("kaglh")
        
        
        pub.publish(msg)
        #pub2.publish(ros_image)
        cv2.imshow('RGB_&_depth',img_h)
        #cv2.imshow('img_depth',img_np_d)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

   

if __name__ == '__main__':

    try:
        subscriber_hello();
    except:
       rospy.logerr('Subscriber is error');
       pass;