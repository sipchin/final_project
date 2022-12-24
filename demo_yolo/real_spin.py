#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from std_msgs.msg import Float32,Float32MultiArray,String
from cv_bridge import CvBridge
import os

class robot_spin(object):
    def __init__(self):
        self.center = ''
        self.new_center = ''
        self.x = 0
        rospy.init_node('rotate_itself')
        rospy.Subscriber('tell_center', String, self.center_callback)
        rospy.wait_for_message('tell_center', String)
        rospy.Subscriber('new_cen', String, self.new_center_callback)
        rospy.wait_for_message('new_cen', String)

    def center_callback(self,data):
        #print(data.data)
        self.center = data.data
    
    def new_center_callback(self,data):
        self.new_center = data.data
    
    def main(self):
        while not rospy.is_shutdown():
            if self.center == 'Center':
                pub = rospy.Publisher('tell_hand', String, queue_size=1)
                print("There you are")
                command = 'Do hand detect'
                rate = rospy.Rate(10)
                rospy.loginfo(command)
                pub.publish(command)
                #rate.sleep()
            elif self.center == 'Not center':
                if self.new_center == 'Not new center':
                    #Adjust depending on last seen x value.
                    if self.x >= 320:
                        print("Turning right")
                        pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                        rate = rospy.Rate(100)
                        rot = Twist()
                        rot.angular.z = -0.5
                        pub.publish(rot)
                    elif self.x <= 320:
                        print("Turning left")
                        pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                        rate = rospy.Rate(100)
                        rot = Twist()
                        rot.angular.z = 0.5
                        pub.publish(rot)

                    #Adjust with left spin always.
                    print("Where are you")
                    pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                    rate = rospy.Rate(100)
                    rot = Twist()
                    rot.angular.z = 0.5
                    pub.publish(rot)

                elif self.new_center == 'New center':
                    pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                    pub_cmd = rospy.Publisher('tell_hand', String, queue_size=1)
                    rate = rospy.Rate(100)
                    rot = Twist()
                    rot.angular.z = 0
                    pub.publish(rot)
                    command = 'Do hand detect'
                    rospy.loginfo(command)
                    pub_cmd.publish(command)
                    rate.sleep()

if __name__ == '__main__':
    main = robot_spin()
    main.main()



