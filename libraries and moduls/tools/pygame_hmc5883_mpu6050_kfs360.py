#!/usr/bin/python
# -*- coding: utf-8 -*-

from hmc5883 import *
from kfs360 import *
from mpu6050 import *

def hmc5883l_read():

	# MPU-6050
	mpu = MPU6050()
	mpu.initialize()

	# calibration data
	mpu.gyro_offs = {'x': -178, 'y': 259, 'z': -104}
	mpu.accel_offs =  {'y': -354, 'x': 389, 'z': -1482}

	# HMC5883L
	compass = hmc5883l()
	# calibration data
	compass.calibration_matrix = [  [1.259098, 0.013830, 0.039295],
			[0.01380, 1.245928, -0.018922],
			[0.039295, -0.018922, 1.360489]]
	compass.bias = [11.16, -43.55, -52.62]

	accel_data = mpu.get_accel()
	x_rotation = mpu.get_x_rotation(accel_data)
	y_rotation = mpu.get_y_rotation(accel_data)

	last_time = time.time()
	alpha = 0.95;

	# Simple Kalman Filter for -180 +180 degrees values
	# Q=2; R=15; F=1; H=1
	# Q - noise
	# R - measuring erro
	# F - dynamics of the system
	# H - 1
	Filter = KFS360(4.0, 15.0, 1.0, 1.0);

	while True:
		new_time = time.time()
		gyro_data = mpu.get_gyro()
		accel_data = mpu.get_accel()

		dt = new_time - last_time
		last_time = new_time
		gyro_angle_x = gyro_data['x']*dt + x_rotation
		if gyro_angle_x > 360:
			gyro_angle_x -= 360
		if gyro_angle_x < 0:
			gyro_angle_x = 360 + gyro_angle_x

		accel_angle_x = mpu.get_x_rotation(accel_data)

		if abs(gyro_angle_x - accel_angle_x) > 180:
			gyro_angle_x = accel_angle_x

		x_rotation = alpha*gyro_angle_x + (1.0 - alpha)*mpu.get_x_rotation(accel_data)

		gyro_angle_y = gyro_data['y']*dt + y_rotation
		y_rotation = alpha*gyro_angle_y + (1.0 - alpha)*mpu.get_y_rotation(accel_data)

		rotation_new = compass.heading(x_rotation, y_rotation)
		Filter.correct(rotation_new)
		rotation = 360 - Filter.State
		time.sleep(0.1)
		return rotation