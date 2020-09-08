from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys
import random

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure




class SerialThread(QRunnable):
    '''
    Main Serial Thread
    '''

    running = True

    def __init__(self, canvas):
        super(SerialThread, self).__init__()
        self.signals = SerialSignals()

        self.canvas = canvas

        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]

        self._plot_ref = None
        self.update_plot()

    @pyqtSlot()
    def run(self):
        '''
        Initialize the independent thread
        '''

        while SerialThread.running:
            result = random.randint(0, 10)
            self.update_plot(result)
            time.sleep(0.01)

        self.signals.finished.emit()

    @staticmethod
    def stop_thread():
        SerialThread.running = False

    def update_plot(self, data=None):
        if data is None:
            self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        else:
            self.ydata = self.ydata[1:] + [data]

        if self._plot_ref is None:
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'b')
            self._plot_ref = plot_refs[0]
        else:
            self._plot_ref.set_ydata(self.ydata)

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
