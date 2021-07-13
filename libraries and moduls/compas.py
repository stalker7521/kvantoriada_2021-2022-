#!/usr/bin/python

from mpu9250 import *
import time

def compass_set():
    compas = AK8963()
    compas.initialize()
    compas.get_calibrated()
    return compas.heading()

while True:
	print (compass_set())
	#time.sleep(1)
