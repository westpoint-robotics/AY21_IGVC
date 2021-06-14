#!/usr/bin/env python
import rospy
import tf
from LatLongUTMconversion import LLtoUTM, UTMtoLL
from geometry_msgs.msg import PoseStamped, Pose


def publishWaypoint(lat, lon):
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    (zone,crnt_utm_e,crnt_utm_n) = LLtoUTM(23, float(lat), float(lon))
    
    goal_pose_stamped = PoseStamped()
    goal_pose_stamped.header.stamp = rospy.Time.now()  
    goal_pose_stamped.header.frame_id = 'utm'   
    goal_pose_stamped.pose.position.x = crnt_utm_e                    
    goal_pose_stamped.pose.position.y = crnt_utm_n 
    #goal_pose_stamped = self.tf1_listener.transformPose('husky/map', goal_pose_stamped) 
    goal_pose_stamped.pose.orientation.z = 0.0985357937255
    goal_pose_stamped.pose.orientation.w = 0.995133507302 
                                                                         
    pub.publish(goal_pose_stamped)



if __name__ == '__main__': 
  try:
    
    rospy.init_node('waypoint_to_moveGoal')
    
    print("Enter latitude: ")
    lat = input()
    print("Enter longitude: ")
    lon = input()
    
    publishWaypoint(float(lat), float(lon))
    
    
  except rospy.ROSInterruptException:
    pass
