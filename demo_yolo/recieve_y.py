#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, PointCloud
from std_msgs.msg import Float32,Float32MultiArray

def callback_x(data):
    #a.append(data.data)
    print('This is x')
    print(data.data)

def callback_y(data):
    print('This is y')
    print(data.data)


def tell_x():
    rospy.init_node('center_value', anonymous=True)
    rospy.Subscriber('center_x', Float32,callback_x)
    rospy.spin()

def tell_y():
    rospy.Subscriber('center_y', Float32, callback_y)
    rospy.spin()
    

if __name__ == '__main__':
    tell_x()
    tell_y()