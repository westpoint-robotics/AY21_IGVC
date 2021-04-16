#!/usr/bin/env python
"""OpenCV feature detectors with ros CompressedImage Topics in python.

This example subscribes to a ros topic containing sensor_msgs 
CompressedImage. It converts the CompressedImage into a numpy.ndarray, 
then detects and marks features in that image. It finally displays 
and publishes the new image - again as CompressedImage topic.
"""
__author__ =  'Simon Haller <simon.haller at uibk.ac.at>'
__version__=  '0.1'
__license__ = 'BSD'
# Python libs
import sys, time

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy
from cv_bridge import CvBridge

# Ros Messages
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
# We do not use cv_bridge it does not support CompressedImage in python
# from cv_bridge import CvBridge, CvBridgeError

# Dependecies for the keras model
from common.transformations.camera import transform_img, eon_intrinsics
from common.transformations.model import medmodel_intrinsics
from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
from lanes_image_space import transform_points
import os
from tensorflow.keras.models import load_model
from tools.lib.parser import parser

bridge = CvBridge()

supercombo = load_model('supercombo.keras')

VERBOSE=False

class image_feature:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        # topic where we publish
        self.image_pub = rospy.Publisher("/output/compressed", 
            CompressedImage, queue_size=1)
        # self.bridge = CvBridge()

        # subscribed Topic
        self.subscriber = rospy.Subscriber("/camera_fm/camera_fm/image_raw",
            Image, self.callback,  queue_size = 1)
        if VERBOSE :
            print "subscribed to /camera/image"


    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected'''
        if VERBOSE :
            print 'received image of type: "%s"' % ros_data.format
        #### direct conversion to CV2 ####
        cv_image = bridge.imgmsg_to_cv2(ros_data, "bgr8")
        
        ############################################################################################
        #### Feature detectors using CV2 #### 
        # "","Grid","Pyramid" + 
        # "FAST","GFTT","HARRIS","MSER","ORB","SIFT","STAR","SURF"
        feat_det = cv2.GFTTDetector.create()
        time1 = time.time()

        # convert np image to grayscale
        greyIm = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        featPoints = feat_det.detect(greyIm)
        time2 = time.time()
        if VERBOSE :
            print '%s detector found: %s points in: %s sec.'%(method,
                len(featPoints),time2-time1)

        for featpoint in featPoints:
            x,y = featpoint.pt
            cv2.circle(cv_image,(int(x),int(y)), 3, (0,0,255), -1)
        #############################################################################################
        
        cv2.imshow('cv_img', cv_image)
        visualizer(cv_image)
        cv2.waitKey(2)

        #### Create CompressedIamge ####
        msg = CompressedImage()
        msg.header.stamp = rospy.Time.now()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', cv_image)[1]).tostring()
        # Publish new image
        self.image_pub.publish(msg)
        
        #self.subscriber.unregister()

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

def visualizer(cv_image):
    camerafile = "sample.hevc"#sys.argv[1]
    imgs_med_model = np.zeros((2, 384, 512), dtype=np.uint8)
    state = np.zeros((1,512))
    desire = np.zeros((1,8))
    cap = cv_image#cv2.VideoCapture(camerafile)

    if not ret:
        exit()
    else:
        img_yuv = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2YUV_I420)
        imgs_med_model[0] = transform_img(img_yuv, from_intr=eon_intrinsics, to_intr=medmodel_intrinsics, yuv=True,
                                            output_size=(512,256))
    while True:
        plt.clf()
        plt.title("lanes and path")
        plt.xlim(0, 1200)
        plt.ylim(800, 0)
        (ret, current_frame) = cap.read()
        if not ret:
            break
        frame = current_frame.copy()
        img_yuv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2YUV_I420)
        imgs_med_model[1] = transform_img(img_yuv, from_intr=eon_intrinsics, to_intr=medmodel_intrinsics, yuv=True,
                                            output_size=(512,256))
        frame_tensors = frames_to_tensor(np.array(imgs_med_model)).astype(np.float32)/128.0 - 1.0

        inputs = [np.vstack(frame_tensors[0:2])[None], desire, state]
        outs = supercombo.predict(inputs)
        parsed = parser(outs)
        # Important to refeed the state
        state = outs[-1]
        pose = outs[-2]   # For 6 DoF Callibration
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame)
        new_x_left, new_y_left = transform_points(x_left, parsed["lll"][0])
        new_x_right, new_y_right = transform_points(x_left, parsed["rll"][0])
        new_x_path, new_y_path = transform_points(x_left, parsed["path"][0])
        plt.plot(new_x_left, new_y_left, label='transformed', color='w')
        plt.plot(new_x_right, new_y_right, label='transformed', color='w')
        plt.plot(new_x_path, new_y_path, label='transformed', color='green')
        imgs_med_model[0]=imgs_med_model[1]
        plt.pause(0.001)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #         break

        #plt.show()

def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    rospy.init_node('image_feature', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)