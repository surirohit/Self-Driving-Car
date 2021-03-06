#!/usr/bin/env python

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import UInt8

LEFT, FORWARD, RIGHT, STOP = 4, 2, 1, 0
frame = None
control_sig = None
bridge = CvBridge()

def controlCallback(msg):
    control_sig = msg.data

def storeNextFrame(msg):
    global frame
    try:
        frame = bridge.imgmsg_to_cv2(msg, 'mono8')
    except CvBridgeError as e:
        print e

def main():
    rospy.init_node('collect_training_data', anonymous=False)
    rospy.Subscriber('/image_front_gray_crop', Image, storeNextFrame)
    rospy.Subscriber('/control_signal',UInt8, controlCallback)
    while not rospy.is_shutdown():
        try:
            if frame != None and controlCallback != None:
                cv2.imshow('Image',frame)
                cv2.waitKey(1)
                if control_sig == FORWARD:
                    print "Forward"
                elif control_sig == LEFT:
                    print "Left"
                elif control_sig == RIGHT:
                    print "Right"
                elif control_sig == FORWARD | LEFT:
                    print "Forward-Left"
                elif control_sig == FORWARD | RIGHT:
                    print "Forward-Right"
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
