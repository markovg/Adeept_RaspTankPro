#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Servos
# Author      : William
# Date        : 2019/02/23
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685
import ultra

from pydub import AudioSegment
from pydub.playback import play

bell = AudioSegment.from_wav("media/bell_short.wav")

import sounddevice as sd
import soundfile as sf

filename = 'myfile.wav'
# Extract data and sampling rate from file
bell = sf.read("media/bell_short.wav", dtype='float32')
def play_sound(data, fs):
        sd.play(data,fs, blocking=True)

from threading import Thread
def play_bell():
        T = Thread(target=play_sound,args=bell)
        T.start()

'''
change this form 1 to 0 to reverse servos
'''
pwm0_direction = 1
pwm1_direction = 0
pwm2_direction = 0
pwm3_direction = 1
pwm4_direction = 0

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm0_init = 300
pwm0_max  = 500
pwm0_min  = 100
pwm0_pos  = pwm0_init

pwm1_init = 350
pwm1_max  = 480
pwm1_min  = 100
pwm1_pos  = pwm1_init

pwm2_init = 350
pwm2_max  = 500
pwm2_min  = 250
pwm2_pos  = pwm2_init

pwm3_init = 300
pwm3_max  = 500
pwm3_min  = 100
pwm3_pos  = pwm3_init

pwm4_init = 300
pwm4_max  = 500
pwm4_min  = 240
pwm4_pos  = pwm4_init

org_pos = 300


def radar_scan():
        global pwm0_pos
        scan_result = 'U: '
        scan_speed = 1
        if pwm0_direction:
                pwm0_pos = pwm0_max
                pwm.set_pwm(0, 0, pwm0_pos)
                time.sleep(0.5)
                scan_result += str(ultra.checkdist())
                scan_result += ' '
                while pwm0_pos>pwm0_min:
                        pwm0_pos-=scan_speed
                        pwm.set_pwm(0, 0, pwm0_pos)
                        scan_result += str(ultra.checkdist())
                        scan_result += ' '
                pwm.set_pwm(0, 0, pwm0_init)
        else:
                pwm0_pos = pwm0_min
                pwm.set_pwm(0, 0, pwm0_pos)
                time.sleep(0.5)
                scan_result += str(ultra.checkdist())
                scan_result += ' '
                while pwm0_pos<pwm0_max:
                        pwm0_pos+=scan_speed
                        pwm.set_pwm(0, 0, pwm0_pos)
                        scan_result += str(ultra.checkdist())
                        scan_result += ' '
                pwm.set_pwm(0, 0, pwm0_init)
        return scan_result





def ctrl_range(raw, max_genout, min_genout):
        if raw > max_genout:
                raw_output = max_genout
                play_bell()
                
        elif raw < min_genout:
                raw_output = min_genout
                play_bell()
        else:
                raw_output = raw
        return int(raw_output)

def ctrl_range_arm(delta_hand, delta_arm, delta_look):
        global pwm0_pos, pwm1_pos, pwm2_pos

        if delta_look!=0:
                if pwm2_pos<430 and pwm1_pos<125:
                        pwm0_pos = ctrl_range(pwm0_pos, pwm0_init+50, pwm0_init-50)
                elif pwm2_pos<380 and pwm1_pos<160:
                        pwm0_pos = ctrl_range(pwm0_pos, pwm0_init+50, pwm0_init-50)
                elif pwm2_pos<350 and pwm1_pos<180:
                        pwm0_pos = ctrl_range(pwm0_pos, pwm0_init+50, pwm0_init-50)
                else:
                        pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)

        if delta_hand!=0:
                # if not facing front, handfown limits are more restrictive
                if pwm0_pos>350 or pwm0_pos<250:
                        if pwm1_pos<125:
                                pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, 430)
                        elif pwm1_pos<160:
                                pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, 380)
                        elif pwm1_pos<180:
                                pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, 350)
                        
                elif pwm1_pos<125:
                        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, 430)
                elif pwm1_pos<160:
                        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, 380)
                elif pwm1_pos<180:
                        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, 350)

        if delta_arm!=0:
                if pwm2_pos<380:
                        pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, 160)
                elif 
                        
                
                        
                        

def camera_ang(direction, ang):
        global org_pos
        if ang == 'no':
                ang = 50
        if look_direction:
                if direction == 'lookdown':
                        org_pos+=ang
                        org_pos = ctrl_range(org_pos, look_max, look_min)
                elif direction == 'lookup':
                        org_pos-=ang
                        org_pos = ctrl_range(org_pos, look_max, look_min)
                elif direction == 'home':
                        org_pos = 300
        else:
                if direction == 'lookdown':
                        org_pos-=ang
                        org_pos = ctrl_range(org_pos, look_max, look_min)
                elif direction == 'lookup':
                        org_pos+=ang
                        org_pos = ctrl_range(org_pos, look_max, look_min)
                elif direction == 'home':
                        org_pos = 300

        pwm.set_all_pwm(0,org_pos)


def lookleft(speed):
        global pwm0_pos
        if pwm0_direction:
                pwm0_pos += speed
        else:
                pwm0_pos -= speed
        #pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
        ctrl_range_arm(0,0,1)
        pwm.set_pwm(0, 0, pwm0_pos)


def lookright(speed):
        global pwm0_pos
        if pwm0_direction:
                pwm0_pos -= speed
        else:
                pwm0_pos += speed       
        #pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
        ctrl_range_arm(0,0,1)
        pwm.set_pwm(0, 0, pwm0_pos)


def up(speed):
        global pwm1_pos
        if pwm1_direction:
                pwm1_pos -= speed
        else:
                pwm1_pos += speed
        #pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
        ctrl_range_arm(0,1,0)
        pwm.set_pwm(1, 0, pwm1_pos)


def down(speed):
        global pwm1_pos
        if pwm1_direction:
                pwm1_pos += speed
        else:
                pwm1_pos -= speed
        #pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
        ctrl_range_arm(0,1,0)
        pwm.set_pwm(1, 0, pwm1_pos)

def handUp(speed):
        global pwm2_pos
        if pwm2_direction:
                pwm2_pos -= speed
        else:
                pwm2_pos += speed
        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
        pwm.set_pwm(2, 0, pwm2_pos)
        #print(pwm1_pos)


def handDown(speed):
        global pwm2_pos
        if pwm2_direction:
                pwm2_pos += speed
        else:
                pwm2_pos -= speed
        pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
        pwm.set_pwm(2, 0, pwm2_pos)
        #print(pwm1_pos)


def lookup(speed):
        global pwm4_pos
        if pwm4_direction:
                pwm4_pos -= speed
        else:
                pwm4_pos += speed
        pwm4_pos = ctrl_range(pwm4_pos, pwm4_max, pwm4_min)
        pwm.set_pwm(4, 0, pwm4_pos)


def lookdown(speed):
        global pwm4_pos
        if pwm4_direction:
                pwm4_pos += speed
        else:
                pwm4_pos -= speed
        pwm4_pos = ctrl_range(pwm4_pos, pwm4_max, pwm4_min)
        pwm.set_pwm(4, 0, pwm4_pos)


def grab(speed):
        global pwm3_pos
        if pwm3_direction:
                pwm3_pos -= speed
        else:
                pwm3_pos += speed
        pwm3_pos = ctrl_range(pwm3_pos, pwm3_max, pwm3_min)
        pwm.set_pwm(3, 0, pwm3_pos)


def loose(speed):
        global pwm3_pos
        if pwm3_direction:
                pwm3_pos += speed
        else:
                pwm3_pos -= speed
        pwm3_pos = ctrl_range(pwm3_pos, pwm3_max, pwm3_min)
        pwm.set_pwm(3, 0, pwm3_pos)


def servo_init():
        pwm.set_pwm(2, 0, pwm2_pos)
        time.sleep(1)
        pwm.set_pwm(0, 0, pwm0_pos)
        pwm.set_pwm(1, 0, pwm1_pos)
        pwm.set_pwm(3, 0, pwm3_pos)
        pwm.set_pwm(4, 0, pwm4_pos)


def clean_all():
        global pwm
        pwm = Adafruit_PCA9685.PCA9685()
        pwm.set_pwm_freq(50)
        pwm.set_all_pwm(0, 0)


def ahead():
        global pwm0_pos, pwm1_pos
        pwm.set_pwm(0, 0, pwm0_init)
        pwm.set_pwm(1, 0, (pwm1_max-20))
        pwm0_pos = pwm0_init
        pwm1_pos = pwm1_max-20


def get_direction():
        return (pwm0_pos - pwm0_init)


if __name__ == '__main__':
        while 0:
                for i in range(0,100):
                        pwm.set_pwm(0,0,(300+i))
                        time.sleep(0.05)
                for i in range(0,100):
                        pwm.set_pwm(0,0,(400-i))
                        time.sleep(0.05)
