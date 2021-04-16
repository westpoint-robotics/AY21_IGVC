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

pltType = "plt"


MAX_DISTANCE = 140.
LANE_OFFSET = 1.8
MAX_REL_V = 10.

LEAD_X_SCALE = 10
LEAD_Y_SCALE = 10
WIDTH = 1920
HEIGHT = 1440

bridge = CvBridge()

# We need a place to keep two separate consecutive image frames
# since that's what SuperCombo uses
previous_frame = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
current_frame = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

fr0 = np.zeros((384, 512), dtype=np.uint8)
fr1 = np.zeros((384, 512), dtype=np.uint8)

crossTrackError = rospy.Publisher('/cross_track_error', Float32, queue_size=1)

if pltType == "plt":
    fig, ax = plt.subplots()
    ax.set_title("lanes and path")
    plt.xlim(0, WIDTH)
    plt.ylim(HEIGHT, 0)
elif pltType == "cv2":
    # OpenCV named windows for visualization (if requested)
    cv2.namedWindow("SuperDrive", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Vision path", cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow("Vision path", 200, 500)

def lane_following(image):
    global supercombo, graph, fr0, fr1, fig, ax
    # print(supercombo.summary())
    imgs_med_model = np.zeros((2, 384, 512), dtype=np.uint8)
    # imgs_med_model = np.zeros((2, HEIGHT, WIDTH), dtype=np.uint8)
    state = np.zeros((1,512)) #################################################
    # state = np.zeros((1,WIDTH))
    desire = np.zeros((1,8))

    x_left = x_right = x_path = np.linspace(0, 192, 192)

    cap = bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
    # print cap.shape # (1440, 1920, 3)

    # filtered = 600
    filtered = WIDTH//2
    alpha = 0.1

    current_frame = cap
    frame = current_frame.copy()

    # print current_frame.shape #(1440,1920)
    current_frame = cv2.resize(current_frame, (512, 384))
    # print current_frame.shape #((384,512))
    current_frame = current_frame[64:320, :]
    # print current_frame.shape #(256, 512)

    img_yuv = cv2.cvtColor(current_frame, cv2.COLOR_BGR2YUV_I420)

    # Use Comma's transformation to get our frame into a format that SuperCombo likes
    frameYUV = transform_img(img_yuv, from_intr=eon_intrinsics,
                             to_intr=medmodel_intrinsics, yuv=True,
                             output_size=(512, 256)).astype(np.float32)/ 128.0 - 1.0

    # We want to push our image in fr1 to fr0, and replace fr1 with
    # the current frame (to feed into the network)
    fr0 = fr1
    fr1 = frameYUV

    # SuperCombo input shape is (12, 128, 256): two consecutive images
    # in YUV space. We concatenate fr0 and fr1 together to get to that
    networkInput = np.concatenate((fr0, fr1))

    # We then want to reshape this into the shape the network requires
    networkInput = networkInput.reshape((1, 12, 128, 256))

    # Build actual input combination
    inputs = [networkInput, desire, state]

    with graph.as_default():
        set_session(sess)
        outs = supercombo.predict(inputs)

    previous_frame = current_frame
    
    #K.clear_session()
    parsed = parser(outs)
    # Important to refeed the state
    state = outs[-1]
    pose = outs[-2]   # For 6 DoF Callibration
    
    leftLanePoints = parsed["lll"][0]
    rightLanePoints = parsed["rll"][0]
    pathPoints = parsed["path"][0]

    new_x_left, new_y_left = transform_points(x_left,leftLanePoints)
    new_x_right, new_y_right = transform_points(x_right, rightLanePoints)
    new_x_path, new_y_path = transform_points(x_path, pathPoints)

    # Compute position on current lane
    currentPredictedPos = (-1) * pathPoints[0]
    print currentPredictedPos #in meters

    error = WIDTH//2 - new_x_path[0]
    #print 'new_x_path[0]: ', new_x_path[0]
    #print 'error [pixels]: ', error
    # deg = (new_x_path[-1] - new_x_path[0])
    filtered = alpha*error + (1-alpha)*filtered #Low Pass Filter
    crossTrackError.publish(filtered)

    #  --------------------------plotting--------------------
    if pltType == "plt":
        ax.cla()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ax.imshow(frame)

        new_x_left = [x*2 for x in new_x_left] #For display only
        new_y_left = [x*2 for x in new_y_left]
        new_x_right = [x*2 for x in new_x_right]
        new_y_right = [x*2 for x in new_y_right]
        new_x_path = [x*2 for x in new_x_path]
        new_y_path = [x*2 for x in new_y_path]
        # print max(new_x_right)
        ax.plot(new_x_left, new_y_left, label='transformed', color='w', linewidth=4)
        ax.plot(new_x_right, new_y_right, label='transformed', color='w', linewidth=4)
        ax.plot(new_x_path, new_y_path, label='transformed', color='green', linewidth=4)
        
        #fig.show()
        # plt.pause(0.001)

    elif pltType == "cv2":
        canvas = frame.copy()
        canvas = cv2.resize(canvas, ((700, 350)))
        cv2.putText(canvas, "Vision processing time: " + str(p_totalFrameTime) + " ms (" + str(fpsActual) + " fps)", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(canvas, "Device: " + tfDevice, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.putText(canvas, "Position: " + str(round(currentPredictedPos, 3)) + " m off centerline", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

        # Create canvas for graph plotting
        plotCanvas = np.zeros((500, 200, 3), dtype=np.uint8)

        # Plot points!
        ppmY = 10
        ppmX = 20

        # We know we can only display 500 / ppmY = 50 meters ahead
        # so limiting our loop will allow for a faster processing time
        for i in range(51):
            cv2.circle(plotCanvas, (int(100 - abs(leftLanePoints[i] * ppmX)), int(i * ppmY)), 2, (160, 160, 160), -1)
            cv2.circle(plotCanvas, (int(100 + abs(rightLanePoints[i] * ppmX)), int(i * ppmY)), 2, (160, 160, 160), -1)
            cv2.circle(plotCanvas, (int(100 - (pathPoints[i] * ppmX)), int(i * ppmY)), 4, (10, 255, 10), -1)

        # Flip plot path for display
        plotCanvas = cv2.flip(plotCanvas, 0)

        # Add some texts for distance
        cv2.putText(plotCanvas, "0 m", (10, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
        cv2.putText(plotCanvas, "10 m", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
        cv2.putText(plotCanvas, "20 m", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
        cv2.putText(plotCanvas, "30 m", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
        cv2.putText(plotCanvas, "40 m", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
        cv2.putText(plotCanvas, "50 m", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200,200,200), 1)
        # print "ayy"
        cv2.imshow("SuperDrive", canvas)
        cv2.waitKey(0)
        cv2.imshow("Vision path", plotCanvas)
        cv2.waitKey(0)
        # print "lmao"


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
