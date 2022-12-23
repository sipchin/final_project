#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image, PointCloud
from std_msgs.msg import Float32,Float32MultiArray, Int32MultiArray

class GetValue(object):

    def __init__(self):
        rospy.init_node('center_value', anonymous=True)
        # rospy.Subscriber('center_x', Float32, self.callback_x)

    def main(self):
        self.a = [0,0]
        self.array_pub = Int32MultiArray(data=[self.a])
        rospy.Subscriber('center_x', Float32, self.callback_x)
        rospy.wait_for_message('center_x', Float32)
        rospy.Subscriber('center_y', Float32, self.callback_y)
        rospy.wait_for_message('center_y', Float32)
        print(self.array_pub)
        self.pub_arr(self.array_pub)
        rospy.spin()
    
    def pub_arr(self,data):
        pub = rospy.Publisher('center_depth', Int32MultiArray , queue_size = 10)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rospy.loginfo(data)
            pub.publish(data)
            rate.sleep()

    def callback_x(self,data):
        x = data.data
        self.a[0] = data.data
        #print('This is x')
        #print(data.data)

    def callback_y(self,data):
        #print('This is y')
        print(data.data)
        self.a[1] = data.data


    
if __name__ == '__main__':
    main = GetValue()
    main.main()
