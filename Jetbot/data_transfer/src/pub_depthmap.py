#!/usr/bin/env python3

import pyrealsense2 as rs 
import numpy as np 
import cv2 
import math
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from std_msgs.msg import Bool

wifi_connection = True
        



def callback2(message2: Bool):
    global wifi_connection
    wifi_connection = message2.data

def depth_cal():
    
    topic = '/img_c';
    topic2 = '/connection'
    topic3 = '/img_d'
    node = rospy.init_node("camera_node",anonymous=True);
    publisher = rospy.Publisher(topic, CompressedImage,queue_size=100);
    publisher2 = rospy.Publisher(topic3, CompressedImage,queue_size=100);

    rate = rospy.Rate(10);    
    
    pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)
    cfg.enable_stream(rs.stream.depth,640,480,rs.format.z16,30)

    pipe.start(cfg)

    #cv2.namedWindow('rgb')
    #cv2.setMouseCallback('rgb', mouse_cb)
    rospy.Subscriber(topic2,Bool, callback2);

    while not rospy.is_shutdown():
        frame = pipe.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        color_image = cv2.resize(color_image, (640,480), interpolation= cv2.INTER_LINEAR)
        
        depth_image2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        depth_image2 = cv2.resize(depth_image2, (640,480), interpolation= cv2.INTER_LINEAR)
        
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', color_image)[1]).tostring()
        
        msg2 = CompressedImage()
        msg2.header.stamp = rospy.Time.now()
        msg2.format = "jpeg"
        msg2.data = np.array(cv2.imencode('.jpg', depth_image2)[1]).tostring()
        
        if(wifi_connection==True):
            publisher.publish(msg);
            publisher2.publish(msg2);
            # print("image publishing....")

        #rate.sleep();
        color_image = cv2.resize(color_image, (640,480), interpolation= cv2.INTER_LINEAR)

        #cv2.imshow('rgb', color_image)
        #cv2.imshow('depth1',depth_image)
        #cv2.imshow('depth2',depth_image2)

        if cv2.waitKey(1) == ord('q'):
            break
    pipe.stop()
    
    
if __name__ == "__main__":
    try:
        depth_cal()
        
    except:
        #rospy.logerr(e);
        print('Error')
        pass;
        
