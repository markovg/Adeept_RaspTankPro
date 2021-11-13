#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Product     : GWR
# Website     : www.gewbot.com
# Author      : William
# Date        : 2019/07/24
import time
import RPi.GPIO as GPIO

import pyttsx3
from time import sleep
import sys

import servo

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 26
Motor_A_Pin2  = 21
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

left_forward  = 1
left_backward = 0

right_forward = 0
right_backward= 1

pwn_A = 0
pwm_B = 0

def motorStop():#Motor stops
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)


def setup():#Motor initialization
        global pwm_A, pwm_B
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Motor_A_EN, GPIO.OUT)
        GPIO.setup(Motor_B_EN, GPIO.OUT)
        GPIO.setup(Motor_A_Pin1, GPIO.OUT)
        GPIO.setup(Motor_A_Pin2, GPIO.OUT)
        GPIO.setup(Motor_B_Pin1, GPIO.OUT)
        GPIO.setup(Motor_B_Pin2, GPIO.OUT)

        motorStop()
        try:
                pwm_A = GPIO.PWM(Motor_A_EN, 1000)
                pwm_B = GPIO.PWM(Motor_B_EN, 1000)
        except:
                pass


def motor_left(status, direction, speed):#Motor 2 positive and negative rotation
        if status == 0: # stop
                GPIO.output(Motor_B_Pin1, GPIO.LOW)
                GPIO.output(Motor_B_Pin2, GPIO.LOW)
                GPIO.output(Motor_B_EN, GPIO.LOW)
        else:
                if direction == Dir_backward:
                        GPIO.output(Motor_B_Pin1, GPIO.HIGH)
                        GPIO.output(Motor_B_Pin2, GPIO.LOW)
                        pwm_B.start(100)
                        pwm_B.ChangeDutyCycle(speed)
                elif direction == Dir_forward:
                        GPIO.output(Motor_B_Pin1, GPIO.LOW)
                        GPIO.output(Motor_B_Pin2, GPIO.HIGH)
                        pwm_B.start(0)
                        pwm_B.ChangeDutyCycle(speed)


def motor_right(status, direction, speed):#Motor 1 positive and negative rotation
        if status == 0: # stop
                GPIO.output(Motor_A_Pin1, GPIO.LOW)
                GPIO.output(Motor_A_Pin2, GPIO.LOW)
                GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
                if direction == Dir_forward:#
                        GPIO.output(Motor_A_Pin1, GPIO.HIGH)
                        GPIO.output(Motor_A_Pin2, GPIO.LOW)
                        pwm_A.start(100)
                        pwm_A.ChangeDutyCycle(speed)
                elif direction == Dir_backward:
                        GPIO.output(Motor_A_Pin1, GPIO.LOW)
                        GPIO.output(Motor_A_Pin2, GPIO.HIGH)
                        pwm_A.start(0)
                        pwm_A.ChangeDutyCycle(speed)
        return direction


def move(speed, direction, turn, radius=0.6):   # 0 < radius <= 1
        #speed = 100
        if direction == 'forward':
                if turn == 'right':
                        motor_left(0, left_backward, int(speed*radius))
                        motor_right(1, right_forward, speed)
                elif turn == 'left':
                        motor_left(1, left_forward, speed)
                        motor_right(0, right_backward, int(speed*radius))
                else:
                        motor_left(1, left_forward, speed)
                        motor_right(1, right_forward, speed)
        elif direction == 'backward':
                if turn == 'right':
                        motor_left(0, left_forward, int(speed*radius))
                        motor_right(1, right_backward, speed)
                elif turn == 'left':
                        motor_left(1, left_backward, speed)
                        motor_right(0, right_forward, int(speed*radius))
                else:
                        motor_left(1, left_backward, speed)
                        motor_right(1, right_backward, speed)
        elif direction == 'no':
                if turn == 'right':
                        motor_left(1, left_backward, speed)
                        motor_right(1, right_forward, speed)
                elif turn == 'left':
                        motor_left(1, left_forward, speed)
                        motor_right(1, right_backward, speed)
                else:
                        motorStop()
        else:
                pass




def destroy():
        motorStop()
        GPIO.cleanup()             # Release resource



        
def move_arm(move_str, steps, sleeptime=0.05):
        func = servo.__getattribute__(move_str)
        for i in range(0,steps):
                func(1)
                sleep(sleeptime)

if __name__ == '__main__':
        try:

                servo.servo_init()
                #servo.clean_all()
                st = 0.005
                # move_arm('handUp',50, st)
                # move_arm('handDown',50, st)
                # move_arm('up',50,st)
                # move_arm('down',50, st)
                # move_arm('handUp',50, st)
                # move_arm('handDown',50, st)
                # move_arm('lookup',50, st)
                # move_arm('lookdown',50, st)
                # move_arm('lookleft',50, st)
                # move_arm('lookright',50, st)
                # move_arm('grab',50, st)
                # #move_arm('loose',50, st)

                engine = pyttsx3.init()
                engine.say("Hello")
                engine.runAndWait()
                sleep(0.5)
                engine.say("My name is Jeffrey and I like to dance!")
                engine.runAndWait()

                
                # arm wave
                import numpy as np
                for angle in np.arange(0,4*np.pi,0.2):
                        pwm1_pos = int(80*np.sin(angle)) + servo.pwm1_pos
                        pwm0_pos = int(80*np.sin(angle)) + servo.pwm0_pos

                        pwm2_pos = int(120*np.sin(angle-np.pi/3)) + servo.pwm2_pos - int(120*np.sin(-np.pi/3))
                        pwm1_pos = servo.ctrl_range(pwm1_pos, servo.pwm1_max, servo.pwm1_min)
                        servo.pwm.set_pwm(1, 0, pwm1_pos)
                        pwm2_pos = servo.ctrl_range(pwm2_pos, servo.pwm2_max, servo.pwm2_min)
                        servo.pwm.set_pwm(2, 0, pwm2_pos)

                        pwm0_pos = servo.ctrl_range(pwm0_pos, servo.pwm0_max, servo.pwm0_min)
                        servo.pwm.set_pwm(0, 0, pwm0_pos)

                        sleep(0.05)

                        
                        
                        #move_arm('up', int(80*np.sin(angle)))
                        

                
                
                
                

                speed_set = 100
                setup()
                t = 2.3
                rad = 1.0
                move(speed_set, 'forward', 'no', rad)
                time.sleep(t)
                motorStop()

                move(speed_set, 'backward', 'no', rad)
                time.sleep(t)
                motorStop()

                move(speed_set, 'forward', 'left', rad)
                time.sleep(t)
                motorStop()

                move(speed_set, 'backward', 'left', rad)
                time.sleep(t)
                motorStop()

                #Rotate left
                move(speed_set, 'no', 'left', None)
                time.sleep(2.0)
                motorStop()

                #Rotate left
                move(speed_set, 'no', 'right', None)
                time.sleep(2.0)
                motorStop()



                destroy()
        except KeyboardInterrupt:
                destroy()
