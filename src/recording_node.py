#!/usr/bin/env python2

import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os, sys

bridge = CvBridge()

class ImageSaver(object):

    def __init__(self, path, rgb):
        self.path = path
        self.rgb = rgb
	self.max_distance = rospy.get_param('/zedA/zed_node_A/depth/max_depth')
        self.min_distance = rospy.get_param('/zedA/zed_node_A/depth/min_depth')
	self.scaling = 65535/(self.max_distance-self.min_distance)
        
        if not os.path.exists(path):
            os.makedirs(path)

    def save_img(self, msg):
        print("Received an image!")    	
        try:
            # Convert your ROS Image message to OpenCV2
            if(self.rgb):
		cv2_img = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough') 
		time = msg.header.stamp
            	cv2.imwrite(self.path+str(time)+'.png', cv2_img)
            else:
		cv2_img = bridge.imgmsg_to_cv2(msg)
		cv2_img = np.clip(cv2_img,self.min_distance,self.max_distance)	
		cv2_img = (cv2_img-self.min_distance)*self.scaling
		time = msg.header.stamp
            	cv2.imwrite(self.path+str(time)+'.png', cv2_img.astype(np.uint16))
        except CvBridgeError, e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            rospy.sleep(0.01)

    def callback(self, msg):
        self.save_img(msg)


def main():
    rospy.init_node('recording_node')   
    path = rospy.get_param('~recording_path')

    if(os.path.exists(path)):
        print("ERROR this experiment has bee already recorded")
        return
    leftRGBsaver = ImageSaver(path + '/left_RGB/',True)
    rightRGBsaver = ImageSaver(path + '/right_RGB/',True)
    depthsaver = ImageSaver(path + '/depth/',False)

    rospy.Subscriber('/left_rgb_camera', Image, leftRGBsaver.callback, queue_size = 100)
    rospy.Subscriber('/right_rgb_camera', Image, rightRGBsaver.callback, queue_size = 100)
    rospy.Subscriber('/depth_camera', Image, depthsaver.callback, queue_size = 100)    

    rospy.spin()


if __name__ == '__main__':
    main()
