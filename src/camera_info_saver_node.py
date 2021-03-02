#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import CameraInfo
import os, sys

    
def cameraInfoCallback(msg):
    path = rospy.get_param('~save_path')
    f = open(path+"info.txt", "a")
    f.write("height: " + str(msg.height)+"\n")
    f.write("width: " + str(msg.width)+"\n")
    f.write("distortion_model: " + str(msg.distortion_model)+"\n")
    f.write("D: " + str(msg.D)+"\n")
    f.write("K: " + str(msg.K)+"\n")
    f.write("R: " + str(msg.R)+"\n")
    f.write("P: " + str(msg.P)+"\n")
    f.write("binning_x: " + str(msg.binning_x)+"\n")
    f.write("binning_y: " + str(msg.binning_y)+"\n")
    f.write("roi.x_offset: " + str(msg.roi.x_offset)+"\n")
    f.write("roi.y_offset: " + str(msg.roi.y_offset)+"\n")
    f.write("roi.height: " + str(msg.roi.height)+"\n")
    f.write("roi.width: " + str(msg.roi.width)+"\n")
    f.write("roi.do_rectify: " + str(msg.roi.do_rectify)+"\n")
    print("CIAOOOO")
    print(msg.height)
    print(msg.width)
    print(msg.distortion_model)
    print(msg.D) 
    print(msg.K)
    print(msg.R)
    print(msg.P)
    print(msg.binning_x)
    print(msg.binning_y)
    print(msg.roi.x_offset)
    print(msg.roi.y_offset)
    print(msg.roi.height)
    print(msg.roi.width)
    print(msg.roi.do_rectify)
    f.close()
    rospy.signal_shutdown("") 	


def main():
    rospy.init_node('camera_info_saver_node')   
    path = rospy.get_param('~save_path')

    if(os.path.exists(path)):
        print("ERROR this experiment has bee already recorded")
        return

    rospy.Subscriber('/camera_info_topic', CameraInfo, cameraInfoCallback)
    rospy.spin()


if __name__ == '__main__':
    main()
