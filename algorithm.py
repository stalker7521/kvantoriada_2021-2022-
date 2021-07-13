from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *

POINTS = [(0, 0), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]  # list with tuples (structure: (latitude, longitude)
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
mpu = MPU9250()
mpu.initialize()
compas = AK8963()
compas.initialize()
compas.get_calibrated()
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
                turn_zero()
                print("ending of turning")
        stopper()
        print("end")




