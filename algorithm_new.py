from Distance import Distance
import serial
import time
import string
import pynmea2
from mpu9250 import *
from module import *

POINTS = [(43.400081,39.964251), (43.400585,39.963003), (43.399175,39.963610), (43.398381,39.963590), (43.398788,39.964401), (43.399534,39.964645), (43.400143,39.965468)]  # list with tuples (structure: (latitude, longitude)
MISTAKE_LAT = 2                                                    # available mistake of the latitude
MISTAKE_LON = 2                                                    # available mistake of the longitude
MISTAKE_DEG = 2                                                    # available mistake of the degrees
delay = 3

########## Initialization ######################################################################################
compass = Compass()
###########################################################################################################
while True:
    weight = len(POINTS)
    if weight > 0:
        print('number of points - ', weight)
        flag = 0 # creating of the counter (number of the next point-target )

        while flag != weight:
            my_lat, my_lon = midl_cord(5, True)

            print('latitude - ', my_lat, 'longitude - ', my_lon, POINTS[flag])

            if ((my_lat - MISTAKE_LAT) <= POINTS[flag][0] <= (my_lat + MISTAKE_LAT)) and ((my_lon - MISTAKE_LON) <= POINTS[flag][1] <= (my_lon + MISTAKE_LON)):
                flag += 1   # if we are on the point-target
                print('finished points - ', flag)

            else:           # if we aren`t on the point-target
                RotateAngel = Distance(my_gps()[0], my_gps()[1], POINTS[flag][0], POINTS[flag][1]).angle()
                my_angel = compass.my_angel()
                while ((RotateAngel - MISTAKE_DEG) < my_angel < (RotateAngel + MISTAKE_DEG)):
                    my_angel = compass.my_angel()
                    print('my angel - ', my_angel, 'rotate angel - ', RotateAngel)
                    moving()
                    turn()

                turn_zero()
                time.sleep(delay)
                print("ending of turning")
    stopper()
    print("end")




