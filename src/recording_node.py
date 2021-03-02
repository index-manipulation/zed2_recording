#!/usr/bin/env python2

import rospy
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os, sys

bridge = CvBridge()

class ImageSaver(object):

    def __init__(self, path):
        self.path = path
	self.rescaling = ''
	self.min_distance_name = ''
        self.max_distance_name = ''
        self.max_distance = 0
        self.min_distance = 0
        self.scaling = 0
	self.get_params()
        
        if not os.path.exists(path):
            os.makedirs(path)

    def get_params(self):
	self.rescaling = rospy.get_param('~rescaling')	
        if(self.rescaling):
		self.rescaling = True
		self.max_distance_name = rospy.get_param('~rescaling_param_max')
       		self.min_distance_name = rospy.get_param('~rescaling_param_min')
        	self.max_distance = rospy.get_param(self.max_distance_name)
        	self.min_distance = rospy.get_param(self.min_distance_name)
		self.scaling = 65535/(self.max_distance-self.min_distance)
		


    def save_img(self, msg):
        print("Received an image!")    	
        try:
            # Convert your ROS Image message to OpenCV2
            if(not(self.rescaling)	):
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
            rospy.sleep(0.01)
	
    def callback(self, msg):
        self.save_img(msg)


def main():
    rospy.init_node('recording_node')   
    path = rospy.get_param('~recording_path')

    if(os.path.exists(path)):
        print("ERROR this experiment has bee already recorded")
        return

    cameraSaver = ImageSaver(path)
    rospy.Subscriber('/camera_topic', Image, cameraSaver.callback)


#    leftRGBsaver = ImageSaver(path + '/left_RGB/',True)
#    rightRGBsaver = ImageSaver(path + '/right_RGB/',True)
#    depthsaver = ImageSaver(path + '/depth/',False)

    #rospy.Subscriber('/left_rgb_camera', Image, leftRGBsaver.callback, queue_size = 100)
    #rospy.Subscriber('/right_rgb_camera', Image, rightRGBsaver.callback, queue_size = 100)
    #rospy.Subscriber('/depth_camera', Image, depthsaver.callback, queue_size = 100)    

    rospy.spin()


if __name__ == '__main__':
    main()
