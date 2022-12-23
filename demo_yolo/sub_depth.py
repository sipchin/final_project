#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, PointCloud
from std_msgs.msg import Float32,Float32MultiArray

def callback_depth(data):
    #a.append(data.data)
    print(data.data[320])
    

def tell_depth():
    rospy.init_node('depth', anonymous=True)
    rospy.Subscriber('/camera/depth/image', Image,callback_depth)
    rospy.spin()

def callback_coor(data):
    #a.append(data.data)
    print(data.data[0])
    callback_depth(data.data[0],data.data[1])


def tell_coor():
    rospy.init_node('center', anonymous=True)
    rospy.Subscriber('center', Float32MultiArray,callback_coor)
    rospy.spin()

if __name__ == '__main__':
    #tell_coor()
    tell_depth()