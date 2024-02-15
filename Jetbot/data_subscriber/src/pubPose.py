#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from unity_robotics_demo_msgs.msg import RbtPose
from sensor_msgs.msg import LaserScan
from unity_robotics_demo_msgs.msg import LidarScan
    
rPosition = None
rOrientation = None
linear_velocity = None
angular_velocity = None

# lidar_data = None

def odom_callback(msg):
    
    global rPosition,rOrientation,linear_velocity,angular_velocity
    
    rPosition = msg.pose.pose.position
    rOrientation = msg.pose.pose.orientation
    linear_velocity = msg.twist.twist.linear
    angular_velocity = msg.twist.twist.angular
    #print(rPosition.x)
    
# def scan_callback(msg2):
#     global lidar_data; 
    
#     lidar_data = msg2 
    
    
def main():

    
    topic1 = '/odom';
    topic2 = '/pos_robt'
    # topic3 = '/scan'
    # topic4 = '/ldata'
    
    rospy.init_node('pose_subscriber')
    rospy.Subscriber(topic1, Odometry, odom_callback)
    # rospy.Subscriber(topic3, LaserScan, scan_callback)
    
    pub = rospy.Publisher(topic2, RbtPose,queue_size=10)
    # pub2 = rospy.Publisher(topic4, LidarScan,queue_size=10)

    
    while not rospy.is_shutdown():
        
        lower_bound = 0
        upper_bound = 13.0
        
        if rPosition is not None:
            
            #print(rPosition.x)
            msg1 = RbtPose() 
            msg1.header.stamp = rospy.Time.now()
            msg1.header.frame_id = "/odom"
            msg1.pos_X = round(rPosition.x, 4)
            msg1.pos_Y = round(rPosition.y, 4)
            msg1.pos_Z = round(rPosition.z, 4)
            
            msg1.rot_X = round(rOrientation.x, 4)
            msg1.rot_Y = round(rOrientation.y, 4)
            msg1.rot_Z = round(rOrientation.z, 4)
            msg1.rot_W = round(rOrientation.w, 4)

            #print(msg1)
            pub.publish(msg1)
        
        # if lidar_data is not None:
            
            
            
        #     msg2 = LidarScan()
            
        #     msg2.header = lidar_data.header
        #     msg2.angle_min = lidar_data.angle_min
        #     msg2.angle_max = lidar_data.angle_max
        #     msg2.angle_increment = lidar_data.angle_increment
        #     msg2.time_increment = lidar_data.time_increment
        #     msg2.scan_time = lidar_data.scan_time
        #     msg2.range_min = lidar_data.range_min
        #     msg2.range_max = lidar_data.range_max
            
        #     msg2.intensities = lidar_data.intensities
            
            
            
        #     filtered_data = [x if lower_bound <= x <= upper_bound else 0 for x in lidar_data.ranges]
        #     filtered_data = tuple(filtered_data)
        #     first_range = filtered_data[:287]  # This gets data from position 1 to 287 (0-based indexing)
        #     second_range = filtered_data[861:1146] 
        #     combined_data =  second_range + first_range
            
        #     msg2.ranges = filtered_data
            
        #     pub2.publish(msg2)
        #     print(len(filtered_data))
            

   

if __name__ == '__main__':

    try:
        main();
    
    except Exception as e:
       rospy.logerr(e);
       pass;