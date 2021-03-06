#!/usr/bin/env python

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import UInt8

LEFT, FORWARD, RIGHT, STOP = 4, 2, 1, 0
frame = None
control_sig = None
fullFrame = None
bridge = CvBridge()

def controlCallback(msg):
    global control_sig
    control_sig = msg.data

def cascade(msg):
    global fullFrame
    try:
        fullFrame = bridge.imgmsg_to_cv2(msg, 'mono8')
    except CvBridgeError as e:
        print e

def storeNextFrame(msg):
    global frame
    try:
        frame = bridge.imgmsg_to_cv2(msg, 'mono8')
    except CvBridgeError as e:
        print e

def main():
    rospy.init_node('collect_training_data', anonymous=False)
    rospy.Subscriber('/image_front_gray_crop', Image, storeNextFrame)
    rospy.Subscriber('/image_front', Image, cascade)
    rospy.Subscriber('/control_signal',UInt8,controlCallback)
    while not rospy.is_shutdown():
        try:
            if control_sig!=None and fullFrame!=None:
                #cv2.imshow('Image',frame)
                cv2.imshow('Stop',fullFrame)
                cv2.waitKey(1)
                if control_sig == FORWARD:
                    print "Forward"
                elif control_sig == RIGHT:
                    print "Right"
                elif control_sig == LEFT:
                    print "Left"
                elif control_sig == FORWARD | RIGHT:
                    print "Forward-Right"
                elif control_sig == FORWARD | LEFT:
                    print "Forward-Left"
        except KeyboardInterrupt:
            break
#        rate.sleep()

if __name__ == "__main__":
    main()
