from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *
import multiprocessing
import os


################-Compass-##############################################

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
        buff = self.my_angel()
        for i in range(num):
            ang = self.my_angel()
            if abs(buff - ang) < 90:
                buff = ang
                all_angels.append(ang)
            else:
                break
        if len(all_angels) < (int(num * 90 / 100)):
            return -1
        average = sum(all_angels)/len(all_angels)
        return average


class Compass_Send:
    def __init__(self):
        self.q = multiprocessing.Queue(maxsize=5)
        self.proc = multiprocessing.Process(target=self.getter)
        self.proc.start()
        # time.sleep(1)

    def getter(self):
        try:
            print(os.getpid(), ' - compass process')
            compass = Compass()
            while True:
                if self.q.empty() == False:
                    out = self.q.get()
                    if out == 'give':
                        info = compass.average_ang(2000)
                        if self.q.empty():
                            self.q.put(info)

        except:
            print("DEAD PROC - compass")
            if self.q.empty():
                self.q.put("DEAD")

    def sender_to_q(self, info):
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
        """
        # print(666)
        self.killer()
        self.q = multiprocessing.Queue(maxsize=5)
        self.proc = multiprocessing.Process(target=self.getter)
        self.proc.start()
        time.sleep(1)
        if (last != None):
            self.sender_to_q(last)

    def killer(self):
        self.proc.terminate()

#################-Tools-###############################################

def turn_chooser(myAngel, finishAngel):
    mod = abs(myAngel - finishAngel)
    if mod == 180:
        return 'turn_right'
    else:
        if ((270 <= myAngel < 360) and (0 < finishAngel <= 90)) or ((270 <= finishAngel <= 360) and (0 < myAngel <= 90)):
            if myAngel > finishAngel:
                return 'turn_right'
            else:
                return 'turn_left'
        elif ((315 <= myAngel <= 360) and (90 <= finishAngel <= 135)) or ((315 <= finishAngel <= 360) and (90 <= myAngel <= 135)):
            if myAngel > finishAngel:
                return 'turn_right'
            else:
                return 'turn_left'
        elif ((225 <= myAngel <= 270) and (0 <= finishAngel <= 45)) or ((225 <= finishAngel <= 270) and (0 <= myAngel <= 45)):
            if myAngel > finishAngel:
                return 'turn_right'
            else:
                return 'turn_left'
        else:
            if myAngel > finishAngel:
                return 'turn_left'
            else:
                return 'turn_right'

def delay(now_dist, max_delay=50, min_delay=6, dist=10, maxx = 0.5):
    """
    :param now_dis: information about distance between goal-point and your-point (meters)
    :param dist: global distance from which counting would be started (meters)
    :param min_delay: minimum checking per minute
    :param max_delay: maximum checking per minute
    :return: in how many seconds will the next check be
    """
    if 1 < now_dist < dist:
        tm_del = now_dist*(min_delay - max_delay)/dist + max_delay
        tm_del = round(60/tm_del)
        if tm_del == 0:
            tm_del = maxx
        return tm_del
    elif 1 >= now_dist:
        return maxx
    else:
        return min_delay


##################-GPS-################################################

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
        if newdata[0:6] == "$GPRMC":
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

################-Arduino-##############################################

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

    def turn_right(self):
        """arduino controlling function (for starting rotation)"""
        self.ser.write(self.TURN_RIGHT.encode('ascii'))
        
    def turn_left(self):
        """arduino controlling function (for starting rotation)"""
        self.ser.write(self.TURN_LEFT.encode('ascii'))

    def turn_zero(self):
        """arduino controlling function (for returning wheels at the default state)"""
        self.ser.write(self.TURN_ZERO.encode('ascii'))

        
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
            print(os.getpid(), ' - arduino process')
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
            print("DEAD PROC - arduino")
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
