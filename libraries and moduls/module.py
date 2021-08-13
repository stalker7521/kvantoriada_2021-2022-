from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *
import multiprocessing
import os


########################################################################
class Compass:

    def __init__(self):
        self.mpu = MPU9250()
        self.mpu.initialize()
        self.mpu.gyro_offs = {'y': 29, 'x': 143, 'z': -11}
        self.mpu.accel_offs = {'y': -160, 'x': -358, 'z': 8472}
        self.compass = AK8963()
        self.compass.initialize()
        self.compass.get_calibrated()
        time.sleep(1)

    def my_angel(self):
        """function with magnetometer (getting the angel from module)"""
        angel = self.compass.heading()
        if angel < 0:
            #print(angel)
            angel = 360 + angel
        return angel
        
    def colibrating (self, max_iter):
        self.compass.callibration(max_iter)
        
    def average_ang(self, num):
        all_angels = []
        for i in range(num):
            ang = self.my_angel()
            all_angels.append(ang)
        average = sum(all_angels)/num
        return average 
    
########################################################################

def my_gps(checker):   
    """function for getting gps cords"""
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
########################################################################

class Arduino:
    
    def __init__(self, bot = 9600, port = '/dev/ttyUSB0', timeout_1 = 1, dlin=4):
        self.ser = serial.Serial(port, bot, timeout=timeout_1)
        self.ser.flush()
        #-------------------------------#
        self.TURN_RIGHT = '3'
        self.TURN_LEFT = '2'
        self.TURN_ZERO = '4'
        self.STOP = '0'
        self.GO = '1' 
        #-------------------------------#
        for i in range(dlin):
            self.ser.write('9'.encode('ascii'))
            time.sleep(1)
        
    def stopper(self):
        self.ser.write(self.STOP.encode('ascii'))

    def moving(self):
        """arduino controlling function (for start motion)"""
        self.ser.write(self.GO.encode('ascii')) 
        print('ok')

    def turn_right(self):
        """arduino controlling function (for starting rotation)"""
        self.ser.write(self.TURN_RIGHT.encode('ascii'))
        
    def turn_left(self):
        """arduino controlling function (for starting rotation)"""
        self.ser.write(self.TURN_LEFT.encode('ascii'))

    def turn_zero(self):
        """arduino controlling function (for returning wheels at the default state)"""
        self.ser.write(self.TURN_ZERO.encode('ascii'))
        
########################################################################
        
class Arduino_send:
    
    def __init__(self, timeout = 0.1):
        self.timeout = timeout
        self.q = multiprocessing.Queue(maxsize=5)
        self.proc = multiprocessing.Process(target=self.sender_to_ar)
        self.proc.start()
        #time.sleep(1)
        
    def sender_to_ar(self):
        try:
            #--------------------------#
            turn_zero = 'turn_zero'
            turn_left = 'turn_left'
            turn_right = 'turn_right'
            stop = 'stop'
            go = 'go'
            #--------------------------#    
            print(os.getpid())
            ard = Arduino(dlin=2)
            time.sleep(1)
            while True:
                if self.q.empty() == False:
                    out = self.q.get()
                    print(out)
                    if out == stop:
                        ard.stopper()
                        time.sleep(self.timeout)
                    elif out == go:
                        ard.moving()
                        time.sleep(self.timeout)
                    elif out == turn_left:
                        ard.turn_left()
                        time.sleep(self.timeout)
                    elif out == turn_right:
                        ard.turn_right()
                        time.sleep(self.timeout)
                    elif out == turn_zero:
                        ard.turn_zero()
                        time.sleep(self.timeout)
        except:
            print("DEAD PROC")
            if self.q.empty():
                self.q.put("DEAD")
            
            
    def sender_to_q(self, info):
        """ @info - 'stop' or 'go' or 'turn_right' or 'turn_left' or 'turn_zero' """
        #print(self.q.empty())
        if self.q.empty():
            self.q.put(info)

                
    def reader_from_q(self):
         if self.q.empty() == False:
            return self.q.get()
         else:
            return None
                    

                
    def resurrection(self, last=None):
        """
        1 -  this function has one optional param, 
        which should be used for for resending last unmatched info.
        2 - the function should be used only inside operator "if" whith 
        condition - (Arduino_send.live_status == 'DEAD')""  
        """
        #print(666)
        self.killer()
        self.q = multiprocessing.Queue(maxsize=5)
        self.proc = multiprocessing.Process(target=self.sender_to_ar)
        self.proc.start()
        time.sleep(1)
        if (last != None):
            self.sender_to_q(last)
            
         
    def killer(self):
        self.proc.terminate()
            
########################################################################
        
        
