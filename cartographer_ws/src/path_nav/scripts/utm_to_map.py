#!/usr/bin/env python
import rospy
import tf
from LatLongUTMconversion import LLtoUTM, UTMtoLL
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped, Pose



if __name__ == '__main__': 
  try:
    
    rospy.init_node('utm_to_map')
    
    #rospy.Subscriber('/fix', NavSatFix, callback, queue_size=10)
    gpsFix = rospy.wait_for_message('/fix', NavSatFix)
    lat = gpsFix.latitude
    lon = gpsFix.longitude
    
    rate = rospy.Rate(50.0)
    
    (zone,crnt_utm_e,crnt_utm_n) = LLtoUTM(23, float(lat), float(lon))
    br = tf.TransformBroadcaster()

    while not rospy.is_shutdown():
        br.sendTransform((crnt_utm_e, crnt_utm_n, 0),
                         (0,0,0,1),
                         rospy.Time.now(),
                         "map",
                         "utm")
        rate.sleep()
    #rospy.spin()
    
  except rospy.ROSInterruptException:
    pass
