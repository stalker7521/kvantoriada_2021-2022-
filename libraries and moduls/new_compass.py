#!/usr/bin/python
# -*- coding: utf-8 -*-
from mpu9250 import *

def hmc5883l_read():
	# MPU-6050
	mpu = MPU9250()
	mpu.initialize()

	compass = AK8963()
	compass.initialize()

	# Set calibration data
	mpu.gyro_offs = {'y': -5, 'x': 158, 'z': -100}
	mpu.accel_offs = {'y': 102, 'x': -34, 'z': -364}

	compass.calibration_matrix = [
		[1.869609, 0.038154, 0.012464],
		[0.038154, 1.660677, 0.042212],
		[0.012464, 0.042212, 1.750332]
	]
	compass.bias = [20.723669, 117.630557, -240.218174]

	accel_data = mpu.get_accel()
	x_rotation = mpu.get_x_rotation(accel_data)
	y_rotation = mpu.get_y_rotation(accel_data)

	last_time = time.time()
	alpha = 0.85

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

	rotation = 360 - compass.heading(x_rotation, y_rotation)
	time.sleep(0.01)

	return rotation
