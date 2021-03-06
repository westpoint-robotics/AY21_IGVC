
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
#https://www.pyimagesearch.com/2018/12/17/image-stitching-with-opencv-and-python/

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True, help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True, help="path to the output image")
ap.add_argument("-c", "--crop", type=int, default=0, help="whether to crop out largest rectangular region")
args = vars(ap.parse_args())
print("Ask HyunJin for questions :).")
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"])))
images = []
if not imagePaths: print("image paths is empty")
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)
#print(images)
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)





if status == 0:
    #cv2.imshow("stitched", stitched)
    #cv2.waitKey(0)
    if args["crop"] > 0:
        #creates 10 pixel border around the stitched image
        print("[INFO] cropping...")
        stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
        #cpnvert the stitched image to grayscale and threshold it
        #such that all pixels greater than zero are set to 255
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
        #gray scale^
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
        #gray contours
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        minRect = mask.copy()
        sub = mask.copy()
        print("while function reached")
        while cv2.countNonZero(sub) > 0:
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, thresh)
            print(cv2.countNonZero(sub))
            cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)
            stitched = stitched[y:y + h, x:x + w]
            #cv2.imshow("stitched", stitched)
            #cv2.waitKey(0)

    #END of Crop
    cv2.imwrite(args["output"], stitched)
    cv2.imshow("stitched", stitched)
    cv2.waitKey(0)

else:
    print("[INFO] image stitching failed ({})".format(status))
    if(status == 1): print("needs more input images to construct")
    if(status == 2): print("algorithm failed")
    if(status == 3): print("I don't know man")
# 1 means need more input images to construct
# 2 means RANSAC homography estimation fails
# 3 failing to properly estimate camera intrinsics/extrinsics