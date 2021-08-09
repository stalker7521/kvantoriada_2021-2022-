from mpu9250 import *
from module import Compass
import time

compas = Compass()
flag = int(input())
print('1 - colibration \n save info -2 ')
if flag == 1:
	compas.colibrating(10000)
	time.sleep(0.1)
elif flag == 2:
	f = open('compass_info.txt', 'w')
	while True:
		info = compas.my_angel()
		print (info)
		info = str(info) + '\n'
		f.write(info)
		time.sleep(0.1)
	f.close()
else:
	while True:
		print (compas.my_angel())
		time.sleep(0.1)
