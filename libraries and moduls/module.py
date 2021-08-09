from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *
import multiprocessing
import os


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
        #print(angel)
        if angel < 0:
            print(angel)
            angel = 360 + angel
        return angel
        
    def colibrating (self, max_iter):
        self.compass.callibration(max_iter)

def my_gps(checker):
    inf = False
    cord = ()
    while inf == False:
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()
        if checker:
            print("her tebe, connection fail")
        if newdata[0:6] == "$GNRMC":
            newmsg = pynmea2.parse(newdata)
            lat = str(newmsg.latitude)
            lon = str(newmsg.longitude)
            lat = float(lat[0:8])
            lon = float(lon[0:8])
            cord = (lat, lon)
            inf = True
            if checker:
                print("net tebe, o no, it is ok")
    return cord

def midl_cord(size, checker):
    """@size - size of buffers with gps cord"""
    flag = 0
    all_lat, all_lon = [], []
    if checker:
        print('i am inside midl_cord')
    while flag != size:
        cord = my_gps(checker)
        all_lat.append(cord[0])
        all_lon.append(cord[1])
        flag += 1
        if checker:
            print(all_lat, all_lon, "flag - ", flag)
    mid_lat = sum(all_lat)/size
    mid_lon = sum(all_lon)/size
    return mid_lat, mid_lon


class Arduino:
    def __init__(self, bot = 9600, port = '/dev/ttyACM0', timeout_1 = 1, dlin=4):
        self.ser = serial.Serial(port, bot, timeout=timeout_1)
        self.ser.flush()
        for i in range(dlin):
            self.ser.write('9'.encode('ascii'))
            time.sleep(1)
        
    def stopper(self):
        self.ser.write('0'.encode('ascii'))

    def moving(self):
        """arduino controlling function (for start motion)"""
        self.ser.write('1'.encode('ascii'))

    def turn(self):
        """arduino controlling function (for starting rotation)"""
        self.ser.write('2'.encode('ascii'))

    def turn_zero(self):
        """arduino controlling function (for returning wheels at the default state)"""
        self.ser.write('3'.encode('ascii'))
        
class Arduino_send:
    
    def __init__(self):
        self.q = multiprocessing.Queue(maxsize=5)
        self.proc = multiprocessing.Process(target=self.sender_to_ar)
        self.proc.start()
        time.sleep(1)
        
    def sender_to_ar(self):
        print(os.getpid())
        ard = Arduino(dlin=2)
        time.sleep(1)
        while True:
            if self.q.empty() == False:
                out = self.q.get()
                print(out)
                if out == 'stop':
                    ard.stopper()
                    time.sleep(1)
                elif out == 'go':
                    ard.moving()
                    time.sleep(1)
                elif out == 'turn':
                    ard.turn()
                    time.sleep(1)
                elif out == 'turn_zero':
                    ard.turn_zero()
                    time.sleep(1)
                    
    def sender_to_q(self, info):
        #print(self.q.empty())
        if self.q.empty():
            self.q.put(info)
                
    def killer(self):
        self.proc.terminate()
            
        
        
        
