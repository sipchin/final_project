#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Float32,Float32MultiArray,String
from cv_bridge import CvBridge
import os
import rospkg

path = rospkg.RosPack().get_path("demo_yolo")

os.chdir(path)

class ObjectDetection(object):

    def __init__(self):
        self.bridge = CvBridge()
        rospy.init_node("person_detect", anonymous=True)
        rospy.Subscriber("/camera/rgb/image_color", Image, self.update_frame_callback)
        rospy.wait_for_message("/camera/rgb/image_color", Image)

    def update_frame_callback(self, data):
        self.image = self.bridge.imgmsg_to_cv2(data, desired_encoding="bgr8") 

    def main(self):
        net = cv2.dnn.readNet("weight/yolov3.weights", "cfg/yolov3.cfg")
        classes = []
        with open("cfg/coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()] 

        output_layers = [layer_name for layer_name in net.getUnconnectedOutLayersNames()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        
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
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    if label == "person":
                        color = colors[i]
                        cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
                        c_x = x+w/2
                        c_y = y+h/2
                        print(c_x)
                        a = 'Not center'
                        if 320 < c_x and c_x < 370:
                            a = "center"
                        print(a)
                        self.pub_cmd(a)
                        cv2.putText(frame, label, (x, y - 5), font, 1, color, 1)
                        cv2.imshow("Image", frame)
                        key = cv2.waitKey(1)
                        if key == 27:
                         break
    def pub_cmd(self,data):
        pub = rospy.Publisher('tell_center', String, queue_size=10)
        rate = rospy.Rate(10)
        rospy.loginfo(data)
        pub.publish(data)
        rate.sleep()



if __name__ == "__main__":
    obj = ObjectDetection()
    obj.main()