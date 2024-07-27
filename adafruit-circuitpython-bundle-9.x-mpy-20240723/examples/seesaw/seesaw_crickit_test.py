# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from adafruit_motor import servo
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.pwmout import PWMOut

# from analogio import AnalogOut
# import board

i2c_bus = board.I2C()  # uses board.SCL and board.SDA
# i2c_bus = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
ss = Seesaw(i2c_bus)
pwm1 = PWMOut(ss, 17)
pwm2 = PWMOut(ss, 16)
pwm3 = PWMOut(ss, 15)
pwm4 = PWMOut(ss, 14)

pwm1.frequency = 50
pwm2.frequency = 50
pwm3.frequency = 50
pwm4.frequency = 50

S1 = servo.Servo(pwm1)
S2 = servo.Servo(pwm2)
S3 = servo.Servo(pwm3)
S4 = servo.Servo(pwm4)

servos = (S1, S2, S3, S4)

CRCKIT_NUM_ADC = 8
CRCKit_adc = (2, 3, 40, 41, 11, 10, 9, 8)

CRCKIT_NUM_DRIVE = 4
CRCKit_drive = (42, 43, 12, 13)

CAPTOUCH_THRESH = 500

_CRCKIT_M1_A1 = 18
_CRCKIT_M1_A2 = 19
_CRCKIT_M1_B1 = 22
_CRCKIT_M1_B2 = 23

cap_state = [False, False, False, False]
cap_justtouched = [False, False, False, False]
cap_justreleased = [False, False, False, False]

motor1_dir = False
motor2_dir = True

test_servos = False
test_motors = False
test_drives = False
test_speaker = False

counter = 0

# analog_out = AnalogOut(board.A0)
# analog_out.value = 512

while True:
    counter = (counter + 1) % 256

    if counter % 32 == 0:
        print("-------------------- analog -----------------------")
        str_out = ""
        for i in range(8):
            val = ss.analog_read(CRCKit_adc[i]) * 3.3 / 1024
            str_out = str_out + str(round(val, 2)) + "\t"

        print(str_out + "\n")

    for i in range(4):
        val = ss.touch_read(i)
        cap_justtouched[i] = False
        cap_justreleased[i] = False

        if val > CAPTOUCH_THRESH:
            print("CT" + str(i + 1) + " touched! value: " + str(val))

            if not cap_state[i]:
                cap_justtouched[i] = True

            cap_state[i] = True

        else:
            if cap_state[i]:
                cap_justreleased[i] = True

            cap_state[i] = False

    if cap_justtouched[0]:
        test_servos = not test_servos
        if test_servos:
            print("Testing servos")
        else:
            print("Stopping servos")

    if cap_justtouched[1]:
        test_drives = not test_drives
        if test_drives:
            print("Testing drives")
        else:
            print("Stopping drives")

    if cap_justtouched[2]:
        test_motors = not test_motors
        if test_motors:
            print("Testing motors")
        else:
            print("Stopping motors")

    if cap_justtouched[3]:
        test_speaker = not test_speaker
        if test_speaker:
            print("Testing speaker")
        else:
            print("Stopping speaker")

    if test_servos:
        if counter % 32 == 0:
            print("-------------------- servos -----------------------")
            servonum = int(counter / 32) % 4

            if counter < 128:
                print("SER" + str(servonum) + " LEFT")
                servos[servonum].angle = 0
            else:
                print("SER" + str(servonum) + " RIGHT")
                servos[servonum].angle = 180

    if test_drives:
        if counter % 32 == 0:
            print("-------------------- drives -----------------------")
            drivenum = int(counter / 64) % 4

            if counter % 64 == 0:
                print("DRIVE" + str(drivenum) + " ON")
                ss.analog_write(CRCKit_drive[drivenum], 65535)

            else:
                print("DRIVE" + str(drivenum) + " OFF")
                ss.analog_write(CRCKit_drive[drivenum], 0)

    if test_motors:
        if counter < 128:
            if motor1_dir:
                ss.analog_write(_CRCKIT_M1_A1, 0)
                ss.analog_write(_CRCKIT_M1_A2, counter * 512)
            else:
                ss.analog_write(_CRCKIT_M1_A2, 0)
                ss.analog_write(_CRCKIT_M1_A1, counter * 512)
        else:
            if motor1_dir:
                ss.analog_write(_CRCKIT_M1_A1, 0)
                ss.analog_write(_CRCKIT_M1_A2, (255 - counter) * 512)
            else:
                ss.analog_write(_CRCKIT_M1_A2, 0)
                ss.analog_write(_CRCKIT_M1_A1, (255 - counter) * 512)
        if counter == 255:
            print("-------------------- motor 1 -----------------------")
            motor1_dir = not motor1_dir

        if counter < 128:
            if motor2_dir:
                ss.analog_write(_CRCKIT_M1_B1, 0)
                ss.analog_write(_CRCKIT_M1_B2, counter * 512)
            else:
                ss.analog_write(_CRCKIT_M1_B2, 0)
                ss.analog_write(_CRCKIT_M1_B1, counter * 512)
        else:
            if motor2_dir:
                ss.analog_write(_CRCKIT_M1_B1, 0)
                ss.analog_write(_CRCKIT_M1_B2, (255 - counter) * 512)
            else:
                ss.analog_write(_CRCKIT_M1_B2, 0)
                ss.analog_write(_CRCKIT_M1_B1, (255 - counter) * 512)
        if counter == 255:
            print("-------------------- motor 2 -----------------------")
            motor2_dir = not motor2_dir
