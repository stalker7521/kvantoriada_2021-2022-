# -*- encoding: utf-8 -*-
from Distance import Distance
from module import *

POINT = (56.84476, 60.59396) #lat, lon
FINISH = False
INIT = []
MISTAKE_LAT = 0.0001
MISTAKE_LON = 0.0001
MISTAKE_ROTATE = 2
flag = False
########## Initialization ######################################################################################

while flag == False:
    try:
        compass = Compass()
        arduino = Arduino_send()
        flag = True
    except:
        flag = False

###########################################################################################################
while FINISH == False:
    #arduino.sender_to_q('stop')
    cords = my_gps(False) # delay - 1с
    myLat = cords[0]
    myLon = cords[1]
    myAngel = compass.average_ang(600) # delay - 0.3c
    arduino.sender_to_q('go')
    
    print('go')
    print(myLat, ' - lat', str(myLon), ' - lon', str(myAngel), ' - angel')

    if ((myLat - MISTAKE_LAT) <= POINT[0] <= (myLat + MISTAKE_LAT)) and ((myLon - MISTAKE_LON) <= POINT[1] <= (myLon + MISTAKE_LON)):
        FINISH = True
    else:
        dist_class = Distance(myLat, myLon, POINT[0], POINT[1])
        length = dist_class.distance_main()
        finishAngel = dist_class.angle()
        direction = turn_chooser(myAngel, finishAngel)
        print(direction)
        flag = False
        while flag == 0:
            if (finishAngel - MISTAKE_ROTATE) < myAngel < (finishAngel + MISTAKE_ROTATE):
                flag = 1
            else:
                myAngel = compass.average_ang(600)  # delay - 0.3c
                arduino.sender_to_q(direction)
                
                print(finishAngel, ' = ', myAngel)
                print(direction)

        checker = delay(length)
        time.sleep(checker) #todo (go) <-------------------------------
        
arduino.sender_to_q('stop')

print('stop')
print('my cord - ', my_gps(False), ' point - ', POINT)

"""

ad.sender_to_q("go")
	print(nan)

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
"""



