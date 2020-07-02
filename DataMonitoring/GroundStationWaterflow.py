import serial
import serial.tools.list_ports
import time
import csv
import matplotlib
matplotlib.use("tkAgg")
import matplotlib.pyplot as plt
import numpy as np
import sys
import select
#import pandas as pd
#import termios, fcntl, sys, os
#fd = sys.stdin.fileno()

'''#UNBLOCKING INPUT
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
##############'''


print("Starting")

chosenCom = ""
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    if "Arduino" in p.description or "ACM" in p.description or "cu.usbmodem" in p[0]:
        chosenCom = p[0]
        print("Chosen COM: {}".format(p))
print("Chosen COM {}".format(chosenCom))
#ser = serial.Serial('/dev/tty/COM3')
ser = serial.Serial(chosenCom, 9600)
ser.flushInput()

# #for testing purposes
# ser = serial.Serial("/dev/cu.usbmodem14101")
# ser.flushInput()
# #######

plot_window = 1000
display = True


filename = input("Which file should the data be written to?\n")

currLine = str(ser.readline())
while ("low pressure sensors" not in currLine):
    time.sleep(500)
    currLine = str(ser.readline())
    print("looking for low pressure input")
numLowSensors = int(input(currLine+"\n"))
byteNum = (str(numLowSensors) + "\r\n").encode('utf-8')
# print(byteNum)
# print(int.from_bytes(byteNum, byteorder='big'))
print("write low sensor nums: {}".format(ser.write(byteNum)))

currLine = str(ser.readline())
while ("high pressure sensors" not in currLine):
    #time.sleep(500)
    currLine = str(ser.readline())
    print("looking for high pressure input")
numHighSensors = int(input(currLine+"\n"))
byteNum = (str(numHighSensors)+"\r\n").encode('utf-8')
#print(byteNum)
#print(int.from_bytes(byteNum, byteorder='big'))
print("write high sensor nums: {}".format(ser.write(byteNum)))

sensors = numLowSensors + numHighSensors
#sensors = int(input("How many sensors are connected?\n")) #set to how many sensors are connected
print(ser.readline().decode("utf-8")) # There are x low PTs and x high PTs.
headers = ser.read_until().decode("utf-8") # low1, low2, low3, high1.....
headerList = headers.split(",")

print("num sensors: {}".format(sensors))
data = [[] for i in range(sensors)]
print(data)
print("length of data: {}".format(len(data)))

plt.ion()
fig, ax = plt.subplots(2, max(numLowSensors, numHighSensors))
plt.show()
print(np.shape(ax))
plots = []

for num in range(numLowSensors):
    print(num)
    ax[0,num].set_title(headerList[num])
    plot, = ax[0,num].plot(data[num])
    plots.append(plot)

for num in range(numHighSensors):
    print(num)
    ax[1,num + numLowSensors].set_title(headerList[num+numLowSensors])
    plot, = ax[1,num + numLowSensors].plot(data[num+numLowSensors])
    plots.append(plot)

with open(filename,"a") as f:
    headers = "time," + headers
    f.write(headers+"\n")

ser.write("0\r\n".encode('utf-8'))

last_first_value = 0
last_values = [0] * 5

def process():
    print("Do something")

print("starting loop")
while True:
    #print("in loop")
    try:
        #print("in try")
        line = ser.readline().strip().decode('utf-8')
        values = line.strip().split(',')

        if values[0] == '':
            values[0] = str(last_first_value);
        if len(values) < sensors:
            print("not enough data, continuing")
            continue
        last_values = values
        values = [val.strip() for val in values]
        last_first_value = values[0]

        print("values: {}".format(values))
        #print("did some processing")

        with open(filename,"a") as f:
            toWrite = str(time.time())+"," + ",".join(values)+"\n"
            #print(toWrite)
            f.write(toWrite)
            #writer = csv.writer(f,delimiter=",")
            #writer.writerow(np.array([time.time(),values]).flatten())

        for i in range(sensors):
            #print("data: {}".format(data))
            #print("in sensor range {}".format(i))
            data[i].append(float(values[i]))
            #print("data[{}]: {}".format(i, data[i]))
            plots[i].set_ydata(data[i])
            plots[i].set_xdata(range(len(data[i])))
        # x.set_xlim(0, len(y_var))
        if display:
            #print("entered display")
            for num in range(numLowSensors):
                #print("low sensor num: {}".format(num))
                ax[0,num].relim()
                ax[0,num].autoscale_view()

            for num in range(numHighSensors):
                #print("high sensor num: {}".format(num))
                ax[1,num + numLowSensors].relim()
                ax[1,num + numLowSensors].autoscale_view()

            fig.canvas.draw()
            fig.canvas.flush_events()
            #plt.show()

        input = select.select([sys.stdin], [], [], 0.2)[0]
        if input:
            #print("inside if statement")
            c = sys.stdin.readline().rstrip()
            if (c == "q"):
                print("Exiting")
                sys.exit(0)
            elif c == '0':
                display = not display
                print("toggling display")
            elif c == 't':
                display = True
            elif c == 'f':
                display = False
            else:
                print("You entered: %s" % value)
        else:
            continue

        '''c = input("Enter one of the following characters (0, t, f): ")
        if c == '0':
            display = not display
            print("toggling display")
        elif c == 't':
            display = True
        elif c == 'f':
            display = False'''
=======
>>>>>>> Stashed changes

    except Exception as e:
        print("Crash: {}".format(e))
        ser.close()
        break



ser.close()
