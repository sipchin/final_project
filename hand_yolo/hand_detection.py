#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float32MultiArray
from cv_bridge import CvBridge
import os
import rospkg

path = rospkg.RosPack().get_path("hand_yolo")

os.chdir(path)

class HandDetect(object):

    def __init__(self):
        self.bridge = CvBridge()
        rospy.init_node("hand_detect", anonymous=True)
        rospy.Subscriber("/camera/rgb/image_color", Image, self.update_frame_callback)
        rospy.wait_for_message("/camera/rgb/image_color", Image)

    def update_frame_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8") 

    def main(self):
        net = cv2.dnn.readNet("weights/cross-hands.weights", "cfg/cross-hands.cfg")
        classes = []
        with open("cfg/coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()] 

        output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
        colors = np.random.uniform(0, 255, 1000)
        
        while not rospy.is_shutdown():
            frame = self.image
            height, width, channels = frame.shape
            blob = cv2.dnn.blobFromImage(frame, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
            net.setInput(blob)
            outputs = net.forward(output_layers)
            boxes = []
            confs = []
            class_ids = []
            for output in outputs:
                for detect in output:
                    scores = detect[5:]
                    class_id = np.argmax(scores)
                    conf = scores[class_id]
                    if conf > 0.3:
                        center_x = int(detect[0] * width)
                        center_y = int(detect[1] * height)
                        w = int(detect[2] * width)
                        h = int(detect[3] * height)
                        x = int(center_x - w/2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confs.append(float(conf))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
            font = cv2.FONT_HERSHEY_PLAIN
            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[0]
                    label = str(classes[class_ids[i]])
                    color = colors[i]
                    center_x = x+w/2
                    center_y = y+h/2
                    center = Float32MultiArray(data=[center_x,center_y])
                    print(center)
                    if center_y < 200:
                        a = 'Raise hand'
                        pub = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=1)
                        rate = rospy.Rate(100)
                        rot = Twist()
                        rot.linear.x = 1.5
                        pub.publish(rot)
                        print(a)
                    elif center_y > 200:
                        a = 'No raise hand'
                        print(a)
                    self.pub_cmd(a)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                    cv2.putText(frame, label, (x, y - 5), font, 1, color, 1)
                    print()
            cv2.imshow("Image", frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    

    def pub_cmd(self,data):
        pub = rospy.Publisher('command', String , queue_size=10)
        rate = rospy.Rate(10)
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()

if __name__ == "__main__":
    obj = HandDetect()
    obj.main()
