import pygame
from pygame.locals import *
import serial

def main():
    control = True
    s = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    while(control):
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                key_input = pygame.key.get_pressed()

                if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                    print "Forward-Right"
                    s.write("O1%L150%R0%")
                elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                    print "Forward-Left"
                    s.write("O1%L0%R150%")
                elif key_input[pygame.K_UP]:
                    print "Forward"
                    s.write("O1%L150%R150%")
                elif key_input[pygame.K_LEFT]:
                    print "Left"
                    s.write("O2%L150%R150%")
                elif key_input[pygame.K_RIGHT]:
                    print "Right"
                    s.write("O3%L150%R150%")

            elif e.type == KEYUP:
                print "Stop"
                s.write("O1%L0%R0%")

if __name__=='__main__':
    main()
