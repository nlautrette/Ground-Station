from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import time, traceback, sys, random, select


import serial
import serial.tools.list_ports


class SerialThread(QRunnable):
    '''
    Main Serial Thread
    '''

    running = True

    def __init__(self, canvas):
        super(SerialThread, self).__init__()
        self.signals = SerialSignals()

        # ---------- Display Config ---------------------------------

        self.canvas = canvas

        n_data = 400
        self.xdata = list(range(n_data))
        self.ydata = [0 for i in range(n_data)]#[random.randint(0, 10) for i in range(n_data)]

        #Initialize Plot
        plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'b')
        self._plot_ref = plot_refs[0]

        # ---------- Serial Config ----------------------------------

        self.numLowPressure = 1
        self.numHighPressure = 0


    @pyqtSlot()
    def run(self):
        '''
        Initialize the independent thread
        '''

        # while SerialThread.running:
        #     result = random.randint(0, 10)
        #     self.update_plot(result)
        #     time.sleep(0.01)


        NUMDATAPOINTS = 400

        print("Starting")

        chosenCom = ""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)
            if "Arduino" in p.description or "ACM" in p.description or "cu.usbmodem" in p[0]:
                chosenCom = p[0]
                print("Chosen COM: {}".format(p))
        print("Chosen COM {}".format(chosenCom))
        baudrate = 9600
        print("Baud Rate {}".format(baudrate))
        ser = serial.Serial(chosenCom, baudrate)
        ser.flushInput()

        display = True
        display_all = False
        repeat = 1

        # if args.file:
        #     filename = next_file_name(args.file)
        # else:
        #     filename = next_file_name("waterflow")
        # # filename = input("Which file should the data be written to?\n")
        # print("Writing data to: {}".format(filename))


        currLine = str(ser.readline())
        start = time.time()
        while ("low pressure sensors" not in currLine and "low pt" not in currLine):
            currLine = str(ser.readline())
            print(currLine);
            if time.time() - start > 1.5:
                start = time.time()
                print("looking for low pressure input")
        numLowSensors = self.numLowPressure
        byteNum = (str(numLowSensors) + "\r\n").encode('utf-8')
        print("write low sensor nums: {}".format(ser.write(byteNum)))

        currLine = str(ser.readline())
        start = time.time()
        while ("high pressure sensors" not in currLine):
            currLine = str(ser.readline())
            if time.time() - start > 1.5:
                start = time.time()
                print("looking for high pressure input")
        numHighSensors = self.numHighPressure
        byteNum = (str(numHighSensors)+"\r\n").encode('utf-8')
        print("write high sensor nums: {}".format(ser.write(byteNum)))

        sensors = numLowSensors + numHighSensors
        #sensors = int(input("How many sensors are connected?\n")) #set to how many sensors are connected
        print(ser.readline().decode("utf-8")) # There are x low PTs and x high PTs.
        headers = ser.read_until().decode("utf-8") # low1, low2, low3, high1.....
        headerList = headers.split(",")
        print(headerList)

        print("num sensors: {}".format(sensors))
        data = [[] for i in range(sensors)]
        toDisplay = [[] for i in range(sensors)]
        #
        # plt.ion()
        # fig, ax = plt.subplots(2, max(numLowSensors, numHighSensors))
        # if max(numLowSensors, numHighSensors) == 1:
        #     ax = np.reshape(ax, (-1, 1))
        # plt.show()
        # print(np.shape(ax))
        # plots = []
        #
        # for num in range(numLowSensors):
        #     ax[0,num].set_title(headerList[num])
        #     plot, = ax[0,num].plot(data[num])
        #     plots.append(plot)
        #
        # for num in range(numHighSensors):
        #     ax[1,num].set_title(headerList[num+numLowSensors])
        #     plot, = ax[1,num].plot(data[num+numLowSensors])
        #     plots.append(plot)
        #
        # with open(filename,"a") as f:
        #     headers = "time," + headers
        #     f.write(headers+"\n")
        plots = [self._plot_ref]

        ser.write("0\r\n".encode('utf-8'))


        def getLatestSerialInput():
            line = ser.readline()
            while(ser.in_waiting > 0):
                line = ser.readline()
            return line.decode('utf-8').strip()


        last_first_value = 0
        last_values = [0] * 5

        print("starting loop")
        while SerialThread.running:
            try:
                line = getLatestSerialInput()
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

                # with open(filename,"a") as f:
                #     toWrite = str(time.time())+"," + ",".join(values)+"\n"
                #     f.write(toWrite)
                    #writer = csv.writer(f,delimiter=",")
                    #writer.writerow(np.array([time.time(),values]).flatten())
                # print("Repeat: {}".format(repeat))

                for i in range(sensors):
                    data[i].append(float(values[i]))
                    print(len(data[i]))
                    toDisplay[i] = data[i][-NUMDATAPOINTS:]
                    print(len(toDisplay[i]))

                    if display_all:
                        plots[i].set_ydata(data[i])
                        plots[i].set_xdata(range(len(data[i])))
                    else:
                        plots[i].set_ydata(toDisplay[i])
                        plots[i].set_xdata(range(len(toDisplay[i])))
                    # else:
                    #     self.ydata = [0 for i in range(400-len(toDisplay[i]))].extend[toDisplay[i]]
                    #     plots[i].set_ydata(self.ydata)


                if display and repeat % 2 == 0:
                    for num in range(numLowSensors):
                        self.canvas.axes.relim()
                        self.canvas.axes.autoscale_view()

                    # for num in range(numHighSensors):
                    #     ax[1,num].relim()
                    #     ax[1,num].autoscale_view()

                    self.canvas.draw()
                    # self.canvas.flush_events()
                    repeat = 1
                else:
                    repeat += 1


                # data_in = select.select([sys.stdin], [], [], 0.1)[0]
                # if data_in:
                #     c = sys.stdin.readline().rstrip()
                #     if (c == "q"):
                #         print("Exiting")
                #         sys.exit(0)
                #     elif c == '0':
                #         display = not display
                #         print("toggling display")
                #     elif c == 't':
                #         display = True
                #     elif c == 'f':
                #         display = False
                #     elif c == 'd':
                #         display_all = not display_all
                #         print("toggle display all data")
                #     elif c == "c":
                #         data = [[] for i in range(sensors)]
                #         toDisplay = [[] for i in range(sensors)]
                #     else:
                #         print("You entered: %s" % c)


            except Exception as e:
                print("Crash: {}".format(e))
                ser.close()
                break

        ser.close()



        self.signals.finished.emit()

    @staticmethod
    def stop_thread():
        SerialThread.running = False

    def update_plot(self):

            self._plot_ref.set_ydata(self.ydata)
            self._plot_ref.set_xdata(self.xdata)

            self.canvas.draw()

class SerialSignals(QObject):
    '''
    Defines the signals available from a running worker thread

    Suported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    data = pyqtSignal(object)
