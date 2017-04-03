#!/usr/bin/env python

# Controls are slightly different here for ease of creation of image set
import cv2
import rospy
import pygame
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from pygame.locals import *
from std_msgs.msg import UInt8

LEFT, FORWARD, RIGHT, STOP = 4, 2, 1, 0
frame = None
bridge = CvBridge()

def storeNextFrame(msg):
    global frame
    try:
        frame = bridge.imgmsg_to_cv2(msg, 'bgr8')
    except CvBridgeError as e:
        print e

def main():
    rospy.init_node('collect_training_data', anonymous=False)
    rospy.Subscriber('/image_front', Image, storeNextFrame)
    control_pub = rospy.Publisher('/control_signal',UInt8,queue_size=1)
    rate = rospy.Rate(30)
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    control = True
    counter = [0,0,0,0,0]
    while not rospy.is_shutdown() and control:
        try:
            if frame != None:
                cv2.imshow('Image',frame)
                cv2.waitKey(1)
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        key_input = pygame.key.get_pressed()
                        if key_input[pygame.K_KP9]:
                            print 'Forward-Right'
                            cv2.imwrite('training_images/forward-right/img'+str(counter[0])+'.jpg',frame)
                            counter[0]+=1
                            control_pub.publish(FORWARD | RIGHT)
                        elif key_input[pygame.K_KP7]:
                            print 'Forward-Left'
                            cv2.imwrite('training_images/forward-left/img'+str(counter[1])+'.jpg',frame)
                            counter[1]+=1
                            control_pub.publish(FORWARD | LEFT)
                        elif key_input[pygame.K_KP8]:
                            print 'Forward'
                            cv2.imwrite('training_images/forward/img'+str(counter[2])+'.jpg',frame)
                            counter[2]+=1
                            control_pub.publish(FORWARD)
                        elif key_input[pygame.K_KP4]:
                            print 'Left'
                            cv2.imwrite('training_images/left/img'+str(counter[3])+'.jpg',frame)
                            counter[3]+=1
                            control_pub.publish(LEFT)
                        elif key_input[pygame.K_KP6]:
                            print 'Right'
                            cv2.imwrite('training_images/right/img'+str(counter[4])+'.jpg',frame)
                            counter[4]+=1
                            control_pub.publish(RIGHT)
                        else:
                            print 'Stop'
                            control_pub.publish(STOP)
                    elif e.type == pygame.KEYUP:
                        print 'Stop'
                        control_pub.publish(STOP)
                    elif e.type == pygame.QUIT:
                        control = False
        except KeyboardInterrupt:
            break
        rate.sleep()

if __name__ == "__main__":
    main()
