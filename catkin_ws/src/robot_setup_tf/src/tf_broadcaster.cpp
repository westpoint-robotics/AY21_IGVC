#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "robot_tf_publisher");
  ros::NodeHandle n;

  ros::Rate r(180);

  tf::TransformBroadcaster broadcaster;

  while(n.ok()){
//    broadcaster.sendTransform(
//      tf::StampedTransform(
//        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 0.29)),
//        ros::Time(0),"base_link", "imu"));
    broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 0.29)),
        ros::Time::now(),"base_link", "imu"));
//    broadcaster.sendTransform(
//      tf::StampedTransform(
//        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 1.6852)),
//        ros::Time(0),"base_link", "velodyne"));
    broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.0, 0.0, 1.6852)),
        ros::Time::now(),"base_link", "velodyne"));
    r.sleep();
  }
}

