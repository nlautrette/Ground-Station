import sys
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # number ### is interpreted as nrows ncols index
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class StatusGroup(QWidget):
    def __init__(self, name, *args, **kwargs):
        super(StatusGroup, self).__init__(*args, **kwargs)

        self.name = name
        layout = QGridLayout()

        self.open_btn = QPushButton("OPEN")
        self.open_btn.setFont(QFont("Helvetica Neue"))
        self.open_btn.clicked.connect(self.open_act)
        self.close_btn = QPushButton("CLOSE")
        self.close_btn.setFont(QFont("Helvetica Neue"))
        self.close_btn.clicked.connect(self.close_act)
        self.status = Status()

        layout.addWidget(self.open_btn,0,0)
        layout.addWidget(self.close_btn,1,0)
        layout.addWidget(self.status,0,1,2,1)

        self.setLayout(layout)
        self.setMaximumHeight(80)

    def open_act(self):
        if self.status.closed:
            print("Opening " + self.name)
            self.status.switch()

    def close_act(self):
        if not self.status.closed:
            print("Closing " + self.name)
            self.status.switch()

class Status(QWidget):
    def __init__(self, *args, **kwargs):
        super(Status, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        self.closed_txt = "<font color='White'>CLOSED</font>"
        self.open_txt = "  OPEN"
        self.color = 'red'
        self.closed = True
        self.set_color(self.color)


        layout = QVBoxLayout()
        self.l = QLabel(self.closed_txt)
        labelfont = QFont("Helvetica Neue", 14, QFont.Bold)
        labelfont.setLetterSpacing(QFont.PercentageSpacing, 105)
        self.l.setFont(labelfont)

        layout.addWidget(self.l, Qt.AlignCenter)

        self.setLayout(layout)

        self.setMaximumHeight(60)
        self.setMinimumWidth(90)

    def switch(self):
        if self.color == 'red':
            # Change to open (green)
            self.color = 'green'
            self.l.setText(self.open_txt)
            self.set_color("#60d936") # Light Green
            self.closed = False
            # TODO: OPENING ACTION
        elif self.color == 'green':
            # Change to closed (red)
            self.color = 'red'
            self.l.setText(self.closed_txt)
            self.set_color("#ee230c") # Bright Red
            self.closed = True
            # TODO: CLOSING ACTION

    def set_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        mainlayout = QGridLayout()

        # row 0

        title = QLabel("Waterflow Dashboard")
        titlefont = QFont("Lucida Grande",20, QFont.Bold)
        title.setFont(titlefont)

        mainlayout.addWidget(title,0,0,1,2)

        # Valves

        valves = ["Pressurant", "LOX GEMS", "Propane GEMS", "LOX 2-WAY",
        "Propane 2-WAY", "LOX 5-WAY", "Propane 5-WAY"]
        StatusGroups = {}
        for i,name in enumerate(valves):
            StatusGroups[name] = StatusGroup(name)

        valve_container = QWidget()
        valve_layout = QGridLayout()
        valve_layout.addWidget(QLabel("Pressurant"),0,1)
        valve_layout.addWidget(StatusGroups['Pressurant'],1,1)
        valve_layout.addWidget(QLabel("LOX"),2,1)
        valve_layout.addWidget(QLabel("Propane"),2,2)
        valve_layout.addWidget(QLabel("GEMS"),3,0)
        valve_layout.addWidget(StatusGroups['LOX GEMS'],3,1)
        valve_layout.addWidget(StatusGroups['Propane GEMS'],3,2)
        valve_layout.addWidget(QLabel("2-WAY"),4,0)
        valve_layout.addWidget(StatusGroups['LOX 2-WAY'],4,1)
        valve_layout.addWidget(StatusGroups['Propane 2-WAY'],4,2)
        valve_layout.addWidget(QLabel("5-WAY"),5,0)
        valve_layout.addWidget(StatusGroups['LOX 5-WAY'],5,1)
        valve_layout.addWidget(StatusGroups['Propane 5-WAY'],5,2)

        valve_container.setLayout(valve_layout)
        mainlayout.addWidget(valve_container,1,0)

        # Graphs

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        mainlayout.addWidget(sc,1,1,1,1)

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

app = QApplication(sys.argv)
w = MainWindow()
app.exec_()
