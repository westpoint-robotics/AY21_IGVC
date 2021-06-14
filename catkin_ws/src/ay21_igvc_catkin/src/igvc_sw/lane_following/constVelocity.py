#!/usr/bin/env python

import rospy, sys, time
from std_msgs.msg import Int8, String, Float64, Float32, Bool
from pacmod_msgs.msg import PacmodCmd
state = 0
#Target Values
currentVelocity = 0.0
previousVelocity = 0.05
targetVelocity = 2.0#2.2352 #5MPH in m/s
signVelocity = 2.0#2.2352
whiteLineVelocity = 2.0#2.2352
error = 0.0
integralError = 0.0
derivativeError = 0.0
previousError = 0.0
previousIntegralError = 0.0
Kp = 1.0#0.8
Ki = 0.2
Kd = 0.0
throttle = 0.0
prevTime = 0.0
curtime = 0.0
controlMax = 10.0
controlMin = 0.0
MPH2MPS = 0.44704
integralMax = 2*MPH2MPS

currentGear = 0
stopsignDistance = 0
numStopLine = 0
numStopSign = 0
reactedToStopSign = False
prevstop = 0
prevline = 0 

#reactedToPerson = False
personXcor = 0.0
personYcor = 0.0
#added
barrelXcor = 0.0
barrelYcor = 0.0

potholeXcor = 0.0
potholeYcor = 0.0

barrelDone = False


merge_flag = rospy.Publisher('/merge_flag', Bool, queue_size = 10)
personDetected_pub= rospy.Publisher('/person/personDetected', Bool, queue_size = 10)

#end added
def state_callback(msg):
    global state
    state = msg.data
    if state == 7:
        rospy.signal_shutdown('killed by selfdrive manager')
        sys.exit()
        
def speedCallBack(msg):
    global currentVelocity
    currentVelocity = msg.data
    
def whiteLineCallback(msg):
    global whiteLineVelocity
    whiteLineVelocity = msg.data
    
def signCallback(msg):
    global signVelocity
    signVelocity = msg.data
    
def shiftCallBack(msg):
    global currentGear
    currentGear = msg.data
    print msg.data
    
def brakeCallBack(msg):
    print msg.data
    
def stoplineCallBack(msg):
    global numStopLine
    numStopLine = msg.data
    
def stopsignCallBack(msg):
    global numStopSign
    numStopSign = msg.data

def personXcorCallBack(msg):
    global personXcor
    personXcor = msg.data

def personYcorCallBack(msg):
    global personYcor
    personYcor = msg.data
#added
def barrelXcorCallBack(msg):
    global barrelXcor
    barrelXcor = msg.data

def barrelYcorCallBack(msg):
    global barrelYcor
    barrelYcor = msg.data

def potholeXcorCallBack(msg):
    global potholeXcor
    potholeXcor = msg.data 

def potholeYcorCallBack(msg):
    global potholeYcor
    potholeYcor = msg.data   

def barrelDoneCallBack(msg):
    global barrelDone
    barrelDone = msg.data      

#end added
def reactToStopSign():
    global reactedToStopSign, prevstop, prevline, numStopSign, numStopLine, targetVelocity, currentVelocity
    
    prevstop = max(numStopSign, prevstop)
    prevline = max(prevline, numStopLine)
    # "prevstop:" + str(prevline)
    if prevstop>0 and prevline>2:
        print "\r\t-- 1111111111111"
        if not reactedToStopSign:
            print "\r\t-- 2222222222222222222222"
            if currentVelocity == 0.0:
                prevstop = 0
                prevline = 0
                time.sleep(2)
                reactedToStopSign = True
                merge_flag.publish(True)
            else:
                targetVelocity = -1.0
                print "\r\t-- 33333333333333333333333333333"
        targetVelocity = -1.0
    if not numStopSign:
        reactedToStopSign = False

person_detected = False
personDetected = False
finishedPerson = False
def reactToPerson(): #once done, copy this into reactToPothole
    global personXcor, personYcor, targetVelocity, person_detected, personDetected, personDetected_pub, finishedPerson
    #if personYcor > 280:#540:#(personXcor > 350 and personXcor < 850 and personYcor > 540) or personYcor > 540: #personXcor > 490
    #    targetVelocity = -1.0
    #was 320
    if 1000 < personYcor: #(personXcor/45-600/45)**2/4 +300 < personYcor:
        print "person within range"
        #targetVelocity = -1.0
        person_detected = True
    if person_detected:
        personDetected = True        
        #targetVelocity = -1.0
    else:
        personDetected = False 
        finishedPerson = True
        #targetVelocity = 2.2352
    personDetected_pub.publish(personDetected) 
    
#added
barrel_detected = False
def reactToBarrel(): #exact same as person
    global numbarrel, barrelXcor, barrelYcor, targetVelocity, barrel_detected
    #use for pulling in, pulling out andstopping at a barrel in the road, and the 300othole test
    if 370 < barrelYcor:#(barrelXcor/45-600/45)**2/4 + 330 < barrelYcor: #was at 300 for stop sign test # was 340 at merge left
    # was 300 for right turn
        print "barrel detected"
        targetVelocity = -1.0#was .7 
        barrel_detected = True
    if barrel_detected == True:
        targetVelocity = -1.0
        print " in barrel detected if loop "
    else:
        pass
        #targetVelocity = 2.2352
    #use for lane changing, moving around barrel, and parallel parking
    
def reactToBarrelTwo():
    global numbarrel, barrelXcor, barrelYcor, targetVelocity, barrel_detected, person_detected, personDetected, personDetected_pub, barrelDone
    #if personYcor > 280:#540:#(personXcor > 350 and personXcor < 850 and personYcor > 540) or personYcor > 540: #personXcor > 490
    #    targetVelocity = -1.0
    #was 340
    # was 370
    if 310< personYcor:#barrelYcor: #(personXcor/45-600/45)**2/4 +300 < personYcor:
        print "PERSON within range"
        #if 350 < barrelYcor:#barrelDone and 480 < barrelYcor:
        #    print "second barrel"
        #    targetVelocity = -1.0
        #targetVelocity = -1.0
        personDetected = True    
        #targetVelocity = -1.0
    if 440 < barrelYcor:#barrelDone and 480 < barrelYcor:
        print "barrel"
        targetVelocity = -1.5
    #else:
    #    personDetected = False 
        #targetVelocity = 2.2352
    personDetected_pub.publish(personDetected) 
    

def reactToPothole(): #exact same as person
    global potholeXcor, potholeYcor, targetVelocity
    if (potholeXcor/45-600/45)**2/3 +400 < potholeYcor:
        targetVelocity = -2.0 
    else:
        pass
        #targetVelocity = 2.2352

#end added
def velController():
    global currentVelocity, previousVelocity, targetVelocity, whiteLineVelocity, signVelocity, error, integralError, derivativeError, previousError, previousIntegralError, Kp, Ki, Kd, throttle, prevTime, curtime, controlMax, controlMin, MPH2MPS, integralMax, initialTime, finishedPerson
    
    prevTime = curtime
    curtime = rospy.get_time()
    dt = curtime-prevTime
    targetVelocity = (whiteLineVelocity + signVelocity)/2
    
    
    reactToStopSign()
        
    #if not finishedPerson:
    #    reactToPerson()
    
    #reactToBarrel()
    
    reactToBarrelTwo()

    #reactToPothole()
    
    error = targetVelocity - currentVelocity
    previousIntegralError = integralError
    integralError = (error * (dt) + integralError)
    if integralError > integralMax:
        integralError = integralMax
    elif integralError < -integralMax:
        intregralError = -integralMax
    derivativeError = currentVelocity - previousVelocity
    ep = (Kp * error)
    ei = (Ki * integralError)
    ed = (Kd * derivativeError)
    u = ep + ei + ed
    throttle = scale(u)
    brake = 0
    
    if u > controlMax:
        throttle = scale(controlMax)
        u -= previousIntegralError
        
    elif u < controlMin:
        brake = throttle
        throttle = scale(controlMin)
        u -= previousIntegralError
    previousError = error
    previousVelocity = currentVelocity
        
    return brake, throttle #brake, throttle
    
def scale(x):
    global controlMax
    u = (x*(1.0/controlMax))+.2
    if u > 1.0:
        u = 1.0
    return u
    
def reverseGear():
    pass
    
    

def constVelocity():
    global currentVelocity, previousVelocity, targetVelocity, error, integralError, derivativeError, previousError, previousIntegralError, Kp, Ki, Kd, throttle, prevTime, curtime, controlMax, controlMin, MPH2MPS, integralMax
    rospy.init_node('speed_controller', anonymous=True)
    accel_pub = rospy.Publisher('pacmod/as_rx/accel_cmd', PacmodCmd, queue_size = 10)
    brake_pub = rospy.Publisher('/pacmod/as_rx/brake_cmd', PacmodCmd, queue_size = 10)
    rospy.Subscriber('/pacmod/as_tx/vehicle_speed', Float64, speedCallBack)
    rospy.Subscriber('/stop_sign/potential_stop_line', Int8, stoplineCallBack)
    rospy.Subscriber('/stop_sign/number', Int8, stopsignCallBack)
    
    rospy.Subscriber('/person/xcor', Float32, personXcorCallBack)
    rospy.Subscriber('/person/ycor', Float32, personYcorCallBack)
    #added
    rospy.Subscriber('/barrel/xcor', Float32, barrelXcorCallBack)
    rospy.Subscriber('/barrel/ycor', Float32, barrelYcorCallBack)

    rospy.Subscriber('/pothole/xcor', Float32, potholeXcorCallBack)
    rospy.Subscriber('/pothole/ycor', Float32, potholeYcorCallBack)
    
    rospy.Subscriber('/barrel/done', Bool, barrelDoneCallBack)
    #end added
    #rospy.Subscriber('/pacmod/parsed_tx/brake_rpt', SystemRptFloat, brakeCallBack)
    shift_cmd = rospy.Publisher('/pacmod/as_rx/shift_cmd', PacmodCmd, queue_size = 10)
    pac_dict = {'drive':3, 'neutral':2, 'reverse':1, 'park':0}
    shift_to_PACMOD = PacmodCmd()
    shift_to_PACMOD.ui16_cmd = pac_dict['reverse']
    #rospy.Subscriber('/pacmod/parsed_tx/shift_rpt', Int8, shiftCallBack)
    #rospy.Subscriber('/stopsign/distance', Float64, stopsignCallBack)
    
    #rospy.Subscriber('/speed_applied', Float64, whiteLineCallBack)
    #rospy.Subscriber('/stop_speed', Float64, whiteLineCallBack)
    rospy.Subscriber('/selfdrive/state', Int8, state_callback)
    accel = PacmodCmd()
    accel.f64_cmd = 0
    brake = PacmodCmd()
    brake.f64_cmd = 0
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #shift_cmd.publish(shift_to_PACMOD)
        
        if state and not (10<=state<20 or state==3):
            #brake.f64_cmd = 0
            #brake_pub.publish(brake)
            #accel.f64_cmd = velController()
            #accel_pub.publish(accel)
            
            brake.f64_cmd, accel.f64_cmd = velController()
            #accel.f64_cmd = .5
            brake_pub.publish(brake)
            accel_pub.publish(accel)
        else:
            integralError = 0
        
        rate.sleep()
        
        
if __name__ == '__main__':
    try:
        constVelocity()
    except rospy.ROSInterruptException:
        pass    
