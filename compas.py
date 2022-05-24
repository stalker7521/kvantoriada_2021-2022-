from module import Compass
import time

compas = Compass()
print('1 - colibration')
print('2 - info during 1sec')
print('3 - just info')
print('4 - average info')
flag = int(input())
print('do you want save info? [y/n]')
save = str(raw_input())


if flag == 1:
	compas.colibrating(1000)
	time.sleep(0.1)
	
elif flag == 2:
	if save == 'y':
		f = open('compass_info.txt', 'w')
	try:
		tm = time.time()
		while time.time() - tm <= 1:
			info = compas.my_angel()
			print(info)
			if save == 'y':
				info = str(info) + '\n'
				f.write(info)
			time.sleep(0.01)
	except:
		if save == 'y':
			f.close()
			
elif flag == 3:
	i = 0
	if save == 'y':
		f = open('compass_info.txt', 'w')
	try:
		while True:
			i += 1
			info = compas.my_angel()
			info = str(i) + ')' + str(info)
			print(info)
			if save == 'y':
				info += '\n'
				f.write(info)
			#time.sleep(0.1)
	except:
		if save == 'y':
			f.close()
			
elif flag == 4:
	i = 0
	print(1111111111)
	if save == 'y':
		f = open('compass_info.txt', 'w')
	try:
		while True:
			i += 1
			tm = time.time()
			info = compas.average_ang(600)
			tm1 = time.time() - tm
			info = str(i) + ')' + str(int(info)) + ' > time - ' + str(tm1)
			print(info)
			if save == 'y':
				info += '\n'
				f.write(info)
	except:
		if save == 'y':
			f.close()

elif flag == 5:
	all_info = []
	if save == 'y':
		f = open('compass_info.txt', 'w')
	try:
		tm = time.time()
		while time.time() - tm <= 1:
			info = compas.my_angel()
			all_info.append(info)
			print(info)
			if save == 'y':
				info = str(info) + '\n'
				f.write(info)
			#time.sleep(0.1)
		ans = sum(all_info)/len(all_info)
		if save == 'y':
				ans = 'average value - ' + str(ans) + '\n'
				f.write(ans)
	except:
		if save == 'y':
			f.close()
