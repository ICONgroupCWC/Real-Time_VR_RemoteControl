#!/usr/bin/python3

import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
import time
import math

class LowLevelCtrl():
    def __init__(self, wheel_distance=0.162, wheel_diameter=0.065):
        rospy.loginfo("Setting Up the Node...")
        
        rospy.init_node('base_llc')

        self.PIN_LIGHT = 5
        self.PIN_HORN = 6
        self.gain = 0.75

        self.left_wheel_omega = 0
        self.right_wheel_omega = 0

        self._wheel_distance = wheel_distance
        self._wheel_radius = wheel_diameter / 2.0

        self.pos_left = 0
        self.pos_right = 0

        self.vel_linear = 0
        self.vel_angular = 0

        self._joint_stat      = JointState()
        self._velocity_msg    = Float32MultiArray()

        self.ros_pub_velocity_array = rospy.Publisher("/wheel_velocity", Float32MultiArray, queue_size=1)
 
        self.ros_pub_joint_stat     = rospy.Publisher("/joint_states", JointState, queue_size=10)


        rospy.loginfo("> Publisher corrrectly initialized")

        #--- Create the Subscriber to Twist commands
        self.ros_sub_twist          = rospy.Subscriber("/cmd_vel", Twist, self.set_actuators_from_cmdvel)
        
        rospy.loginfo("> Subscriber corrrectly initialized")

        #--- Get the last time e got a commands
        self._last_time_cmd_rcv     = time.time()
        self._timeout_s             = 2
        self.anglez                 = 0.00

        self.current_time = rospy.Time.now()
        self.last_time = rospy.Time.now()

        rospy.loginfo("Initialization complete")
        
    def set_actuators_from_cmdvel(self, message):
     
        self._last_time_cmd_rcv = time.time()
        self.vel_linear = message.linear.x
        self.vel_angular = message.angular.z 
        
        self.set_cmd_vel(message.linear.x * 1.0 ,message.angular.z *1.0)
        # rospy.loginfo("Got a command v = %2.1f  s = %2.1f"%(message.linear.x, message.angular.z))
        
    def set_cmd_vel(self, linear_speed, angular_speed):

        body_turn_radius = self.calculate_body_turn_radius(linear_speed, angular_speed)

        wheel = "right"
        right_wheel_turn_radius = self.calculate_wheel_turn_radius(body_turn_radius,
                                                                   angular_speed,
                                                                   wheel)

        wheel = "left"
        left_wheel_turn_radius = self.calculate_wheel_turn_radius(body_turn_radius,
                                                                  angular_speed,
                                                                  wheel)

        right_wheel_rpm = self.calculate_wheel_rpm(linear_speed, angular_speed, right_wheel_turn_radius)
        left_wheel_rpm = self.calculate_wheel_rpm(linear_speed, angular_speed, left_wheel_turn_radius)

        self.left_wheel_omega = left_wheel_rpm
        self.right_wheel_omega = right_wheel_rpm
        
    def calculate_body_turn_radius(self, linear_speed, angular_speed):
        if angular_speed != 0.0:
            body_turn_radius = linear_speed / angular_speed
        else:
            # Not turning, infinite turn radius
            body_turn_radius = None
        return body_turn_radius

    def calculate_wheel_turn_radius(self, body_turn_radius, angular_speed, wheel):

        if body_turn_radius is not None:
        
            if wheel == "right":
                wheel_sign = 1
            elif wheel == "left":
                wheel_sign = -1
            else:
                assert False, "Wheel Name not supported, left or right only."

            wheel_turn_radius = body_turn_radius + ( wheel_sign * (self._wheel_distance / 2.0))
        else:
            wheel_turn_radius = None
        
        return wheel_turn_radius

    def calculate_wheel_rpm(self, linear_speed, angular_speed, wheel_turn_radius):
        if wheel_turn_radius is not None:
            # The robot is turning
            wheel_rpm = 2.5 * (angular_speed * wheel_turn_radius) / self._wheel_radius
        else:
            # Its not turning therefore the wheel speed is the same as the body
            wheel_rpm = 1.5 * linear_speed / self._wheel_radius

        return wheel_rpm
    
    def send_velocity_msg(self):
        self._velocity_msg.data = [self.left_wheel_omega, self.right_wheel_omega, 50, 50, self.vel_angular, self.vel_linear] #=================================================
        self.ros_pub_velocity_array.publish(self._velocity_msg)

    def send_joint_stat_msg(self,left_p,right_p):
        self._joint_stat.header.stamp = self.current_time
        self._joint_stat.name       = ["wheel_left_joint","wheel_right_joint"]
        self._joint_stat.position   = [left_p, right_p]
        self._joint_stat.velocity   = [self.left_wheel_omega, self.right_wheel_omega]
        self._joint_stat.effort     = [0, 0]
        self.ros_pub_joint_stat.publish(self._joint_stat)
        
    @property
    def run(self):

        #--- Set the control rate
        rate = rospy.Rate(50)

        while not rospy.is_shutdown():
            #print self._last_time_cmd_rcv, self.is_controller_connected
            #if not self.is_controller_connected:
            #    self.set_actuators_idle()
            self.current_time = rospy.Time.now()
            dt = (self.current_time - self.last_time).to_sec()

            delta_pos_left = self.left_wheel_omega * dt
            delta_pos_right = self.right_wheel_omega * dt

            self.pos_left += delta_pos_left
            self.pos_right += delta_pos_right

            self.send_velocity_msg()
            self.send_joint_stat_msg(self.pos_left,self.pos_right)
            self.last_time = self.current_time
            rate.sleep()

if __name__ == "__main__":
    base_llc     = LowLevelCtrl()
    base_llc.run()