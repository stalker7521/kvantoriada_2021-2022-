# -*- encoding: utf-8 -*-
from Distance import Distance
from module import *

POINTS = [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
]
GOAL = len(POINTS)
MISTAKE_LAT = 0.0001
MISTAKE_LON = 0.0001
MISTAKE_ROTATE = 2
counter = 0
flag = False
local_flag = False

########## Initialization ######################################################################################

while flag == False:
    try:
        compass = Compass()
        arduino = Arduino_send()
        flag = True
    except:
        flag = False

################################################################################################################
while counter != GOAL:
    local_point = counter
    pointLat = POINTS[counter][0]
    pointLon = POINTS[counter][1]
    flag = False
    while flag == False:
        cords = my_gps(False)  # delay - 1с
        myLat = cords[0]
        myLon = cords[1]
        myAngel = compass.average_ang(600)  # delay - 0.3c
        arduino.sender_to_q('go')
        # -------------------------------------------------------------------- #
        print('go')
        print(myLat, ' - lat', str(myLon), ' - lon', str(myAngel), ' - angel')
        # -------------------------------------------------------------------- #
        if ((myLat - MISTAKE_LAT) <= pointLat <= (myLat + MISTAKE_LAT)) and (
                (myLon - MISTAKE_LON) <= pointLon <= (myLon + MISTAKE_LON)):
            flag = True
            counter += 1
            # ----------------------------------------------------------------------------------------------------- #
            print('my cord - ', my_gps(False), ' point - ', (pointLat, pointLon), 'number of the point - ', counter)
            # ----------------------------------------------------------------------------------------------------- #
        else:
            dist_class = Distance(myLat, myLon, pointLat, pointLon)
            length = dist_class.distance_main()
            finishAngel = dist_class.angle()
            direction = turn_chooser(myAngel, finishAngel)
            # -------------------------------------------------------------------- #
            print(direction)
            # -------------------------------------------------------------------- #
            local_flag = False
            while local_flag == False:
                if (finishAngel - MISTAKE_ROTATE) < myAngel < (finishAngel + MISTAKE_ROTATE):
                    local_flag = True
                else:
                    myAngel = compass.average_ang(600)  # delay - 0.3c
                    arduino.sender_to_q(direction)
                    # -------------------------------------------------------- #
                    print(finishAngel, ' = ', myAngel)
                    print(direction)
                    # -------------------------------------------------------- #
            checker = delay(length)
            time.sleep(checker)  # todo (go) <-------------------------------

print('stop')
print('my cord - ', my_gps(False), ' point - ', (pointLat, pointLon), 'number of the point - ', counter)
