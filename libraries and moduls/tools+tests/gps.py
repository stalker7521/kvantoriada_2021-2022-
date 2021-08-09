import serial
import time
import string
import pynmea2
from module import midl_cord

func = int(input())
########################################################################
if func == 1:	
	with open('gps_cord.txt', 'w+') as f:
		while True:
			tr = time.time()
			port="/dev/ttyAMA0"
			ser=serial.Serial(port, baudrate=9600, timeout=0.5)
			dataout = pynmea2.NMEAStreamReader()
			newdata=ser.readline()
			#print(newdata)
			if newdata[0:6] == "$GPRMC":
				newmsg=pynmea2.parse(newdata)
				lat=newmsg.latitude
				lng=newmsg.longitude
				gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng) + '\n'
				print(gps)
				t = str(time.time() - tr) + '\n'
				f.write(gps)
				f.write(t)
			else:
				#h = 'no' + '\n'
				#d = 'nooo' + '\n'
				#f.write(h)
				#f.write(d)
				print(1)
########################################################################
else:
    with open('gps_cord.txt', 'w+') as f: 
	tr = time.time()
	lat, lon = midl_cord(3, True)
	print(time.time()-tr)
	print(lat, lon)
	#f.write([lat, lon])

