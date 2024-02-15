#!/usr/bin/env python3

import pyrealsense2 as rs 
import numpy as np 
import cv2 
import math
import rospy

refPt = np.zeros(2)
click = False
        

def depth_cal():
    node = rospy.init_node("camera_node",anonymous=True);
    pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)
    cfg.enable_stream(rs.stream.depth,640,480,rs.format.z16,30)

    pipe.start(cfg)

    pc = rs.pointcloud()
    points = rs.points()
    decimate = rs.decimation_filter()
    colorizer = rs.colorizer()


    while not rospy.is_shutdown():
        frame = pipe.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()
        

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        #print(type(depth_image))
        
        depth_image2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
    
        cv2.imshow('rgb', color_image)
        cv2.imshow('depth1',depth_image)
        cv2.imshow('depth2',depth_image2)

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
        