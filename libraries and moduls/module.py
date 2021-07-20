from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *


class Compass:

    def __init__(self):
        self.mpu = MPU9250()
        self.mpu.initialize()
        self.mpu.gyro_offs = {'y': -5, 'x': 158, 'z': -100}
        self.mpu.accel_offs = {'y': 102, 'x': -34, 'z': -364}
        self.compass = AK8963()
        self.compass.initialize()
        self.compass.get_calibrated()
        time.sleep(1)

    def my_angel(self):
        """function with magnetometer (getting the angel from module)"""
        angel = self.compass.heading()
        if angel < 0:
            angel = 360 + angel
        return angel

def my_gps():
    inf = False
    cord = ()
    while inf == False:
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()
        if newdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(newdata)
            cord = (newmsg.latitude, newmsg.longitude)
            inf = True
    return cord

def midl_cord(size, checker):
    """@size - size of buffers with gps cord"""
    flag = 0
    all_lat, all_lon = [], []
    while flag != size:
        cord = my_gps()
        all_lat.append(cord[0])
        all_lon.append(cord[1])
        flag += 1
        if checker:
            print(all_lat, all_lon, "flag - ", flag)
    mid_lat = sum(all_lat)/size
    mid_lon = sum(all_lon)/size
    return mid_lat, mid_lon

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
