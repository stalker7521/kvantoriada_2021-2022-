# TODO for tests (in sirius)

from module import *
import Distance
import time

cord = (1, 1)
flag = False
ang_m = 1
lat_lon_m = 0.001
compass = Compass()
while True:
    if flag == True:
        break
    lat, lon = midl_cord(4, True)  # 5 sec
    if ((lat - lat_lon_m) < cord[0] < (lat - lat_lon_m)) and ((lon - lat_lon_m) < cord[0] < (lon - lat_lon_m)):
    dist = Distance(lat, lon, cord[0], cord[1])
    angel = dist.angel()
    while ((angel - ang_m) < compass.my_angel() < (angel + ang_m)):
        print('крутись')
        print(compass.my_angel())
        time.sleep(1)             # 1 sec





# print('start')
# a = 0
# d = 3
# while not((14 - d)< a <(14 + d)):
#     time.sleep(1)
    # a += 1
    # print(a)
# print('end')