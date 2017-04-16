#!/usr/bin/env python
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import UInt8
import numpy as np

LEFT, FORWARD, RIGHT = 4, 2, 1


def main():
    cap = cv2.VideoCapture(0)
    rospy.init_node('stream_video',anonymous=False)
    front_pub = rospy.Publisher('/image_front_gray_crop', Image, queue_size=1)
    control_pub = rospy.Publisher('/control_signal', UInt8, queue_size=1)
    bridge = CvBridge()
    model = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')
    imgs = []
    for i in range(3):
        try:
            read, frame = cap.read()
            imgs.append(frame)
        except KeyboardInterrupt:
            break
    while not rospy.is_shutdown():
        try:
            read, frame = cap.read()
            imgs.append(frame)
            frame = imgs[0]
            imgs.pop(0)
            if read == True:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_gray_small = cv2.resize(frame_gray, (320, 240))
                frame_gray_small_crop = frame_gray_small[60:180,0:320]
                img_arr = frame_gray_small_crop.reshape(1,38400).astype(np.float32)
                ret, resp = model.predict(img_arr)
                prediction = resp[0].argmax(-1)
                img = bridge.cv2_to_imgmsg(frame_gray_small_crop, 'mono8')
                front_pub.publish(img)
                if prediction == 0:
                    control_pub.publish(FORWARD)
                elif prediction == 1:
                    control_pub.publish(LEFT)
                elif prediction == 2:
                    control_pub.publish(RIGHT)
                elif prediction == 3:
                    control_pub.publish(FORWARD | LEFT)
                elif prediction == 4:
                    control_pub.publish(FORWARD | RIGHT)
		print prediction
        except KeyboardInterrupt:
            break

if __name__=='__main__':
    main()
