"""
void setup() {
Serial.begin(9600);
}

void loop() {
if (Serial.available()){
	String data = Serial.readStringUntil("\n");
	Serial.println("You: ") + data;
	}
}
"""
"""
if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.flush()
	while True:
		ser.write('3'.encode('ascii'))
		#line = ser.readline().decode('utf-8').rstrip()
		print(1)
		time.sleep(1)
"""
"""
print(os.getpid())

def g():
	while True:
		print(os.getpid())
		time.sleep(1)

g = multiprocessing.Process(target=g)
g.start()
g.terminate()
print('finish')


from module import Arduino
ser = Arduino(bot = 9600, port = '/dev/ttyACM0', timeout_1 = 1, dlin=2)
print("here")
time.sleep(1)
while True:
	ser.stopper()
	print(1)
	time.sleep(1)
"""
import time
import multiprocessing
import os
from module import *

ad = Arduino_send()
#time.sleep(1)
nan = 0
print(os.getpid())
while True:
	ad.sender_to_q("go")
	time.sleep(0.1)
	nan += 1
	print(nan)
	if ad.reader_from_q() == 'DEAD':
		print('here')
		ad.resurrection()


