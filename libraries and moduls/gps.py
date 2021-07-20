import serial
import time
import string
import pynmea2
from module import midl_cord

func = int(input())
########################################################################
if func == 1:	
	while True:
		tr = time.time()
		port="/dev/ttyAMA0"
		ser=serial.Serial(port, baudrate=9600, timeout=0.5)
		dataout = pynmea2.NMEAStreamReader()
		newdata=ser.readline()

		if newdata[0:6] == "$GPRMC":
			newmsg=pynmea2.parse(newdata)
			lat=newmsg.latitude
			lng=newmsg.longitude
			gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
			print(gps)
			print(time.time() - tr)
		else:
			print(None)
########################################################################
else:
	tr = time.time()
	lat, lon = 	midl_cord(10, True)
	print(time.time()-tr)
	print(lat, lon)
	
