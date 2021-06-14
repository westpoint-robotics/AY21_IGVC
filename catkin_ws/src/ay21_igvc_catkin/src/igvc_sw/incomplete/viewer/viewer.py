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

### Global values ###
GUI = False # in the future implement gui
TITLE = "------------AY21 Controller------------" # title message
SYSTEM_MESSAGE = "" # system message
prev_message = "" # initialize prev_message
mode = 0 # initialize mode
speed = 0
enabled = False
enabled_change = False
shift_cmd = PacmodCmd()
brake_cmd = PacmodCmd()

self_drive_options = """ 

OPTIONS:
* E-Stop Qualification:                '1'
* Straight Lane Keeping Qualification: '2'
* Left Turn Qualification:             '3'
* Right Turn Qualification:            '4'
* Stop Sign Detection Qualification    '5'
* Full Self-drive                      '6'
"""

parking_options = """ 

OPTIONS:
* Pull in:                '1'
* Pull out:               '2'
* Parallel park:          '3'

"""

### Modes ###
modes = {
    0: "Manual drive",
    1: "Teleop",
    2: "Self-drive",
    21: "E-Stop Qualification",
    22: "Straight Lane Keeping Qualification",
    23: "Left Turn Qualification",
    24: "Right Turn Qualification",
    25: "Stop Sign Detection Qualification",
    26: "Full Self-drive",
    3: "Parking",
    31: "Pull in",
    32: "Pull out",
    33: "Parallel park",
    7: "E-Stop (kill)",
}

def get_key_and_determine_mode():
    global mode
    char = sys.stdin.read(1)
    # self-drive input
    if mode == 2: 
        if char in '123456':
            mode = mode*10+int(char)
        elif char == '\n':
            mode = 26 # Full self drive
        elif char in 'cC':
            mode = 0
    # parking input
    elif mode == 3:
        if char in '123':
            mode = mode*10+int(char)
    else:
        # if down arrow pressed put in manual drive
        if char in 'mM':
            mode = 0
        # if right arrow pressed put in tele-op
        elif char in 'tT':
            mode = 1
        # if up arrow pressed put in self drive
        elif char in 'aAsS':
            mode = 2
        # parking
        elif char in 'pP':
            mode = 3
        # if back arrow pressed signal shutdown
        elif char in '\x1b':
            mode = 7


def set_system_message():
    global  modes, mode, SYSTEM_MESSAGE, speed
    SYSTEM_MESSAGE = ""
    SYSTEM_MESSAGE += "\n\r---- {} ----".format(modes[mode])
    if mode == 1:
        SYSTEM_MESSAGE += "\r\t-- Press 'A' for forward drive and 'B' for reverse. 'RT' for throttle and 'LT' for brake. Steer with left joystick. E-Stop is 'LB'."
    elif mode == 2:
        SYSTEM_MESSAGE += self_drive_options
        SYSTEM_MESSAGE += "\t-- enter run mode (ENTER for default self drive, 'c' to cancel): "
    elif mode in range(21, 27) or mode in range(31, 34): 
        if speed:# if speed is not 0.0
            SYSTEM_MESSAGE += "\n\r** vehicle still moving...cannot be put in {} mode!".format(modes[mode])
            mode = mode//10
    elif mode == 3:
        SYSTEM_MESSAGE += parking_options
    elif mode == 7:
        SYSTEM_MESSAGE += "\n\r*** E-Stop triggered...shutting down! ***"

def countdown_to_run(mode_num):
    global shift_cmd, brake_cmd
    if mode_num < 10:
        return
    tgt_shift = 3    # put in forward drive
    shift_cmd.ui16_cmd = tgt_shift
    shift_pub.publish(shift_cmd)
    print "\r\t-- running {} in\n\r\t\t5...".format(modes[mode_num])
    tm = rospy.get_time()
    n = 5
    while n:
        rospy.get_time()-tm>1.0:
        tm = rospy.get_time()
        print "\r\t\t{}...".format(n)
        n -= 1
    print "\r\t-- RUNNING!"
    brake_cmd.f64_cmd = 0
    brake_pub.publish(brake_cmd)
    return

def cleanup():
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def delay(dtm):
  ctm = rospy.get_time()
  while rospy.get_time()-ctm < dtm:
    pass
  return

def speed_callback(msg):
    global speed
    speed = msg.data

def stop_vehicle():
    global speed
    throttle = PacmodCmd()
    throttle.f64_cmd = 0.0
    brake = PacmodCmd()
    kp = 0.25
    rate = rospy.Rate(10)
    while speed > 0.01:
        throttle_pub.publish(throttle)
        brake_val = kp*speed
        if brake_val > 0.8:
            brake_val = 0.8
        elif brake_val < 0.60:
            brake_val = 0.60
        #brake_val = 0.75
        brake.f64_cmd = brake_val
        brake_pub.publish(brake)
        rate.sleep()
    brake.f64_cmd = 0.65
    brake_pub.publish(brake)
    return

def estop_callback(msg):
    if msg.data:
        print "\n\r*** E-Stop triggered...shutting down! ***"
        stop_vehicle()
        enable_pub.publish(False)
        ## shutdown node
        rospy.signal_shutdown("E-Stop pressed: killing ROS")
        #raise KeyboardInterrupt
        sys.exit()

def enable_callback(msg):
    global enabled, enabled_change
    enabled_change = enabled ^ msg.data # bitwise XOR
    if enabled_change and mode > 10:
        print "\r\n\t ** Manual overwrite detected..."
    enabled = msg.data

def joy_callback(msg):
    global mode, last_joy_tm
    tm = rospy.get_time()
    if mode == 0:
        if tm-last_joy_tm>0.2:  # implement debounce
            last_joy_tm = tm
            # if LB pressed signal shutdown
            if msg.buttons[4]:
                mode = 7
            # if down arrow pressed put in manual drive
            elif msg.axes[7] == -1.0:
                mode = 0
            # if right arrow pressed put in tele-op
            elif msg.axes[6] == -1.0:
                mode = 1
            # if up arrow pressed put in self drive
            elif msg.axes[7] == 1.0:
                mode = 2
            

if __name__ == "__main__":
    global mode, TITLE, SYSTEM_MESSAGE, speed, enabled, enabled_change

    print TITLE
    # Initiate controller node
    rospy.init_node("master_controller", anonymous = True)
    rate = rospy.Rate(10)

    # ROS Publishers
    mode_pub = rospy.Publisher('/gem/operation_mode', Int8, queue_size=10)
    enable_pub = rospy.Publisher('/pacmod/as_rx/enable', Bool, queue_size=10)
    shift_pub = rospy.Publisher('/pacmod/as_rx/shift_cmd', PacmodCmd, queue_size=10)
    #steer_pub = rospy.Publisher('/pacmod/as_rx/steer_cmd', PositionWithSpeed, queue_size=10)
    #turn_sig_pub = rospy.Publisher('/pacmod/as_rx/turn_cmd', PacmodCmd, queue_size=10)s

    # ROS Subscribers
    rospy.Subscriber('/gem/eStop', Bool, estop_callback)
    rospy.Subscriber('/pacmod/as_tx/enable', Bool, enable_callback)
    rospy.Subscriber('pacmod/as_tx/vehicle_speed', Float64, speed_callback)
    rospy.Subscriber('/joy', Joy, joy_callback)

    
    # Termios set up
    ### Key press code adapted from https://www.darkcoding.net/software/non-blocking-console-io-is-not-possible/ ###
    key_delay = 0.2
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    rospy.on_shutdown(cleanup)
    tty.setcbreak(sys.stdin.fileno())
    while not rospy.is_shutdown():
        try:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                get_key_and_determine_mode()
                delay(key_delay)
                set_system_message()
                if not SYSTEM_MESSAGE == prev_message:
                    print SYSTEM_MESSAGE
                prev_message = SYSTEM_MESSAGE
                countdown_to_run(mode)
                enable_pub.publish(mode > 10)
                mode_pub.publish(mode) 
        except:
            pass

        finally:
            rate.sleep()
        