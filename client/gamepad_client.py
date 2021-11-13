#!/usr/bin/python3
# -*- coding: utf-8 -*-
# File name   : client.py
# Description : client
# Website	 : www.adeept.com
# Author	  : William
# Date		: 2019/08/28

from socket import *
import sys
import time
import threading as thread
import math
import numpy as np

import pygame

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')


OSD_X = 0#1
OSD_Y = 0
advanced_OSD = 0

def global_init():
        global DS_stu, TS_stu, color_bg, color_text, color_btn, color_line, color_can, color_oval, target_color
        global speed, ip_stu, Switch_3, Switch_2, Switch_1, servo_stu, servos_moving, function_stu
        DS_stu = 0
        TS_stu = 0

        color_bg='#000000'		#Set background color
        color_text='#E1F5FE'	  #Set text color
        color_btn='#0277BD'	   #Set button color
        color_line='#01579B'	  #Set line color
        color_can='#212121'	   #Set canvas color
        color_oval='#2196F3'	  #Set oval color
        target_color='#FF6D00'
        speed = 1
        ip_stu=1

        Switch_3 = 0
        Switch_2 = 0
        Switch_1 = 0

        servo_stu = 0
        servos_moving = [0,0,0,0,0,0]
        function_stu = 0


global_init()


def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
        newline=""
        str_num=str(new_num)
        with open("ip.txt","r") as f:
                for line in f.readlines():
                        if(line.find(initial) == 0):
                                line = initial+"%s" %(str_num)
                        newline += line
        with open("ip.txt","w") as f:
                f.writelines(newline)	#Call this function to replace data in '.txt' file


def num_import(initial):			#Call this function to import data from '.txt' file
        with open("ip.txt") as f:
                for line in f.readlines():
                        if(line.find(initial) == 0):
                                r=line
        begin=len(list(initial))
        snum=r[begin:]
        n=snum
        return n


def socket_connect():	 #Call this function to connect with the server
        global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr
        ip_adr="192.168.1.25"

        SERVER_IP = ip_adr
        SERVER_PORT = 10223   #Define port serial
        #SERVER_PORT = 5000   #Define port serial
        BUFSIZ = 1024		 #Define buffer size
        ADDR = (SERVER_IP, SERVER_PORT)
        tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

        for i in range (1,6): #Try 5 times if disconnected
                #try:
                if ip_stu == 1:
                        print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
                        print("Connecting")
                        tcpClicSock.connect(ADDR)		#Connection with the server

                        print("Connected")


                        ip_stu=0						 #'0' means connected

                        break
                else:
                        print("Cannot connecting to server,try it latter!")
                        ip_stu=1
                        time.sleep(1)
                        continue



def connect():	   #Call this function to connect with the server
        if ip_stu == 1:
                sc=thread.Thread(target=socket_connect) #Define a thread for connection
                sc.setDaemon(True)					  #'True' means it is a front thread,it would close when the mainloop() closes
                sc.start()							  #Thread starts
        return sc

def scale_send(event=None):
        time.sleep(0.03)
        tcpClicSock.send(('wsB %s;'%var_Speed.get()).encode())


def call_up(event=None):
        global servos_moving
        if servos_moving[1] != 1:
                tcpClicSock.send(('up;').encode())
                servos_moving[1] = 1

def call_down(event=None):
        global servos_moving
        if servos_moving[1] != -1:
                tcpClicSock.send(('down;').encode())
                servos_moving[1] = -1
def call_armstop(event=None):
        global servos_moving
        if servos_moving[1] != 0:
                tcpClicSock.send(('armstop;').encode())
                servos_moving[1] = 0

def call_handup(event=None):
        global servos_moving
        if servos_moving[0] != 1:
                tcpClicSock.send(('handup;').encode())
                servos_moving[0] = 1

def call_handdown(event=None):
        global servos_moving
        if servos_moving[0] != -1:
                tcpClicSock.send(('handdown;').encode())
                servos_moving[0] = -1

def call_handstop(event=None):
        global servos_moving
        if servos_moving[0] != 0:
                tcpClicSock.send(('handstop;').encode())
                servos_moving[0] = 0

def call_lookleft(event=None):
        global servos_moving
        if servos_moving[3] != -1:
                tcpClicSock.send(('lookleft;').encode())
                servos_moving[3] = -1

def call_lookright(event=None):
        global servos_moving
        if servos_moving[3] != 1:
                tcpClicSock.send(('lookright;').encode())
                servos_moving[3] = 1

def call_lookhstop(event=None):
        global servos_moving
        if servos_moving[3] != 0:
                tcpClicSock.send(('lookhstop;').encode())
                servos_moving[3] = 0

def call_lookup(event=None):
        global servos_moving
        if servos_moving[4] != 1:
                tcpClicSock.send(('lookup;').encode())
                servos_moving[4] = 1

def call_lookdown(event=None):
        global servos_moving
        if servos_moving[4] != -1:
                tcpClicSock.send(('lookdown;').encode())
                servos_moving[4] = -1

def call_lookvstop(event=None):
        global servos_moving
        if servos_moving[4] != 0:
                tcpClicSock.send(('lookvstop;').encode())
                servos_moving[4] = 0

def call_grab(event=None):
        global servos_moving
        if servos_moving[5] != 1:
                tcpClicSock.send(('grab;').encode())
                servos_moving[5] = 1

def call_loose(event=None):
        global servos_moving
        if servos_moving[5] != -1:
                tcpClicSock.send(('loose;').encode())
                servos_moving[5] = -1

def call_grabstop(event=None):
        global servos_moving
        if servos_moving[5] != 0:
                tcpClicSock.send(('grabstop;').encode())
                servos_moving[5] = 0

def call_stop(event=None):
        global servo_stu
        tcpClicSock.send(('stop;').encode())
        servo_stu = 0

def call_home(event=None):
        tcpClicSock.send(('home;').encode())
        time.sleep(0.15)



def call_left(event=None):
        global TS_stu
        if TS_stu != -1:
                tcpClicSock.send(('left;').encode())
                TS_stu = -1

def call_right(event=None):
        global TS_stu
        if TS_stu != 1:
                tcpClicSock.send(('right;').encode())
                TS_stu = 1

def call_forward(event=None):
        global DS_stu
        if DS_stu != 1:
                tcpClicSock.send(('forward;').encode())
                DS_stu = 1

def call_backward(event=None):
        global DS_stu
        if DS_stu != -1:
                tcpClicSock.send(('backward;').encode())
                DS_stu = -1

def call_DS(event=None):
        global DS_stu
        tcpClicSock.send(('DS;').encode())
        DS_stu = 0

def call_TS(event=None):
        global TS_stu
        tcpClicSock.send(('TS;').encode())
        TS_stu = 0

def servoStop(event=None):
        global servo_stu
        servo_stu = 0
        tcpClicSock.send(('stop;').encode())



def call_Switch_1(event=None):
        if Switch_1 == 0:
                tcpClicSock.send(('Switch_1_on;').encode())
        else:
                tcpClicSock.send(('Switch_1_off;').encode())


def call_Switch_2(event=None):
        if Switch_2 == 0:
                tcpClicSock.send(('Switch_2_on;').encode())
        else:
                tcpClicSock.send(('Switch_2_off;').encode())


def call_Switch_3(event=None):
        if Switch_3 == 0:
                tcpClicSock.send(('Switch_3_on;').encode())
        else:
                tcpClicSock.send(('Switch_3_off;').encode())

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10




if __name__ == '__main__':

        sc = connect()
        time.sleep(2)

        pygame.init()

        # Set the width and height of the screen (width, height).
        screen = pygame.display.set_mode((500, 700))

        pygame.display.set_caption("My Game")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates.
        clock = pygame.time.Clock()

        # Initialize the joysticks.
        pygame.joystick.init()
        joy = pygame.joystick.Joystick(0)

        # Safety timer to ensure check joystate on regular interval
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        # Get ready to print.
        textPrint = TextPrint()

        # -------- Main Program Loop -----------
        while not done:
            #
            # EVENT PROCESSING STEP
            #
            # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
            # JOYBUTTONUP, JOYHATMOTION
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.QUIT: # If user clicked close.
                    done = True # Flag that we are done so we exit this loop.
                elif event.type == pygame.JOYBUTTONDOWN:
                        if joy.get_button(0):
                                tcpClicSock.send(('bark').encode())
                elif event.type in [pygame.JOYAXISMOTION, pygame.JOYHATMOTION, pygame.USEREVENT]:
                        hat_state = joy.get_hat(0)
                        if hat_state[0] == 0:
                                # TS = turn stop
                                call_handstop()
                        elif hat_state[0] == -1:
                                call_handdown()
                        elif hat_state[0] == 1:
                                call_handup()

                        if hat_state[1] == 0:
                                # DS = drive stop
                                call_armstop()
                        elif hat_state[1] == 1:
                                call_up()
                        elif hat_state[1] == -1:
                                call_down()
                                        
                        axis_state = [joy.get_axis(i) for i in range(joy.get_numaxes())]
                        axst = np.array(axis_state)
                        # ignore center fluctuations
                        axst[np.abs(axst)<0.1] = 0.0
                        if axst[4]>0.5:
                                call_lookup()
                        elif axst[4]<-0.5:
                                call_lookdown()
                        else:
                                call_lookvstop()

                        if axst[3]>0.5:
                                call_lookright()
                        elif axst[3]<-0.5:
                                call_lookleft()
                        else:
                                call_lookhstop()

                        if axst[1]>0.5:
                                # arm
                                #call_up()
                                call_backward()
                        elif axst[1]<-0.5:
                                #call_down()
                                call_forward()
                        else:
                                #call_armstop()
                                call_DS()

                        if axst[0]>0.5:
                                #call_handup()
                                call_left()
                        elif axst[0]<-0.5:
                                #call_handdown()
                                call_right()
                        else:
                                #call_handstop()
                                call_TS()

                        if axst[2]>0.5:
                                call_grab()
                        elif axst[5]>0.5:
                                call_loose()
                        else:
                                call_grabstop()
                        


                        
        #TODO:
        # Map joy axis to movement commands
        # https://www.programcreek.com/python/example/56152/pygame.JOYAXISMOTION


            #
            # DRAWING STEP
            #
            # First, clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            screen.fill(WHITE)
            textPrint.reset()

            # Get count of joysticks.
            joystick_count = pygame.joystick.get_count()

            textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
            textPrint.indent()

            # For each joystick:
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                try:
                    jid = joystick.get_instance_id()
                except AttributeError:
                    # get_instance_id() is an SDL2 method
                    jid = joystick.get_id()
                textPrint.tprint(screen, "Joystick {}".format(jid))
                textPrint.indent()

                # Get the name from the OS for the controller/joystick.
                name = joystick.get_name()
                textPrint.tprint(screen, "Joystick name: {}".format(name))

                try:
                    guid = joystick.get_guid()
                except AttributeError:
                    # get_guid() is an SDL2 method
                    pass
                else:
                    textPrint.tprint(screen, "GUID: {}".format(guid))

                # Usually axis run in pairs, up/down for one, and left/right for
                # the other.
                axes = joystick.get_numaxes()
                textPrint.tprint(screen, "Number of axes: {}".format(axes))
                textPrint.indent()

                for i in range(axes):
                    axis = joystick.get_axis(i)
                    textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
                textPrint.unindent()

                buttons = joystick.get_numbuttons()
                textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
                textPrint.indent()

                for i in range(buttons):
                    button = joystick.get_button(i)
                    textPrint.tprint(screen,
                                     "Button {:>2} value: {}".format(i, button))
                textPrint.unindent()

                hats = joystick.get_numhats()
                textPrint.tprint(screen, "Number of hats: {}".format(hats))
                textPrint.indent()

                # Hat position. All or nothing for direction, not a float like
                # get_axis(). Position is a tuple of int values (x, y).
                for i in range(hats):
                    hat = joystick.get_hat(i)
                    textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
                textPrint.unindent()

                textPrint.unindent()

            #
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
            #

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # Limit to 20 frames per second.
            clock.tick(20)

        # Close the window and quit.
        # If you forget this line, the program will 'hang'
        # on exit if running from IDLE.
        pygame.quit()



        # call_backward()
        # time.sleep(1)
        # call_DS()
        # call_forward()
        # time.sleep(1)
        # call_DS()
        # call_right()
        # time.sleep(1)
        # call_TS()
        # call_left()
        # time.sleep(1)
        # call_TS()
