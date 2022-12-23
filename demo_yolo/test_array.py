#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, PointCloud
from std_msgs.msg import Float32,Float32MultiArray

def callback(data):
    #a.append(data.data)
    print(data.data)



def tell_array():
    rospy.init_node('center', anonymous=True)
    rospy.Subscriber('center', Float32MultiArray,callback)
    rospy.spin()

if __name__ == '__main__':
    tell_array()