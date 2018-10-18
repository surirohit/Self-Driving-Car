#!/usr/bin/env python
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import UInt8
import numpy as np

LEFT, FORWARD, RIGHT = 4, 2, 1

import math
alpha = 25.0 * math.pi / 180
v0 = 239.5
ay = 521.52
def calculate(v, h, x_shift, image):
    d = h / math.tan(alpha + math.atan((v - v0) / ay))
    if d > 0:
        cv2.putText(image, "%.1fcm" % d,
            (image.shape[1] - x_shift, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return d

def main():
    cap = cv2.VideoCapture(0)
    rospy.init_node('stream_video',anonymous=False)
    front_pub = rospy.Publisher('/image_front_gray_crop', Image, queue_size=1)
    front_pub_full = rospy.Publisher('/image_front', Image, queue_size=1)
    control_pub = rospy.Publisher('/control_signal', UInt8, queue_size=1)
    bridge = CvBridge()
    model = cv2.ml.ANN_MLP_load('mlp_xml/mlp.xml')
    stopCascade = cv2.CascadeClassifier('cascade_xml/stop_sign.xml')
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
                cascade_obj = stopCascade.detectMultiScale(frame_gray_small,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
        	for (x_pos, y_pos, width, height) in cascade_obj:
            	    cv2.rectangle(frame_gray_small, (x_pos+5, y_pos+5), (x_pos+width-5, y_pos+height-5), (255, 255, 255), 2)
            	    calculate(y_pos+height-5,22-18,300,frame_gray_small)
                img = bridge.cv2_to_imgmsg(frame_gray_small, 'mono8')
                front_pub_full.publish(img)
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
