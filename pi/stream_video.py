#!/usr/bin/env python
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main():
    cap = cv2.VideoCapture(0)
    rospy.init_node('stream_video',anonymous=False)
    front_pub = rospy.Publisher('/image_front',Image,queue_size=1)
    rate = rospy.Rate(30)
    bridge = CvBridge()
    while not rospy.is_shutdown():
        try:
            read, frame = cap.read()
            if read == True:
                img = bridge.cv2_to_imgmsg(frame, 'bgr8')
                front_pub.publish(img)
        except KeyboardInterrupt:
            break
        rate.sleep()

if __name__ == '__main__':
    main()
