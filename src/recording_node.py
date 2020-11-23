#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os, sys

bridge = CvBridge()

class ImageSaver(object):

    def __init__(self, path, rgb):
        self.path = path
        self.rgb = rgb
        
        if not os.path.exists(path):
            os.makedirs(path)

    def save_img(self, msg):
        print("Received an image!")    
        try:
            # Convert your ROS Image message to OpenCV2
            if(self.rgb):
                cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
            else:
                cv2_img = bridge.imgmsg_to_cv2(msg)
        except CvBridgeError, e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            time = msg.header.stamp
            cv2.imwrite(self.path+str(time)+'.png', cv2_img)
            rospy.sleep(1)

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
