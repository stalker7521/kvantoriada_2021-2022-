from Distance import Distance


POINTS = [(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
MISTAKE_LAT = 2
MISTAKE_LON = 2

def my_gps():
    cord = (10, 16)
    return cord


while True:
    weight = len(POINTS)
    if weight > 0:
        flag = -1
        while flag != weight:
            my_xy = my_gps()
            if ((my_xy[0] - MISTAKE_LAT) >= my_xy[0] <= (my_xy[0] + MISTAKE_LAT)) && ((my_xy[0] - MISTAKE_LON) >= my_xy[0] <= (my_xy[0] + MISTAKE_LON)):
                flag += 1
            else:
                """IN progress"""


