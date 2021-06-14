#!/usr/bin/env python
import cv2
import sys, time, os
from common.transformations.camera import transform_img, eon_intrinsics
from common.transformations.model import medmodel_intrinsics
import numpy as np
# from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from lanes_image_space import transform_points
from tensorflow.keras.models import load_model
from parser import parser


# numpy and scipy
from scipy.ndimage import filters

# Ros libraries
import roslib
import rospy
from cv_bridge import CvBridge

# Ros Messages
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import Float32, Int8
from pacmod_msgs.msg import PacmodCmd

# Tensorflow
from tensorflow.keras import backend as K
from tensorflow.python.keras.backend import set_session


MAX_DISTANCE = 140.
LANE_OFFSET = 1.8
MAX_REL_V = 10.

LEAD_X_SCALE = 10
LEAD_Y_SCALE = 10
WIDTH = 1920
HEIGHT = 1440
CENTER_PIXEL = 573#570#540#525#510
SCALING_FACTOR = -120
DISCOUNT_RATE = .7

CENTER_PIXEL = 510
SCALING_FACTOR = 115

bridge = CvBridge()

PARKING_FLAG = 0
PARALLEL_FLAG = 0
MERGE_LEFT_FLAG = False
MERGE_RIGHT_FLAG = True


crossTrackError = rospy.Publisher('/cross_track_error', Float32, queue_size=1)
stopline_pub = rospy.Publisher('/stop_sign/potential_stop_line', Int8, queue_size=1)
shift_cmd = rospy.Publisher('/pacmod/as_rx/shift_cmd', PacmodCmd, queue_size = 10)
pac_dict = {'drive':3, 'neutral':2, 'reverse':1, 'park':0}
shift_to_PACMOD = PacmodCmd()
shift_to_PACMOD.ui16_cmd = pac_dict['reverse']

"""
matplotlib plt setup IOT speed up the plotting
"""

def discount(arr):
    res = 0
    temp = arr[:len(arr)//2]
    for i in temp[::-1]:
        res = DISCOUNT_RATE*i + (1-DISCOUNT_RATE)*res
    return res

def change_brightness(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    brightness = np.average(v)
    value = int(brightness)
    if brightness >= 50:
        v[v < value] = value//2
        v[v >= value] -= value
    else:
        limit = 255 - value
        v[v > limit] = limit
        v[v <= limit] += (50 - value)
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

    
def detect_lines(frame):
    global potential_stopline
    frame = np.copy(frame[frame.shape[0]//3:frame.shape[0], :])
    edges = cv2.Canny(frame, 150, 240)
    minLineLength = 150
    maxLineGap = 20
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
    curr = frame.copy()
    potential_stopline = 0
    try:
        for [[x1, y1, x2, y2]] in lines:
            if abs(x2-x1) > abs(y2-y1)*4: #  horizontal lines
                cv2.line(frame, (x1,y1), (x2,y2), (0,0,255), 3)
                if y2 >= frame.shape[0]//3+30:
                    potential_stopline += 1
            elif abs(x2-x1)*4 > abs(y2-y1): #  vertical lines
                cv2.line(curr, (x1,y1), (x2,y2), (255,0,0), 3)
                cv2.line(frame, (x1,y1), (x2,y2), (255,0,0), 3)
            
    except TypeError:
        pass
    finally:
        #cv2.line(frame, (frame.shape[1]//3, frame.shape[0]//3), (frame.shape[1]*2//3, frame.shape[0]//3), (255,0,0),2)
        cv2.line(frame, (frame.shape[1]//4, frame.shape[0]//2+100), (frame.shape[1]*3//4, frame.shape[0]//2+100), (255,0,0),2)
        cv2.line(frame, (frame.shape[1]//4, frame.shape[0]//2-50), (frame.shape[1]*3//4, frame.shape[0]//2-50), (255,0,0),2)
        cv2.line(frame, (frame.shape[1]//2, 0), (frame.shape[1]//2, frame.shape[0]), (255,0,0),2)
        
        mask1 = cv2.inRange(frame, (0,0,255), (0,0,255))
        mask2 = cv2.inRange(frame, (255,0,0), (255,0,0))
        intersections = np.bitwise_and(mask1,mask2)
        #cv2.imshow("Intersections", intersections)
        stopline_pub.publish(potential_stopline)
        #cv2.imshow("Hough lines", frame)
        cv2.waitKey(1)
 
    
def frames_to_tensor(frames):                                                                                               
  H = (frames.shape[1]*2)//3                                                                                                
  W = frames.shape[2]                                                                                                       
  in_img1 = np.zeros((frames.shape[0], 6, H//2, W//2), dtype=np.uint8)                                                      
                                                                                                                            
  in_img1[:, 0] = frames[:, 0:H:2, 0::2]                                                                                    
  in_img1[:, 1] = frames[:, 1:H:2, 0::2]                                                                                    
  in_img1[:, 2] = frames[:, 0:H:2, 1::2]                                                                                    
  in_img1[:, 3] = frames[:, 1:H:2, 1::2]                                                                                    
  in_img1[:, 4] = frames[:, H:H+H//4].reshape((-1, H//2,W//2))                                                              
  in_img1[:, 5] = frames[:, H+H//4:H+H//2].reshape((-1, H//2,W//2))
  return in_img1

def lane_following(image):
    global supercombo, graph
    # print(supercombo.summary())
    #initial = time.time()
    imgs_med_model = np.zeros((2, 384, 512), dtype=np.uint8)
    # imgs_med_model = np.zeros((2, HEIGHT, WIDTH), dtype=np.uint8)
    state = np.zeros((1,512)) #################################################
    # state = np.zeros((1,WIDTH))
    desire = np.zeros((1,8))

    x_left = x_right = x_path = np.linspace(0, 192, 192)

    cap = bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
    height, width = cap.shape[:2]
    cap = cv2.resize(cap,(1200, 800), interpolation = cv2.INTER_CUBIC)   
    
    filtered = 0
    #filtered = WIDTH//2
    alpha = 0.8
    plt.clf()
    plt.title("lanes and path")
    plt.xlim(0, 1200)
    # plt.xlim(0, WIDTH)
    plt.ylim(800, 0)
    # plt.ylim(HEIGHT, 0)
    
    # applies brightness filter using HSV in CV2
    #cap = change_brightness(cap)

    frame = cap.copy()
    
    detect_lines(frame)
    
    img_yuv = cv2.cvtColor(cap, cv2.COLOR_BGR2YUV_I420)
    # frame is a list of 1440 x 1920
    imgs_med_model[1] = transform_img(img_yuv, from_intr=eon_intrinsics, to_intr=medmodel_intrinsics, yuv=True, output_size=(512,256)) #This order is correct, outputsize = (maxWidth, maxHeight)
    # imgs_med_model[1] = transform_img(img_yuv, from_intr=eon_intrinsics, to_intr=medmodel_intrinsics, yuv=True, output_size=(WIDTH,HEIGHT*2/3)) ##########################################
    
    frame_tensors = frames_to_tensor(np.array(imgs_med_model)).astype(np.float32)/128.0 - 1.0 
    # print frame_tensors.shape # (2, 6, 128, 960)
    
    inputs = [np.vstack(frame_tensors[0:2])[None], desire, state] 
    # inputs = [np.vstack(frame_tensors[0:2])[None], np.zeros((1,8)), state]
    # print len(frame_tensors[0][0])

    with graph.as_default():
        set_session(sess)
        outs = supercombo.predict(inputs)

    #K.clear_session()
    parsed = parser(outs)
    # Important to refeed the state
    state = outs[-1]
    pose = outs[-2]   # For 6 DoF Callibration
    #prev = time.time()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #print "DELAY: {:.2}".format((time.time()-prev)*1000)
    
    new_x_left, new_y_left = transform_points(x_left, parsed["lll"][0])
    new_x_right, new_y_right = transform_points(x_right, parsed["rll"][0])
    new_x_path, new_y_path = transform_points(x_path, parsed["path"][0])
    #error = (discount(new_x_path)-CENTER_PIXEL)/SCALING_FACTOR
    #filtered = alpha*error + (1-alpha)*filtered
    #crossTrackError.publish(filtered)
    
    plt.imshow(frame, interpolation=None)###################################

   # new_x_left, new_y_left = transform_points(x_left, parsed["lll"][0])
   # new_x_right, new_y_right = transform_points(x_right, parsed["rll"][0])
 #   new_x_path, new_y_path = transform_points(x_path, parsed["path"][0])
    potential_middle = average_blue(parsed["lll"][0], parsed["rll"][0])
    #error = (new_x_path[0]-CENTER_PIXEL)/SCALING_FACTOR
    #error = discount(parsed["path"][0])*3
    error = discount(potential_middle[:40])# - discount(parsed["path"][0][:40])
    #error = discount(potential_middle)#+ 0.07 # DML add 0.7
    
    #error = 0 if abs(error) < 0.05 else error
    filtered = error#filtered = alpha*error + (1-alpha)*filtered
    crossTrackError.publish(filtered)
    #mergeLeft(rospy.get_time())
    #mergeRight(rospy.get_time())
#    plt.plot(new_x_left, new_y_left, label='transformed', color='w', linewidth=4)
#    plt.plot(new_x_right, new_y_right, label='transformed', color='w', linewidth=4)
#    plt.plot(new_x_path, new_y_path, label='transformed', color='green', linewidth=4)
    plt.clf()
    plt.title("lanes and path")
    plt.xticks([-3,-2,-1,0,1,2,3])
    plt.xlim(-3, 3)
    # lll = left lane line
    plt.text(-1,10, str(error)[:6]) # DML added this line
    distance = 100
    plt.plot(parsed["lll"][0][:distance], range(0,distance), "b-", linewidth=1)
    # rll = right lane line
    plt.plot(parsed["rll"][0][:distance], range(0, distance), "b-", linewidth=1)
    # path = path cool isn't it ?
    #plt.plot(parsed["path"][0][:distance]*(-1), range(0, distance), "r-", linewidth=1)
    plt.plot(parsed["path"][0][:distance], range(0, distance), "g-", linewidth=1) # potential_middle[:50]
    plt.plot(np.subtract(potential_middle[:distance], parsed["path"][0][:distance]), range(0, distance), "r-", linewidth=1)
    imgs_med_model[0]=imgs_med_model[1]
    #print time.time() - initial
    plt.gca().invert_xaxis()
    plt.pause(0.001)
    #plt.show()

def load_models():
    global sess
    initial = time.time()
    # tf_config = some_custom_config
    sess = tf.compat.v1.Session()#config=tf_config
    set_session(sess)
    os.chdir('/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/lane_following')
    global supercombo
    supercombo = tf.keras.models.load_model("supercombo.keras")
    # this is the key : save the graph after loading the model
    global graph
    graph = tf.compat.v1.get_default_graph()

def parking():
    global PARKING_FLAG, PARALLEL_FLAG
    """
    0: idle
    1: parallel
    2: pull in
    3: pull out
    """
    """
    https://github.com/Rohith-K/Autonomous-Parallel-Parking-Car-like-Robot-Gazebo-ROS/blob/master/parkingdemo_gazebo/scripts/parallel_parking.py
    locate parking spot
    0.position itself
    1.pull in- 0deg until the back of the vehicle passes the cone
    2.pull in- -45deg until the back of the vehicle is one feet away from the edge
    3.pull in- 45deg until the back of the vehicle is centered with the cone in the rear 
    4.pull in- 0deg until the vehicle is fully in spot
    5.stop (done)
    """
    steer = 0.0 #Float32
    if PARKING_FLAG == 0: # IDLE
        pass
    elif PARKING_FLAG == 1: # PARALLEL
        if PARALLEL_FLAG == 1:
            steer = 0.0
        elif PARALLEL_FLAG == 2:
            steer = 1.0
        elif PARALLEL_FLAG == 3:
            steer = -1.0
        elif PARALLEL_FLAG == 4:
            steer = 0.0
        else:
            steer = 0.0
        crossTrackError.publish(steer)
    elif PARKING_FLAG == 2: # PULL IN
        pass
    elif PARKING_FLAG == 3: # PULL OUT
        pass
    else:
        pass

def mergeLeft(startTime):
    global crossTrackError, MERGE_LEFT_FLAG
    while MERGE_LEFT_FLAG and (rospy.get_time() - startTime) < 100:
        crossTrackError.publish(-0.7)
        
def mergeRight(startTime):
    global crossTrackError, MERGE_RIGHT_FLAG
    while MERGE_RIGHT_FLAG and (rospy.get_time() - startTime) < 100:
        crossTrackError.publish(0.7)

def average_blue(arr1, arr2):
    res = []
    for i in range(0, len(arr1)):
        res.append((arr1[i] + arr2[i])/2)
    return res

def listener():
    global cv_image, res, ourGuy
    initial = time.time()
    rospy.init_node('linedetection',anonymous=True)
    #rate = rospy.Rate(12) # 12hz
    topic = "/camera_fm/camera_fm/image_raw"
    load_models()
    #print time.time() - initial
    rospy.Subscriber(topic, Image, lane_following)
    print time.time() - initial
    #while not rospy.is_shutdown():
    # publish pixel distance from car to line; -1 if not found
    #    rate.sleep()   
    rospy.spin()     
        
if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Goodbye")
