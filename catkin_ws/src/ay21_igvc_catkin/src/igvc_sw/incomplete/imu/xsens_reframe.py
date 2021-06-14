#!/usr/bin/env python
# license removed for brevity
import rospy
from sensor_msgs.msg import Imu
from marti_sensor_msgs.msg import Gyro
import copy

imuData = Imu()

def callback(data):
    global imuData
    imuData = data


def talker():
    imupub = rospy.Publisher('/localization/imu/reframe', Imu, queue_size=10)
    yawpub = rospy.Publisher('/localization/yaw_rate', Gyro, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rospy.Subscriber("/localization/imu/raw", Imu, callback)

    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
        if imuData.header.seq == 0:
            pass
        else:
            msg=imuData # Establishes msg as the variable with the raw imu data from the subscriber
            msg.header.frame_id = "/imu" # Sets the IMU data into the IMU frame
            imupub.publish(msg) # Publishes the IMU data to /localization/imu/reframe
            yawMsg=Gyro()
            yawMsg.header.stamp = rospy.Time.now()
            yawMsg.header.frame_id = "/imu" # Sets the Gyro data into the IMU frame
            yawMsg.angular_rate = msg.angular_velocity.z # Fills out the Gyro data with the z direction angular velocity from the IMU data
            yawMsg.variance = 0.0004 # TODO check if this the best value. Sets the variance to an acceptable value   
            yawpub.publish(yawMsg) # Publishes the new yawMsg to the /localization/yaw_rate topic to satisfy the yaw rate  
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
        
        '''
        
        marti_sensor_msgs/Gyro
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
float64 angular_rate
float64 variance

        
        '''
