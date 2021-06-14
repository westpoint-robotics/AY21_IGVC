#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <geometry_msgs/PointStamped.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "my_tf_listener");

  ros::NodeHandle node;

//  ros::service::waitForService("spawn");
//  ros::ServiceClient add_turtle = 
//    node.serviceClient<turtlesim::Spawn>("spawn");
//  turtlesim::Spawn srv;
//  add_turtle.call(srv);

//  ros::Publisher turtle_vel = 
//    node.advertise<turtlesim::Velocity>("turtle2/command_velocity", 10);

  tf::TransformListener listener;

  ros::Rate rate(10.0);
  while (node.ok()){
    tf::StampedTransform transform;

    try {
    listener.waitForTransform("base_link", "imu", ros::Time(0), ros::Duration(10.0) );
    listener.lookupTransform("base_link", "imu", ros::Time(0), transform);

} catch (tf::TransformException ex) {
    ROS_ERROR("%s",ex.what());
}

//    turtlesim::Velocity vel_msg;
//    vel_msg.angular = 4.0 * atan2(transform.getOrigin().y(),
//                                transform.getOrigin().x());
//    vel_msg.linear = 0.5 * sqrt(pow(transform.getOrigin().x(), 2) +
//                                pow(transform.getOrigin().y(), 2));
//    turtle_vel.publish(vel_msg);

    rate.sleep();
  }
  return 0;
};
