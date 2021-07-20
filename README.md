# kvantoriada_2021
***
## Helpfull links:
- [Gps modul (Neo 6M)](https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/)   
- [Magnetometer (MPU-6050, MPU-9250 the same)](https://blog.avislab.com/hmc5883l_ru/)  
***
## More information
- To work MPU-9250 without errors, you need to initialize both the accelerometer and the magnetometer.  
mpu = MPU9250()  
mpu.initialize()
mpu.gyro_offs = {'y': -5, 'x': 158, 'z': -100}
mpu.accel_offs = {'y': 102, 'x': -34, 'z': -364}
compas = AK8963()  
compas.initialize()
