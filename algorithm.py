from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *

POINTS = [(43.400081,39.964251), (43.400585,39.963003), (43.399175,39.963610), (43.398381,39.963590), (43.398788,39.964401), (43.399534,39.964645), (43.400143,39.965468)]  # list with tuples (structure: (latitude, longitude)
MISTAKE_LAT = 2                                                    # available mistake of the latitude
MISTAKE_LON = 2                                                    # available mistake of the longitude
MISTAKE_DEG = 2                                                    # available mistake of the degrees


#------RaspberryPi commands--------------------------------------------------------------------------------------------
def my_gps():
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    if newdata[0:6] == "$GPRMC":
        newmsg=pynmea2.parse(newdata)
        cord = (newmsg.latitude, newmsg.longitude)
    else:
        cord = (0,0)
    return cord


def my_angel():
    """function with magnetometer (getting the angel from module)"""
    angel = compas.heading()
    if angel < 0:
        angel = 360 + angel
    return angel

#------Arduino commands------------------------------------------------------------------------------------------------
def stopper():
    print("stop")
    pass


def moving():
    """arduino controlling function (for start motion)"""
    print("go")
    pass


def turn():
    """arduino controlling function (for starting rotation)"""
    print("turning")
    pass


def turn_zero():
    """arduino controlling function (for returning wheels at the default state)"""
    print("stop turning")
    pass

#-----------------------------------------------------------------------------------
mpu = MPU9250()                                    # prosto, suka nado
mpu.initialize()                                   # prosto, suka nado
mpu.gyro_offs =  {'y': -5, 'x': 158, 'z': -100}    # prosto, suka nado
mpu.accel_offs =  {'y': 102, 'x': -34, 'z': -364}  # prosto, suka nado
compas = AK8963()
compas.initialize()
compas.get_calibrated()
delay = 3
time.sleep(1)
#-----------------------------------------------------------------------------------
while True:
    weight = len(POINTS)
    if weight > 0:
        print('number of points - ', weight)
        flag = 0           # creating of the counter (number of the next point-target )
        while flag != weight:
            my_xy = my_gps()
            print('latitude - ', my_xy[0], 'longtude - ', my_xy[1], POINTS[flag])
            if ((my_xy[0] - MISTAKE_LAT) <= POINTS[flag][0] <= (my_xy[0] + MISTAKE_LAT)) and ((my_xy[0] - MISTAKE_LON) <= POINTS[flag][1] <= (my_xy[0] + MISTAKE_LON)):
                flag += 1   # if we are on the point-target
                print('finished points - ', flag)
            else:           # if we aren`t on the point-target
                RotateAngel = Distance(my_gps()[0], my_gps()[1], POINTS[flag][0], POINTS[flag][1]).angle()
                while ((RotateAngel - MISTAKE_DEG > my_angel()) or (my_angel() > RotateAngel + MISTAKE_DEG)):
                    print('my angel - ', my_angel(), 'rotate angel - ', RotateAngel)
                    moving()
                    turn()
                time.sleep(delay)
                turn_zero()
                print("ending of turning")
        stopper()
        print("end")




