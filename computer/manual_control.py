#!/usr/bin/env python
import pygame
from pygame.locals import *
import rospy
from std_msgs.msg import UInt8

LEFT, FORWARD, RIGHT, STOP = 4, 2, 1, 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    rospy.init_node('manual_control_computer',anonymous=False)
    control_pub = rospy.Publisher('/control_signal',UInt8,queue_size=1)
    rate = rospy.Rate(30)
    control = True
    while not rospy.is_shutdown() and control:
        try:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                    key_input = pygame.key.get_pressed()
                    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                        print "Forward-Right"
                        control_pub.publish(FORWARD | RIGHT)
                    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                        print "Forward-Left"
                        control_pub.publish(FORWARD | LEFT)
                    elif key_input[pygame.K_UP]:
                        print "Forward"
                        control_pub.publish(FORWARD)
                    elif key_input[pygame.K_LEFT]:
                        print "Left"
                        control_pub.publish(LEFT)
                    elif key_input[pygame.K_RIGHT]:
                        print "Right"
                        control_pub.publish(RIGHT)
                    else:
                        print "Stop"
                        control_pub.publish(STOP)
                elif e.type == pygame.QUIT:
                    control = False
        except KeyboardInterrupt:
            break
        rate.sleep()


if __name__=='__main__':
    main()
