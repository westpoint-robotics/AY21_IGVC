#!/usr/bin/env python
#shebang required to run on ROS

import sys, select, termios, tty, os, time
import rospy
from subprocess import call
from std_msgs.msg import Float64, Int8, Bool
from sensor_msgs.msg import Joy
from pacmod_msgs.msg import PacmodCmd, PositionWithSpeed

turn_cmd = PacmodCmd()
shift_cmd = PacmodCmd()
steer_cmd = PositionWithSpeed()

GUI = False
TITLE = "-------------AY21 Controller-------------"

"""
Modes:
0: Manual drive
1: 
2: Self-drive
7: E-Stop
"""

def clear():
    # clears the shell window
    call("clear" if os.name == "posix" else 'cls')
    print TITLE

def display_mode():
    

def modeControl():
    pass




if __name__ == "__main__":
    print TITLE
    global GUI, 
    # Init controller node
    rospy.init_node("master_controller", anonymous = True)

    # ROS Publishers
    mode_pub = rospy.Publisher('/gem/operation_mode', Int8, queue_size=10)
    enable_pub = rospy.Publisher('/pacmod/as_rx/enable', Bool, queue_size=10)
    shift_pub = rospy.Publisher('/pacmod/as_rx/shift_cmd', PacmodCmd, queue_size=10)
    steer_pub = rospy.Publisher('/pacmod/as_rx/steer_cmd', PositionWithSpeed, queue_size=10)
    turn_sig_pub = rospy.Publisher('/pacmod/as_rx/turn_cmd', PacmodCmd, queue_size=10)s

    # ROS Subscribers
    rospy.Subscriber('/pacmod/as_tx/enable', Bool, enable_callback)
    rospy.Subscriber('/gem/eStop', Bool, estop_callback)
    rospy.Subscriber('pacmod/as_tx/vehicle_speed', Float64, speed_callback)
    rospy.Subscriber('/gem/mode_input', Int8, user_input_callback)
    rospy.Subscriber('/selfdrive/status', Int8, selfdrive_sig_callback)
    while not rospy.is_shutdown():
        pass