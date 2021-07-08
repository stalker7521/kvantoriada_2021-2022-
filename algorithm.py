from Distance import Distance
import time as tm

POINTS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]  # list with tuples (structure: (latitude, longitude)
MISTAKE_LAT = 2                                                    # available mistake of the latitude
MISTAKE_LON = 2                                                    # available mistake of the longitude

#------RaspberryPi commands--------------------------------------------------------------------------------------------
def my_gps():
    """function with GPS (getting GPS coordinate from module)"""
    cord = (10, 16)
    return cord


def my_angel():
    """function with magnetometer (getting the angel from module)"""
    angel = 45
    return angel

#------Arduino commands------------------------------------------------------------------------------------------------
def stopper():
    """arduino controlling function (for stop motion)"""
    pass


def moving():
    """arduino controlling function (for start motion)"""
    pass


def turn():
    """arduino controlling function (for starting rotation)"""
    pass


def turn_zero():
    """arduino controlling function (for returning wheels at the default state)"""
    pass

#---------------------------------------------------------------------------------------------------------------------
while True:
    weight = len(POINTS)
    if weight > 0:
        flag = -1   # creating of the counter (number of the next point-target )
        while flag != weight:
            my_xy = my_gps()
            if ((my_xy[0] - MISTAKE_LAT) >= my_xy[0] <= (my_xy[0] + MISTAKE_LAT)) and ((my_xy[0] - MISTAKE_LON) >= my_xy[0] <= (my_xy[0] + MISTAKE_LON)):
                flag += 1   # if we are on the point-target
            else:           # if we aren`t on the point-target
                RotateAngel = Distance(my_gps()[0], my_gps()[1], POINTS[flag][0], POINTS[flag][1]).angle()
                while RotateAngel != my_angel():
                    moving()
                    turn()
                turn_zero()
        tm.sleep(1)         # time of delay
        stopper()




