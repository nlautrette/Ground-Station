import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit, QTextEdit,  QCheckBox, QWidget
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # number ### is interpreted as nrows ncols index
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        mainlayout = QGridLayout()

        # row 0

        title = QLabel("Waterflow Data Visualization")
        titlefont = QFont("Lucida Grande",20, QFont.Bold)
        title.setFont(titlefont)

        mainlayout.addWidget(title,0,0,1,2)

        # row 1

        # Create the relevant pushbottons
        b1 = QPushButton("Butt 1")
        b1.clicked.connect(self.act1)
        b2 = QPushButton("Butt 2")
        b2.clicked.connect(self.act2)
        b3 = QPushButton("Butt 3")
        b3.clicked.connect(self.act3)

        mainlayout.addWidget(b1,1,0)
        mainlayout.addWidget(b2,1,1)
        mainlayout.addWidget(b3,1,2)

        # row 2

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        mainlayout.addWidget(sc,2,0,1,3)

        # Add layout to a dummy QWidget, and set it as the Central Widget
        widget = QWidget()
        widget.setLayout(mainlayout)

        self.setCentralWidget(widget)

        self.show()

    def act1(self):
        print("Action 1")

    def act2(self):
        print("Action 2")

    def act3(self):
        print("Action 3")

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
