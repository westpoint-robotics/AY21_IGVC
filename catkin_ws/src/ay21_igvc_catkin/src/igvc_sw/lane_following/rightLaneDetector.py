#!/usr/bin/env python
#import the necessary packages
#this used to be colorFind.py
import rospy
import itertools
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
import cv2
import numpy as np
import math
from cv_bridge import CvBridge
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union, transform
bridge = CvBridge()

imgWidth = 1920
imgHeight = 1440
cv_image = np.zeros((imgWidth, imgHeight,3), np.uint8)
res = np.zeros((imgWidth, imgHeight,3), np.uint8)
image_size = (imgWidth, imgHeight)
numSectors = 4
state = [0] * (numSectors**2)

# initialize line structs
global right
#global frame
rightDetected = False
lastRightLine = None

# filter values for white lanes
hul=0
huh=20
sal=0
sah=20
val=235
vah=255

HSVLOW=np.array([hul,sal,val])
HSVHIGH=np.array([huh,sah,vah])

pub = rospy.Publisher('/cross_track_error',Float32,queue_size=1)
#pub = rospy.Publisher('/y_distance',Float32,queue_size=1)
pub_image_top_down = rospy.Publisher('/lane_detection_image_top_down',Image,queue_size=1)
pub_image_seek = rospy.Publisher('/lane_detection_image_seek',Image,queue_size=1)

#set up sector limits
wInt = int(1536/numSectors)
hInt = int(720/numSectors)
polyList = []

for y in range (0,numSectors):
    for x in range(0,numSectors):
        newPoly = Polygon([(x*wInt,y*hInt),((x+1)*wInt,y*hInt),((x+1)*wInt,(y+1)*hInt),(x*wInt,(y+1)*hInt)])
        polyList.append(newPoly)

def unwarp_lane(img):
    undist = img
    undist_orig = undist.copy()
    
    rad = 1.26
    length = 800
    x1 = 714
    y1 = 1429
    x2 = x1-int(length*math.cos(rad))
    y2 = y1-int(length*math.sin(rad))
    x4 = 1478
    y4 = 1185
    x3 = x4-int(length*math.cos(rad))
    y3 = y4-int(length*math.sin(rad))

    cv2.line(undist_orig, (x1,y1), (x2, y2), [255,0,0], 5)
    cv2.line(undist_orig, (x3,y3), (x4, y4), [255,0,0], 5)

    img = bridge.cv2_to_imgmsg(undist_orig,'bgr8')
    pub_image_seek.publish(img)

    src = np.float32([(x1,y1),(x2,y2),(x3,y3),(x4,y4)])


    dst = np.float32([(0,800),(0,0),(800,0),(800,800)])
    M = cv2.getPerspectiveTransform(src, dst)

    warped = cv2.warpPerspective(undist_orig, M, image_size)
    cropped = warped[0:800,0:800]
    img = bridge.cv2_to_imgmsg(cropped,'bgr8')
    pub_image_top_down.publish(img)
    return cropped, M


def find_lane(polyArray, contourArray, image):
    global rightDetected, lastRightLine

    #sort by closest to bottom, then closest to center
    #print str(polyArray)
    rights = sorted(sorted(list(zip(polyArray, contourArray)), key = lambda p: p[0].bounds[2]), key = lambda p: -p[0].bounds[3])
    
    coords = None
    
    if len(rights) > 0:
        coords = rights[0][0].exterior.coords.xy #get closest right lane
        print "in if loop"
#        cv2.fillConvexPoly(image, np.array(zip(x,y), 'int32'),(255,255,0))
#        myCoeffs = np.polyfit(x,y,2)
#        right_poly = myCoeffs
#        y = [myCoeffs[2] + myCoeffs[1]*x1 + myCoeffs[0]*(x1**2) for x1 in x]
#        rightCoords = np.int32([np.array(list(zip(x,y)))])
#        cv2.polylines(image,rightCoords, False, 0, thickness=3)
        
    try:
        #print coords
        lane = list(zip(coords[0],coords[1]))
        measure_center(lane)
        print "after measure center try"
    except:
        pass
#    for i in range(0,len(rights)):
#        x,y = filteredRightPolys[i].exterior.coords.xy
#        cv2.fillConvexPoly(image, np.array(zip(x,y), 'int32'),(0,255,0))
#    
#    for i in range(0,len(lefts)):
#        x,y = filteredLeftPolys[i].exterior.coords.xy
#        cv2.fillConvexPoly(image, np.array(zip(x,y), 'int32'),(0,255,255))

def callback(data):
    global cv_image
    global res
    global state
    boxPolyArray = []
    contourArray = []
    state = [0] * (numSectors**2)
    cv_image_orig = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
    cv_image = cv_image_orig[:]
    cv_image=cv2.GaussianBlur(cv_image,(5,5),0)
    
    #try getting topDown image
    cv_image_top, M = unwarp_lane(cv_image)
    hsv=cv2.cvtColor(cv_image_top, cv2.COLOR_BGR2HSV)
    # apply this to the top/down thing
    mask = cv2.inRange(hsv,HSVLOW, HSVHIGH)
    res = cv2.bitwise_and(cv_image_top,cv_image_top, mask = mask)
    # erode and dilate
    kernel = np.ones((6,6),np.uint8)
    res = cv2.erode(res,kernel, iterations = 1)
    res = cv2.dilate(res,kernel, iterations = 1)
    res2 = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    cv2.imshow('res', cv_image_top)
    # find counters
    _, contours, hierarchy = cv2.findContours(res2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print str(contours)
    if contours:
      sigNum = 0
      
        
      # draw contours and create polygons that are >= 500 pixels
      for index,contour in enumerate(contours):
        rect = cv2.minAreaRect(contour)
        (center, (w, h), angle) = rect
        epsilon = 0.1*cv2.arcLength(contour,True)
        polyPoints = np.int0([val for sublist in contour for val in sublist])
        print contour + str(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if(w*h >= 500):
            cv2.drawContours(cv_image_top, contour, -1, (0,255,0), 3)
            cv2.drawContours(res, contour, -1, (0,255,0), 3)
            #boxConvert = map(lambda p: tuple(p), approx)
            boxPoly = Polygon(polyPoints)
            boxPolyArray.append(boxPoly)
            contourArray.append(contour)
            lineDetected = 0
            for i in range (0,numSectors**2):
                if(boxPoly.intersects(polyList[i])):
                    state[i] = 1
                # Do we have a solid white line in front of us - stop?
                if(boxPoly.intersects(polyList[12]) and boxPoly.intersects(polyList[13]) and boxPoly.intersects(polyList[14]) and boxPoly.intersects(polyList[15])):
                    lineDetected = 1
            #rospy.loginfo(lineDetected)
                    
    # Now use our polygons to find lanes
    find_lane(boxPolyArray, contourArray, cv_image_top)
    h1, w1, _ = cv_image_top.shape
    h1 = int(h1)
    w1 = int(w1)
    wP = int(w1/numSectors)
    hP = int(h1/numSectors)
    #for i in range (1,numSectors):
        #cv2.line(cv_image_top,(wP*i,0),(wP*i,h1),(50,50,255),3)
        #cv2.line(cv_image_top,(0,hP*i),(w1,hP*i),(50,50,255),3)

    final_img = bridge.cv2_to_imgmsg(cv_image_top,'bgr8')
    #cv2.imshow('Camera', cv_image_top)
    pub_image_top_down.publish(final_img)
    #cv2.imshow('res', res)
    cv2.waitKey(1)

def measure_center(lane):
    # On undistorted image, 1 ft = 200px - 0.06 in / px
    # Distorted maps 800 px to 764
    # 1ft = 0.3048m
    # it's 0.1524 cm to px
    # car is 55 in across
    # this gives up 41/2 = 20.5 in to be centered
    m_per_pix = 0.001524
    x_distance_centered = 200 * (20.5/12) # centered if 20.5 in away
    right_lane = lane
    right_lane = filter(lambda p: 800-p[1]<10, right_lane)
    right_lane = sorted(right_lane, key = lambda p: p[0])
    
    lane_width_m = 2.4384
    if right_lane != None and len(right_lane) > 0: # we have our lane
        right_x = right_lane[0][0]
        deviation_from_center = -(x_distance_centered - right_x)*m_per_pix
    else: # no lanes, we screwed
        deviation_from_center = -99
    # return lane width and camera's position
    rospy.loginfo(deviation_from_center)
    pub.publish(float(deviation_from_center))
    print deviation_from_center
    return deviation_from_center

def listener():
    global cv_image
    global res
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('right_lane_detection', anonymous=True)
    rate = rospy.Rate(12) # 12hz - camera runs at 12 fps
    topic = "camera_fr/camera_fr/image_raw"#"camera_fm/camera_fm/image_raw"
    rospy.Subscriber(topic, Image, callback)
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        print("Waiting for Image")
        listener()
    except KeyboardInterrupt:
        print("Goodbye")
