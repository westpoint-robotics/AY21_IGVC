#!/usr/bin/env python
from ctypes import *
import math
import random
import numpy as np

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Int8, Float32
from cv_bridge import CvBridge
bridge = CvBridge()

import cv2

## publishers
stopsign_pub = rospy.Publisher('/stop_sign/number', Int8, queue_size=1)
person_num_pub = rospy.Publisher('/person/number', Int8, queue_size=1)
person_xcor_pub = rospy.Publisher('/person/xcor', Float32, queue_size=1)
person_ycor_pub = rospy.Publisher('/person/ycor', Float32, queue_size=1)
#added below
barrel_pub = rospy.Publisher('/barrel/number', Int8, queue_size=1)
barrel_xcor_pub = rospy.Publisher('/barrel/xcor', Float32, queue_size=1)
barrel_ycor_pub = rospy.Publisher('/barrel/ycor', Float32, queue_size=1)
pothole_pub = rospy.Publisher('/pothole/number', Int8, queue_size=1)
pothole_xcor_pub = rospy.Publisher('/pothole/xcor', Float32, queue_size=1)
pothole_ycor_pub = rospy.Publisher('/pothole/ycor', Float32, queue_size=1)
right_pub = rospy.Publisher('/right/number', Int8, queue_size=1)
left_pub = rospy.Publisher('/left/number', Int8, queue_size=1)
car_pub = rospy.Publisher('/car/number', Int8, queue_size=1)

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]
"""
class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]
  """              
class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int),
                ("uc", POINTER(c_float)),
                ("points", c_int),
                ("embeddings", POINTER(c_float)),
                ("embedding_size", c_int),
                ("sim", c_float),
                ("track_id", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

    

#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL("/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

ndarray_image = lib.ndarray_to_image
ndarray_image.argtypes = [POINTER(c_ubyte), POINTER(c_long), POINTER(c_long)]
ndarray_image.restype = IMAGE

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

def classify(net, meta, im):
    im = nparray_to_image(im)
    #im = array_to_image(im)
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res
    
    """
class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]
"""
def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    #im = load_image(image, 0, 0)
    im = nparray_to_image(image)
    num = c_int(0)
    pnum = pointer(num)
    out = predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms):
        do_nms_obj(dets, num, meta.classes, nms)
    res = []
    for j in range(num):
        for i in range(meta.classes):          
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
                #if meta.names[i] == "stop sign":
                    #print(b.w*b.h)
                #    pub_state.data = [b.w * b.h]
                    #print (pub_state.data)
    #res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res

    
def arr_to_img(arr):
    c, h, w= arr.shape
    step_h, step_w, step_c = arr.strides
    im = make_image(w, h, c)
    #print(type(im))
    for i in range(h):
        for k in range(c):
            for j in range(w):
                index1 = k*w*h + i*w + j
                index2 = step_h*i + step_w*j + step_c*k
                im.data[index1] = arr[index2]/255.
    return im
    
def nparray_to_image(img):
    data = img.ctypes.data_as(POINTER(c_ubyte))
    image = ndarray_image(data, img.ctypes.shape, img.ctypes.strides)

    return image

def draw(img, boxes):
    global stopsign_pub, person_num_pub, person_xcor_pub, person_ycor_pub, barrel_xcor_pub, barrel_ycor_pub, pothole_xcor_pub, pothole_ycor_pub, num_car, num_barrel, num_pothole, num_left, num_right, num_person, xcor_person, ycor_person, xcor_barrel, ycor_barrel, xcor_pothole, ycor_pothole, barrel_xcor_pub
    colors = [(255,0,0), (0,255,0), (0,0,255)]
    num_stopsign = 0
    num_person = 0
    num_car = 0
    num_barrel = 0
    num_pothole = 0
    num_left = 0
    num_right = 0
    xcor_person = 0.0
    ycor_person = 0.0
    #added
    xcor_barrel = 0.0
    ycor_barrel = 0.0
    xcor_pothole = 0.0
    ycor_pothole = 0.0
    #added end
    for i, box in enumerate(boxes):
        item, confidence, (x, y, w, h) = box
        color = colors[i%len(colors)]
        if confidence > .7:
            #changed / added below 
            if item == 'stopsign': #and x > img.shape[1]:
                num_stopsign += 1
            if item == 'pedestrian':
                num_person += 1
                if max(ycor_person, y) == y:
                    xcor_person = x
                    ycor_person = y
            if item == 'trafficbarrel':
                num_barrel += 1
                xcor_barrel = x
                ycor_barrel = y
            if item == 'pothole':
                num_pothole += 1
                if max(ycor_pothole, y) == y:
                    xcor_pothole = x
                    ycor_pothole = y
            if item == 'onewayright':
                num_right += 1
            if item == 'onewayleft':
                num_left += 1
            if item == 'car' or item == 'truck':
                num_car += 1
            #end added above
            cv2.rectangle(img, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), color, 4)
            cv2.putText(img, "{}:{:.1f}%".format(item, confidence*100), (int(x)-int(w/3), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
            #print("{}:{:.1f}%".format(item, confidence*100))
    stopsign_pub.publish(num_stopsign)
    person_num_pub.publish(num_person)
    person_xcor_pub.publish(xcor_person)
    person_ycor_pub.publish(ycor_person)
    #added below 
    barrel_pub.publish(num_barrel)
    barrel_xcor_pub.publish(xcor_barrel)
    barrel_ycor_pub.publish(ycor_barrel)
    pothole_pub.publish(num_pothole)
    pothole_xcor_pub.publish(xcor_pothole)
    pothole_ycor_pub.publish(ycor_pothole)
    right_pub.publish(num_right)
    left_pub.publish(num_left)
    car_pub.publish(num_car)
    #end added 
    #if num_person:
    #    person_xcor_pub.publish(xcor_person)
    #    person_ycor_pub.publish(ycor_person)
   
    

def callback(img):
    img = bridge.imgmsg_to_cv2(img, desired_encoding="bgr8")
    img = cv2.resize(img,(1200, 800), interpolation = cv2.INTER_CUBIC)
    boxes = detect(net, meta, img)
    draw(img, boxes)
    """
    try:
        boxes = detect(net, meta, img)
        draw(img, boxes)
    except ValueError, e:
        print(e)
        """
    #cv2.imshow("TEST", img)
    #cv2.waitKey(30) # delay to prevent darknet from depleting resources

def listener():
    global stopsign_pub, person_num_pub, person_xcor_pub, person_ycor_pub, barrel_pub, pothole_pub, left_pub, right_pub, car_pub
    #changed above
    rospy.init_node("object_detection", anonymous=True)
    rate = rospy.Rate(3)
    # topic = "/camera_fm/camera_fm/image_raw"
    topic = "/camera_fm/camera_fm/image_raw"
    
    #added above
    #topic = "/camera/rgb/image"
    rospy.Subscriber(topic, Image, callback)
    
    while not rospy.is_shutdown():
        rate.sleep()
    
if __name__ == "__main__":
    #net = load_net("/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/cfg/yolov3-416/yolov3.cfg", "/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/cfg/yolov3-416/yolov3.weights", 0)
    #meta = load_meta("/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/cfg/coco.data")
    net = load_net("/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/custom_weights/multigpu.cfg", "/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/custom_weights/multigpu_16000.weights", 0)
    meta = load_meta("/home/user1/Desktop/igvc/catkin_ws/src/ay21_igvc_catkin/src/igvc_sw/stop_sign/custom_weights/ultimate.data")
    set_gpu(0)
    try:
        listener()
    except KeyboardInterrupt:
        print "-----BYE-----"
    #r = detect(net, meta, "dog.jpg")
    #print r
    

