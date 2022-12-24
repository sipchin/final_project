#!/usr/bin/env python3
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Quaternion, Pose, Point
from std_msgs.msg import Float32, String

class move_to_goal(object):
    def __init__(self):
        self.a ='Raise Hand'
        #rospy.Subscriber('command', String, self.callback)
        #rospy.wait_for_message('command', String)
        rospy.on_shutdown(self.shutdown)
    
    def callback(self,data):
        print(data.data)
        self.a = data.data

    def move(self):
        if self.a == 'Raise Hand':
            move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
            rospy.loginfo("wait for the action server to come up")
            move_base.wait_for_server(rospy.Duration(5))
            goal = MoveBaseGoal()
            goal.target_pose.header.frame_id = 'base_footprint'
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = 0.5 #3 meters
            goal.target_pose.pose.orientation.w = 1.0 #go forward
            #start moving
            move_base.send_goal(goal)
            #allow TurtleBot up to 60 seconds to complete task
            success = move_base.wait_for_result(rospy.Duration(60))
            if not success:
                move_base.cancel_goal()
                rospy.loginfo("The base failed to move forward 3 meters for some reason")
            else:
                # We made it!
                state = move_base.get_state()
                self.shutdown()
                if state == GoalStatus.SUCCEEDED:
                    rospy.loginfo("The base moved 3 meters forward")

    def shutdown(self):
        stop_goal = MoveBaseGoal()
        self.move_base.send_goal(stop_goal)
        rospy.loginfo("Stop")

if __name__ == "__main__":
    move_to_goal.move()

    