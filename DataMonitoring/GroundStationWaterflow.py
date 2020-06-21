import serial 
import time 
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt 
import numpy as np 
import threading
import termios, fcntl, sys, os
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

ser = serial.Serial("/dev/cu.usbmodem14101")
ser.flushInput() 

plot_window = 20
y_var = np.array(np.zeros([plot_window]))

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(y_var)


while True: 
	try:
		ser_bytes = ser.readline()
		print('collected new data')
		try: 
			decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
			print(decoded_bytes)
		except: 
			continue
		with open("test_data.csv", "a") as f:
			writer = csv.writer(f, delimiter = ",")
			writer.writerow([time.time(), decoded_bytes])
		y_var = np.append(y_var, decoded_bytes)
		y_var = y_var[1:plot_window + 1]
		c = sys.stdin.read(1)
		if c:
			print("Got character", repr(c))
			line.set_ydata(y_var)
			ax.relim()
			ax.autoscale_view()
			fig.canvas.draw() 
			fig.canvas.flush_events()
		else:
			continue
	except: 
		print("Keyboard Interrupt")
		break


def raw_input_with_timeout(prompt, timeout = 2.0):
	astring = None
	threading.Timer(timeout, raw_input_with_timeout).start()
	
	return astring


