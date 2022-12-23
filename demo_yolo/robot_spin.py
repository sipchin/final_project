#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Float32,Float32MultiArray,String
from cv_bridge import CvBridge
import os
import rospkg

class robot_spin(object):
    def __init__(self):
        self.a = ''
        rospy.init_node('rotate_itself')
        rospy.Subscriber('new_cen', String, self.command_callback)
        rospy.wait_for_message('tell_center', String)

    def command_callback(self,data):
        self.a = data.data
    
    def main(self):
        while not rospy.is_shutdown():
            if self.a == 'Not center':
                pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                rate = rospy.Rate(100)
                rot = Twist()
                rot.angular.z = 0.5
                pub.publish(rot)
            elif self.a == 'center':
                pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                rate = rospy.Rate(100)
                rot = Twist()
                rot.angular.z = 0
                pub.publish(rot)
            print(self.a)

            # while not rospy.is_shutdown():
            # pub.publish(rot)
            # rate.sleep()

if __name__ == '__main__':
    main = robot_spin()
    main.main()
