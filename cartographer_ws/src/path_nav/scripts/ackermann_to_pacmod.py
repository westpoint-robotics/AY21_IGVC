#!/usr/bin/env python

# Author: Curtis Manore

import rospy, math
from geometry_msgs.msg import Twist
from ackermann_msgs.msg import AckermannDriveStamped
from std_msgs.msg import Int8, String, Float64, Float32, Bool
from pacmod_msgs.msg import PositionWithSpeed
from pacmod_msgs.msg import PacmodCmd

enable_pub = rospy.Publisher('/pacmod/as_rx/enable', Bool, queue_size=10)
shift_pub = rospy.Publisher('/pacmod/as_rx/shift_cmd', PacmodCmd, queue_size=10)

def publishSteering(steeringAngle, steeringVel):
    steer_pub = rospy.Publisher('/pacmod/as_rx/steer_cmd', PositionWithSpeed, queue_size=10)
    steer_msg = PositionWithSpeed()
    
    steer_msg.angular_position = steeringAngle
    steer_msg.angular_velocity_limit = steeringVel
    enable_pub.publish(True)
    steer_pub.publish(steer_msg)
    rospy.loginfo("Success")
    

def cmd_callback(data):
    # control and publish steering first
    steeringAngle = data.drive.steering_angle #in radians
    steeringVel = data.drive.steering_angle_velocity # rad/s
    #rospy.loginfo("Success")


    publishSteering(steeringAngle, steeringVel)
    





if __name__ == '__main__': 
  try:
    
    rospy.init_node('ackermann_drive_to_pacmod')
        
    ackermann_cmd_topic = rospy.get_param('~ackermann_cmd_topic', '/ackermann_cmd')
    twist_cmd_topic = rospy.get_param('~twist_cmd_topic', '/cmd_vel') 
    
    rospy.Subscriber(ackermann_cmd_topic, AckermannDriveStamped, cmd_callback, queue_size=1)
    #pub = rospy.Publisher(ackermann_cmd_topic, AckermannDriveStamped, queue_size=1)
    
    #rospy.loginfo("Node 'cmd_vel_to_ackermann_drive' started.\nListening to %s, publishing to %s. Frame id: %s, wheelbase: %f", "/cmd_vel", ackermann_cmd_topic, frame_id, wheelbase)
    
    rospy.spin()
    
  except rospy.ROSInterruptException:
    pass

