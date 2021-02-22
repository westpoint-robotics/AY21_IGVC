from common.transformations.camera import transform_img, eon_intrinsics
from common.transformations.model import medmodel_intrinsics
import numpy as np
# from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
from lanes_image_space import transform_points
from tensorflow.keras.models import load_model
import tensorflow as tf
from parser import parser
import cv2
import sys, time, os

# numpy and scipy
from scipy.ndimage import filters

# Ros libraries
import roslib
import rospy
from cv_bridge import CvBridge

# Ros Messages
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from std_msgs.msg import Float32

from tensorflow.keras import backend as K
from tensorflow.python.keras.backend import set_session


MAX_DISTANCE = 140.
LANE_OFFSET = 1.8
MAX_REL_V = 10.

LEAD_X_SCALE = 10
LEAD_Y_SCALE = 10
WIDTH = 1920
HEIGHT = 1440
mm = 0

bridge = CvBridge()

# We need a place to keep two separate consecutive image frames
# since that's what SuperCombo uses
previous_frame = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
current_frame = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
# previous_frame = np.zeros((256, 512), dtype=np.uint8)
# current_frame = np.zeros((256, 512), dtype=np.uint8)

crossTrackError = rospy.Publisher('/cross_track_error', Float32, queue_size=1)

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
    global supercombo, graph, mm
    # print(supercombo.summary())
    imgs_med_model = np.zeros((2, 384, 512), dtype=np.uint8)
    # imgs_med_model = np.zeros((2, HEIGHT, WIDTH), dtype=np.uint8)
    state = np.zeros((1,512)) #################################################
    # state = np.zeros((1,WIDTH))
    desire = np.zeros((1,8))

    x_left = x_right = x_path = np.linspace(0, 192, 192)

    cap = bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
    #cap.resize((256, 512, 3))
    #print "BEFORE: " + str(cap.shape)
    #np.reshape(cap, (874, 1164, 3)) 
    height, width = cap.shape[:2]
    #cap = cv2.resize(cap,(width/2, height/2), interpolation = cv2.INTER_CUBIC) 
    cap = cv2.resize(cap,(1200, 800), interpolation = cv2.INTER_CUBIC)   
    #print "AFTER: " + str(cap.shape)
    # print cap.shape # (1440, 1920, 3)

    # filtered = 600
    filtered = WIDTH//2
    alpha = 0.1
    plt.clf()
    plt.title("lanes and path")
    plt.xlim(0, 1200)
    # plt.xlim(0, WIDTH)
    plt.ylim(800, 0)
    # plt.ylim(HEIGHT, 0)

    current_frame = cap
    frame = current_frame.copy()
    img_yuv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2YUV_I420)
    # frame is a list of 1440 x 1920
    imgs_med_model[1] = transform_img(img_yuv, from_intr=eon_intrinsics, to_intr=medmodel_intrinsics, yuv=True, output_size=(512,256)) #This order is correct, outputsize = (maxWidth, maxHeight)
    # imgs_med_model[1] = transform_img(img_yuv, from_intr=eon_intrinsics, to_intr=medmodel_intrinsics, yuv=True, output_size=(WIDTH,HEIGHT*2/3)) ##########################################
    
    frame_tensors = frames_to_tensor(np.array(imgs_med_model)).astype(np.float32)/128.0 - 1.0 
    # print frame_tensors.shape # (2, 6, 128, 960)
    
    inputs = [np.vstack(frame_tensors[0:2])[None], desire, state] #########################################################
    # inputs = [np.vstack(frame_tensors[0:2])[None], np.zeros((1,8)), state]
    # print len(frame_tensors[0][0])

    with graph.as_default():
        set_session(sess)
        outs = supercombo.predict(inputs)

    previous_frame = current_frame
    
    #K.clear_session()
    parsed = parser(outs)
    # Important to refeed the state
    state = outs[-1]
    pose = outs[-2]   # For 6 DoF Callibration
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    plt.imshow(frame)

    new_x_left, new_y_left = transform_points(x_left, parsed["lll"][0])
    new_x_right, new_y_right = transform_points(x_right, parsed["rll"][0])
    new_x_path, new_y_path = transform_points(x_path, parsed["path"][0])
    # new_x_left = [x*2 for x in new_x_left]
    # new_y_left = [x*2 for x in new_y_left]
    # new_x_right = [x*2 for x in new_x_right]
    # new_y_right = [x*2 for x in new_y_right]
    # new_x_path = [x*2 for x in new_x_path]
    # new_y_path = [x*2 for x in new_y_path]

    error = WIDTH//2 - new_x_path[0]
    #print 'new_x_path[0]: ', new_x_path[0]
    #print 'error [pixels]: ', error
    # deg = (new_x_path[-1] - new_x_path[0])
    filtered = alpha*error + (1-alpha)*filtered
    crossTrackError.publish(filtered)
    mm = max(max(new_y_right), mm)
    #print mm
    plt.plot(new_x_left, new_y_left, label='transformed', color='w', linewidth=4)
    plt.plot(new_x_right, new_y_right, label='transformed', color='w', linewidth=4)
    plt.plot(new_x_path, new_y_path, label='transformed', color='green', linewidth=4)
    imgs_med_model[0]=imgs_med_model[1]
    plt.pause(0.001)
#    plt.show()

def load_models():
    global sess
    # tf_config = some_custom_config
    sess = tf.Session()#config=tf_config
    set_session(sess)
    global supercombo
    supercombo = load_model('supercombo.keras')
            # this is key : save the graph after loading the model
    global graph
    graph = tf.get_default_graph()


def listener():
    global cv_image, res, ourGuy
    
    rospy.init_node('linedetection',anonymous=True)
    rate = rospy.Rate(12) # 12hz
    topic = "/camera_fm/camera_fm/image_raw"
    load_models()
    rospy.Subscriber(topic, Image, lane_following)
    
    while not rospy.is_shutdown():
    # publish pixel distance from car to line; -1 if not found
        rate.sleep()        
        
if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print("Goodbye")
