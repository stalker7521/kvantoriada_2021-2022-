#!/usr/bin/python

from mpu9250 import *
import time

mpu = MPU9250()
mpu.initialize()

compas = AK8963()
compas.initialize()

# Set calibration data
mpu.gyro_offs =  {'y': -5, 'x': 158, 'z': -100}
mpu.accel_offs =  {'y': 102, 'x': -34, 'z': -364}

compas.calibration_matrix = [  [4.389680,-0.040792, -0.251706],
                                        [-0.040792,4.253841 , 0.083236],
                                        [-0.251706,0.083236 ,5.092105 ]]
compas.bias = [186.292456, 45.661290, -62.344200]

while True:
	gyro_data = mpu.get_gyro()
	accel_data = mpu.get_accel()
	compas_data = compas.get_calibrated()
	
	print ("GYROSCOPE: ", gyro_data)
	print ("ACCELEROMETER: ", accel_data)
	print ("TEMPERATURE: ",mpu.get_temp())
	print ("MAGNETOMETER: ", compas_data, "\n\n")

	time.sleep(1)
