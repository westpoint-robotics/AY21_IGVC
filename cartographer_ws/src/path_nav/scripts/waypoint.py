#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped

def talker():
    pubPose = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)
    rospy.init_node('waypoint_goal', anonymous=True)
    pubPose.goalMsg = PoseStamped()
    pubPose.goalMsg.header.frame_id = "map"
    pubPose.goalMsg.header.stamp = rospy.Time.now()
    pubPose.goalMsg.pose.position.x = 5
    pubPose.goalMsg.pose.position.y = 10
    pubPose.goalMsg.pose.orientation.z = 0.0
    pubPose.goalMsg.pose.orientation.w = 1.0
    
    pubPose.publish(pubPose.goalMsg)
    rospy.loginfo("Success")
    
    '''
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
    '''

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
