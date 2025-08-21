# IMPORT STATEMENTS
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sklearn.metrics import auc
import numpy as np
from matplotlib.figure import Figure
from sklearn.preprocessing import minmax_scale
import matplotlib.pyplot as plt



class SyncWindow(QWidget):
    delay_changed = pyqtSignal()
    start_time_changed = pyqtSignal()
    end_time_changed = pyqtSignal()
    def __init__(self, graph, max, delay, mts_time, fluke_time, temp, disp, mts_temp, synced_absolute, disp_title,
                 fluke_temp_title):
        super().__init__()
        self.setWindowTitle("Test Sync")

        # MAIN LAYOUT
        layout = QVBoxLayout()

        # GRAPHS SECTION
        self.graph_layout = QHBoxLayout()
        self.toolbar_layout = QHBoxLayout()
        self.synced_data = synced_absolute
        self.disp_title = disp_title
        self.fluke_temp_title = fluke_temp_title
        self.graph = graph
        self.canvas = FigureCanvas(self.graph)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.draw()
        # creating and plotting the mts fig (normalized temp and displacement)
        self.mts_temp_fig = Figure()
        ax = self.mts_temp_fig.add_subplot(111)
        times = mts_time
        temps = minmax_scale(mts_temp, feature_range=(0, 1))
        ax.plot(times, disp, label="Displacement")
        ax.plot(times, temps, label="Temperature")
        ax.set_xlabel("Time (s)")
        ax.set_title("MTS Temperature and Displacement")
        ax.legend(loc="best")

        self.mts_temp = temps
        self.mts_canvas = FigureCanvas(self.mts_temp_fig)
        self.mts_canvas.draw()
        self.mts_toolbar = NavigationToolbar(self.mts_canvas, self)

        self.graph_layout.addWidget(self.canvas)
        self.graph_layout.addWidget(self.mts_canvas)
        self.toolbar_layout.addWidget(self.toolbar)
        self.toolbar_layout.addWidget(self.mts_toolbar)

        layout.addLayout(self.graph_layout)
        layout.addLayout(self.toolbar_layout)

        # INITIAL CONDITIONS
        self.delay = delay
        self.delay2 = 0
        self.mts_time = mts_time
        self.fluke_time = fluke_time
        self.temp = temp
        self.disp = disp


        # FONTS
        font = QFont()
        font.setPointSize(10)
        bold_font = QFont()
        bold_font.setBold(True)
        bold_font.setPointSize(10)


        # DELAY SECTION
        self.delay_layout = QHBoxLayout()
        instructions = QLabel()
        instructions.setFont(font)
        instructions.setText("Drag slider to adjust delay or enter a value in the box:")
        horizontal_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer3= QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer4 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        instructions.setMaximumHeight(50)
        self.delay_layout.addItem(horizontal_spacer)
        self.delay_layout.addWidget(instructions)
        self.delay_slider = QSlider(Qt.Horizontal)
        self.delay_slider.setMinimum(-5000)
        self.delay_slider.setMaximum(5000)
        self.delay_slider.setValue(int(self.delay))
        self.delay_edit = QLineEdit(self)
        self.delay_edit.setMaximumWidth(75)
        self.delay_edit.setText(str(self.delay))
        self.delay_layout.addWidget(self.delay_slider)
        self.delay_layout.addWidget(self.delay_edit)
        self.delay_layout.addItem(horizontal_spacer2)
        self.check_button = QPushButton(self)
        self.check_button.setText("Check")
        self.check_button.setFont(bold_font)
        self.check_button.setMaximumWidth(50)
        self.delay_layout.insertWidget(4, self.check_button)
        self.abs_time_switch = QCheckBox(self)
        self.abs_time_switch.setText("Absolute Time")
        self.delay_layout.addWidget(self.abs_time_switch)


        # START/END TIME SECTION
        self.times_layout = QHBoxLayout()
        start_label = QLabel()
        start_label.setText("Start Time:")
        start_label.setFont(font)
        start_label.setMaximumHeight(40)
        self.start_edit = QLineEdit(self)
        self.start_edit.setMaximumWidth(75)
        end_label = QLabel()
        end_label.setFont(font)
        end_label.setText("End Time:")
        self.end_edit = QLineEdit(self)
        self.end_edit.setMaximumWidth(75)
        self.test_button = QPushButton(self)
        self.test_button.setText("Test")
        self.test_button.setFont(bold_font)
        min_intersect_label = QLabel()
        min_intersect_label.setFont(font)
        min_intersect_label.setText("Minimum distance between intersections:")
        self.min_intersect_edit = QLineEdit(self)
        self.min_intersect_edit.setMaximumWidth(75)
        self.times_layout.addItem(horizontal_spacer3)
        self.times_layout.addWidget(start_label)
        self.times_layout.addWidget(self.start_edit)
        self.times_layout.addWidget(end_label)
        self.times_layout.addWidget(self.end_edit)
        self.times_layout.addWidget(min_intersect_label)
        self.times_layout.addWidget(self.min_intersect_edit)
        self.times_layout.addWidget(self.test_button)
        self.times_layout.addItem(horizontal_spacer4)
        self.start_time = 0
        self.end_time = 0
        self.intersect_tolerance = 0

        # AREA SECTION
        self.area_label = QLabel(self)
        self.area_label.setText("Calculated Area Between Curves:")
        self.area_label.setFont(bold_font)
        self.area_label.setMaximumHeight(40)
        self.area_label.setAlignment(Qt.AlignCenter)

        # TEMPORARY MTS TEMP DISP TROUUBLESHOOTING
        horizontal_spacer5 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer6 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer7 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer8 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer9 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer10 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer11 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        horizontal_spacer12 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.delay_layout2 = QHBoxLayout()
        self.times_layout2 = QHBoxLayout()
        mts_delay = QLabel()
        mts_delay.setText("Delay:")
        mts_delay.setFont(font)
        mts_delay.setMaximumHeight(40)
        self.mts_delay = QLineEdit(self)
        self.mts_delay.setMaximumWidth(75)
        self.mts_check_button = QPushButton(self)
        self.mts_check_button.setFont(bold_font)
        self.mts_check_button.setText("Check")
        self.mts_check_button.setMaximumWidth(100)
        self.delay_layout2.addItem(horizontal_spacer5)
        self.delay_layout2.addWidget(mts_delay)
        self.delay_layout2.addWidget(self.mts_delay)
        self.delay_layout2.addWidget(self.mts_check_button)
        self.delay_layout2.addItem(horizontal_spacer6)
        mts_start_label = QLabel()
        mts_start_label.setText("Start Time:")
        mts_start_label.setFont(font)
        mts_start_label.setMaximumHeight(40)
        self.mts_start = QLineEdit(self)
        self.mts_start.setMaximumWidth(75)
        mts_end_label = QLabel()
        mts_end_label.setFont(font)
        mts_end_label.setText("End Time:")
        self.mts_end = QLineEdit(self)
        self.mts_end.setMaximumWidth(75)
        mts_min_intersect_label = QLabel()
        mts_min_intersect_label.setFont(font)
        mts_min_intersect_label.setText("Minimum distance between intersections:")
        self.mts_min_intersect = QLineEdit(self)
        self.mts_min_intersect.setMaximumWidth(75)
        self.mts_test_button = QPushButton(self)
        self.mts_test_button.setText("Test")
        self.mts_test_button.setFont(bold_font)
        self.times_layout2.addItem(horizontal_spacer10)
        self.times_layout2.addWidget(mts_start_label)
        self.times_layout2.addWidget(self.mts_start)
        self.times_layout2.addWidget(mts_end_label)
        self.times_layout2.addWidget(self.mts_end)
        self.times_layout2.addWidget(mts_min_intersect_label)
        self.times_layout2.addWidget(self.mts_min_intersect)
        self.times_layout2.addWidget(self.mts_test_button)
        self.times_layout2.addItem(horizontal_spacer9)
        self.area2 = QLabel(self)
        self.area2.setText("Calculated Area Between Curves: ")
        self.area2.setAlignment(Qt.AlignCenter)
        self.area2.setFont(bold_font)
        self.area2.setMaximumHeight(40)
        self.plot_delay_layout = QHBoxLayout()
        delay_plotter_title = QLabel()
        delay_plotter_title.setMaximumHeight(40)
        delay_plotter_title.setFont(bold_font)
        delay_plotter_title.setText('Plot Delay vs. Area')
        delay_plotter_title.setAlignment(Qt.AlignCenter)
        delay_initial_label = QLabel()
        delay_initial_label.setFont(font)
        delay_initial_label.setMaximumHeight(40)
        delay_initial_label.setText("Initial Delay:")
        self.range_initial = QLineEdit(self)
        self.range_initial.setMaximumWidth(75)
        delay_final_label = QLabel()
        delay_final_label.setFont(font)
        delay_final_label.setMaximumHeight(40)
        delay_final_label.setText("Final Delay:")
        self.range_final = QLineEdit(self)
        self.range_final.setMaximumWidth(75)
        delay_interval_label = QLabel()
        delay_interval_label.setFont(font)
        delay_interval_label.setMaximumHeight(40)
        delay_interval_label.setText("Delay Interval:")
        self.delay_interval = QLineEdit(self)
        self.delay_interval.setMaximumWidth(75)
        self.plot_button = QPushButton(self)
        self.plot_button.setText("Plot")
        self.plot_button.setFont(bold_font)
        self.plot_delay_layout.addItem(horizontal_spacer7)
        self.plot_delay_layout.addWidget(delay_initial_label)
        self.plot_delay_layout.addWidget(self.range_initial)
        self.plot_delay_layout.addWidget(delay_final_label)
        self.plot_delay_layout.addWidget(self.range_final)
        self.plot_delay_layout.addWidget(delay_interval_label)
        self.plot_delay_layout.addWidget(self.delay_interval)
        self.plot_delay_layout.addWidget(self.plot_button)
        self.plot_delay_layout.addItem(horizontal_spacer8)

        # TEMPORARY GROUPING FOR TROUBLESHOOTING
        self.fluke_disp_calcs = QVBoxLayout()
        self.fluke_disp_calcs.addLayout(self.delay_layout)
        self.fluke_disp_calcs.addLayout(self.times_layout)
        self.fluke_disp_calcs.addWidget(self.area_label)
        self.mts_disp_calcs = QVBoxLayout()
        self.mts_disp_calcs.addLayout(self.delay_layout2)
        self.mts_disp_calcs.addLayout(self.times_layout2)
        self.mts_disp_calcs.addWidget(self.area2)
        self.mts_disp_calcs.addWidget(delay_plotter_title)
        self.mts_disp_calcs.addLayout(self.plot_delay_layout)
        self.all_calcs = QHBoxLayout()
        self.all_calcs.addLayout(self.fluke_disp_calcs)
        self.all_calcs.addLayout(self.mts_disp_calcs)


        # CORRECT LAYOUT (commented out stuff)
        # layout.addLayout(self.delay_layout)
        # layout.addLayout(self.times_layout)
        # layout.addWidget(self.area_label)
        layout.addLayout(self.all_calcs)
        self.setLayout(layout)

        # SIGNALS
        self.delay_slider.valueChanged.connect(self.sliderMove)
        self.delay_edit.editingFinished.connect(self.delayChange)
        self.check_button.clicked.connect(self.changeGraph)
        self.start_edit.editingFinished.connect(self.getStartTime)
        self.end_edit.editingFinished.connect(self.getEndTime)
        self.min_intersect_edit.editingFinished.connect(self.getIntersectDistanceTolerance)
        self.test_button.clicked.connect(self.calcArea)
        self.abs_time_switch.stateChanged.connect(self.graphToAbsolute)
        # self.test_button.clicked.connect(self.plotTimes)
        #TEMPORARY SIGNALS
        self.mts_delay.editingFinished.connect(self.delayChange2)
        self.mts_check_button.clicked.connect(self.changeGraph2)
        self.mts_test_button.clicked.connect(self.calcArea2)
        self.plot_button.clicked.connect(self.plotDelayArea)


    def sliderMove(self):
        val = self.delay_slider.value()
        self.delay_edit.setText(str(val))
        self.delay = val

    def delayChange(self):
        val = float(self.delay_edit.text())
        self.delay_slider.setValue(val)
        self.delay = val


    def changeGraph(self):
        self.graph.clear()
        ax = self.graph.add_subplot(111)

        mts_time = [x - self.delay for x in self.mts_time]

        ax.plot(mts_time, self.disp, label="Displacement")
        ax.plot(self.fluke_time, self.temp, label="Temperature")
        ax.set_title("Fluke Temperature and Displacement")
        ax.set_xlabel("Time (s)")
        ax.legend(loc="best")

        self.canvas.draw()

        self.delay_changed.emit()


    def graphToAbsolute(self):
        self.graph.clear()
        if self.abs_time_switch.isChecked():
            ax = self.graph.add_subplot(111)
            time = self.synced_data.index.to_numpy()
            disp = self.synced_data[self.disp_title].tolist()
            disp = minmax_scale(disp, feature_range=(0, 1))
            temps = self.synced_data[self.fluke_temp_title].tolist()
            temps = minmax_scale(temps, feature_range=(0, 1))
            ax.plot(time, disp, label='Displacement')
            ax.plot(time, temps, label='Temperature')
            ax.set_title("Fluke Temperature and Displacement")
            ax.set_xlabel("Time (s)")
            ax.legend(loc="best")

            self.canvas.draw()
        else:
            ax = self.graph.add_subplot(111)

            mts_time = [x - self.delay for x in self.mts_time]

            ax.plot(mts_time, self.disp, label="Displacement")
            ax.plot(self.fluke_time, self.temp, label="Temperature")
            ax.set_title("Fluke Temperature and Displacement")
            ax.set_xlabel("Time (s)")
            ax.legend(loc="best")

            self.canvas.draw()

    # TEMPORARY FOR TROUBLESHOOTING
    def changeGraph2(self):
        mts_time = [x - self.delay2 for x in self.mts_time]
        self.mts_temp_fig.clear()
        ax1 = self.mts_temp_fig.add_subplot(111)
        # temp = np.array([self.mts_temp, np.zeros(len(self.mts_temp))])
        # temp = normalize(temp)[0]
        temp = minmax_scale(self.mts_temp, feature_range=(0, 1))
        ax1.plot(mts_time, self.disp, label="Displacement")
        ax1.plot(self.mts_time, temp, label="Temperature")
        ax1.legend(loc="best")
        ax1.set_title("MTS Temperature and Displacement")
        ax1.set_xlabel("Time (s)")

        self.mts_canvas.draw()

    # TEMPORARY FOR TROUBLESHOOTING
    def delayChange2(self):
        self.delay2 = float(self.mts_delay.text())

    def getDelay(self):
        return self.delay


    def getStartTime(self):
        self.start_time = float(self.start_edit.text())


    def returnEndTime(self):
        return self.end_time


    def returnStartTime(self):
        return self.start_time


    def getEndTime(self):
        self.end_time = float(self.end_edit.text())


    def plotTimes(self):
        ax = self.graph.axes[0]
        if len(ax.lines) > 2:
            ax.lines[3].remove()
            ax.lines[2].remove()
        # x_min = min(self.mts_time) - self.delay
        # x_max = max(self.mts_time) - self.delay
        # ax.set_xlim([x_min, x_max])
        start_line = ax.axvline(x=self.start_time, color="red", ls="--")
        end_line = ax.axvline(x=self.end_time, color="red", ls="--")

        self.canvas.draw()


    def getIntersectDistanceTolerance(self):
        self.intersect_tolerance = float(self.min_intersect_edit.text())


    def calcArea(self):
        self.start_time_changed.emit()
        self.end_time_changed.emit()

        # finding points within interval
        mts_time = np.array([x - self.delay for x in self.mts_time], dtype=float)
        fluke_time = np.array(self.fluke_time, dtype=float)

        start_ind_mts = np.searchsorted(mts_time, self.start_time)
        if abs(mts_time[start_ind_mts] - float(self.start_time)) > abs(mts_time[start_ind_mts - 1] - float(self.start_time)):
            start_ind_mts = start_ind_mts - 1
        end_ind_mts = np.searchsorted(mts_time, self.end_time)
        if abs(mts_time[end_ind_mts] - float(self.end_time)) > abs(mts_time[end_ind_mts - 1] - float(self.end_time)):
            end_ind_mts = end_ind_mts - 1


        start_ind_fluke = np.searchsorted(fluke_time, self.start_time)
        if abs(fluke_time[start_ind_fluke] - float(self.start_time)) > abs(fluke_time[start_ind_fluke - 1] - float(self.start_time)):
            start_ind_fluke = start_ind_fluke - 1
        end_ind_fluke = np.searchsorted(fluke_time, self.end_time)
        if abs(fluke_time[end_ind_fluke] - float(self.end_time)) > abs(fluke_time[end_ind_fluke - 1] - float(self.end_time)):
            end_ind_fluke = end_ind_fluke - 1

        mts_time = mts_time[start_ind_mts: end_ind_mts + 1]
        disp = np.array(self.disp[start_ind_mts: end_ind_mts + 1], dtype=float)
        fluke_time = fluke_time[start_ind_fluke: end_ind_fluke + 1]
        temp = np.array(self.temp[start_ind_fluke: end_ind_fluke + 1], dtype=float)

        # finding intersection points
        longer_indices = [0]
        shorter_indices = []
        time_tol = 5
        y_tol = 0.01
        index_sep_tol = self.intersect_tolerance
        if (len(temp) > len(disp)):
            longer_arr = temp
            longer_time = fluke_time
            shorter_arr = disp
            shorter_time = mts_time
        else:
            longer_arr = disp
            longer_time = mts_time
            shorter_arr = temp
            shorter_time = fluke_time

        while (max(longer_indices) - min(longer_indices) < index_sep_tol):
            longer_indices.clear()
            shorter_indices.clear()
            for i in range(max(len(temp), len(disp))):
                for j in range(min(len(temp), len(disp))):
                    if abs(longer_arr[i] - shorter_arr[j]) <= y_tol and abs(longer_time[i] - shorter_time[j]) <= time_tol:
                        longer_indices.append(i)
                        if j not in shorter_indices:
                            shorter_indices.append(j)
            y_tol += 0.005
            if (len(longer_indices) == 0):
                longer_indices = [0]

        # print(longer_indices)
        # print(shorter_indices)
        # for ind in longer_indices:
        #     print("{}: {}".format(longer_time[ind], longer_arr[ind]))
        # print("BREAK")
        # for id in shorter_indices:
        #     print("{}: {}".format(shorter_time[id], shorter_arr[id]))


        # new intervals between intersection points
        if (len(longer_arr) == len(temp)):
            temp_indices = longer_indices
            disp_indices = shorter_indices
        else:
            temp_indices = shorter_indices
            disp_indices = longer_indices
        mts_time = mts_time[min(disp_indices):max(disp_indices) + 1]
        disp = disp[min(disp_indices):max(disp_indices) + 1]
        fluke_time = fluke_time[min(temp_indices):max(temp_indices) + 1]
        temp = temp[min(temp_indices):max(temp_indices) + 1]

        # calculating area
        area_mts = auc(mts_time, disp)
        area_fluke = auc(fluke_time, temp)

        area_between_curves = abs(area_mts - area_fluke)

        self.area_label.setText("Intersections detected at times: {}s and {}s; Calculated Area: {:.2f}".format(min(mts_time), max(mts_time), area_between_curves))

    # TEMPORARY FOR TROUBLESHOOTING
    def calcArea2(self):
        start = float(self.mts_start.text())
        end = float(self.mts_end.text())
        index_sep_tol = float(self.mts_min_intersect.text())

        # finding points within interval
        disp_time = np.array([x - self.delay2 for x in self.mts_time], dtype=float)
        temp_time = np.array(self.mts_time, dtype=float)

        start_ind_disp = np.searchsorted(disp_time, start)
        if abs(disp_time[start_ind_disp] - float(start)) > abs(
                disp_time[start_ind_disp - 1] - float(start)):
            start_ind_disp = start_ind_disp - 1
        end_ind_disp = np.searchsorted(disp_time, end)
        if abs(disp_time[end_ind_disp] - float(end)) > abs(disp_time[end_ind_disp - 1] - float(end)):
            end_ind_disp = end_ind_disp - 1

        start_ind_temp = np.searchsorted(temp_time, start)
        if abs(temp_time[start_ind_temp] - float(start)) > abs(
                temp_time[start_ind_temp - 1] - float(start)):
            start_ind_temp = start_ind_temp - 1
        end_ind_temp = np.searchsorted(temp_time, end)
        if abs(temp_time[end_ind_temp] - float(end)) > abs(
                temp_time[end_ind_temp - 1] - float(end)):
            end_ind_temp = end_ind_temp - 1

        disp_time = disp_time[start_ind_disp: end_ind_disp + 1]
        disp = np.array(self.disp[start_ind_disp: end_ind_disp + 1], dtype=float)
        temp_time = temp_time[start_ind_temp: end_ind_temp + 1]
        temp = np.array(self.mts_temp[start_ind_temp: end_ind_temp + 1], dtype=float)

        # finding intersection points
        longer_indices = [0]
        shorter_indices = []
        time_tol = 25
        y_tol = 0.01
        if (len(temp) > len(disp)):
            longer_arr = temp
            longer_time = temp_time
            shorter_arr = disp
            shorter_time = disp_time
        else:
            longer_arr = disp
            longer_time = disp_time
            shorter_arr = temp
            shorter_time = temp_time

        while (max(longer_indices) - min(longer_indices) < index_sep_tol):
            longer_indices.clear()
            shorter_indices.clear()
            for i in range(max(len(temp), len(disp))):
                for j in range(min(len(temp), len(disp))):
                    if abs(longer_arr[i] - shorter_arr[j]) <= y_tol and abs(longer_time[i] - shorter_time[j]) <= time_tol:
                        longer_indices.append(i)
                        if j not in shorter_indices:
                            shorter_indices.append(j)
            y_tol += 0.005
            if len(longer_indices) == 0:
                longer_indices = [0]

        for ind in longer_indices:
            print("{}: {}".format(longer_time[ind], longer_arr[ind]))
        print("BREAK")
        for id in shorter_indices:
            print("{}: {}".format(shorter_time[id], shorter_arr[id]))
        print(y_tol)

        # new intervals between intersection points
        if (len(longer_arr) == len(temp)):
            temp_indices = longer_indices
            disp_indices = shorter_indices
        else:
            temp_indices = shorter_indices
            disp_indices = longer_indices
        disp_time = disp_time[min(disp_indices):max(disp_indices) + 1]
        disp = disp[min(disp_indices):max(disp_indices) + 1]
        temp_time = temp_time[min(temp_indices):max(temp_indices) + 1]
        temp = temp[min(temp_indices):max(temp_indices) + 1]

        # calculating area
        area_mts = auc(disp_time, disp)
        area_fluke = auc(temp_time, temp)

        area_between_curves = abs(area_mts - area_fluke)

        self.area2.setText("Intersections detected at {}s and {}s; Calculated Area: {:.2f}".format(min(disp_time), max(disp_time), area_between_curves))


    def areaTester(self, start, end, index_sep_tol, delay):
        # finding points within interval
        disp_time = np.array([x - delay for x in self.mts_time], dtype=float)
        temp_time = np.array(self.mts_time, dtype=float)

        start_ind_disp = np.searchsorted(disp_time, start)
        if abs(disp_time[start_ind_disp] - float(start)) > abs(
                disp_time[start_ind_disp - 1] - float(start)):
            start_ind_disp = start_ind_disp - 1
        end_ind_disp = np.searchsorted(disp_time, end)
        # if abs(disp_time[end_ind_disp] - float(end)) > abs(disp_time[end_ind_disp - 1] - float(end)):
        #     end_ind_disp = end_ind_disp - 1

        start_ind_temp = np.searchsorted(temp_time, start)
        if abs(temp_time[start_ind_temp] - float(start)) > abs(
                temp_time[start_ind_temp - 1] - float(start)):
            start_ind_temp = start_ind_temp - 1
        end_ind_temp = np.searchsorted(temp_time, end)
        if abs(temp_time[end_ind_temp] - float(end)) > abs(
                temp_time[end_ind_temp - 1] - float(end)):
            end_ind_temp = end_ind_temp - 1

        disp_time = disp_time[start_ind_disp: end_ind_disp + 1]
        disp = np.array(self.disp[start_ind_disp: end_ind_disp + 1], dtype=float)
        temp_time = temp_time[start_ind_temp: end_ind_temp + 1]
        temp = np.array(self.mts_temp[start_ind_temp: end_ind_temp + 1], dtype=float)

        # finding intersection points
        longer_indices = [0]
        shorter_indices = []
        time_tol = 25
        y_tol = 0.01
        if (len(temp) > len(disp)):
            longer_arr = temp
            longer_time = temp_time
            shorter_arr = disp
            shorter_time = disp_time
        else:
            longer_arr = disp
            longer_time = disp_time
            shorter_arr = temp
            shorter_time = temp_time

        while (max(longer_indices) - min(longer_indices) < index_sep_tol):
            longer_indices.clear()
            shorter_indices.clear()
            for i in range(max(len(temp), len(disp))):
                for j in range(min(len(temp), len(disp))):
                    if abs(longer_arr[i] - shorter_arr[j]) <= y_tol and abs(longer_time[i] - shorter_time[j]) <= time_tol:
                        longer_indices.append(i)
                        if j not in shorter_indices:
                            shorter_indices.append(j)
            y_tol += 0.005
            if y_tol >= 0.5:
                time_tol *= 2
                y_tol = 0.01
            if len(longer_indices) == 0:
                longer_indices = [0]

        # new intervals between intersection points
        if (len(longer_arr) == len(temp)):
            temp_indices = longer_indices
            disp_indices = shorter_indices
        else:
            temp_indices = shorter_indices
            disp_indices = longer_indices
        disp_time = disp_time[min(disp_indices):max(disp_indices) + 1]
        disp = disp[min(disp_indices):max(disp_indices) + 1]
        temp_time = temp_time[min(temp_indices):max(temp_indices) + 1]
        temp = temp[min(temp_indices):max(temp_indices) + 1]

        # calculating area
        area_mts = auc(disp_time, disp)
        area_fluke = auc(temp_time, temp)

        area_between_curves = abs(area_mts - area_fluke)

        return area_between_curves


    def plotDelayArea(self):
        initial = int(self.range_initial.text())
        final = int(self.range_final.text())
        interval = int(self.delay_interval.text())

        start = float(self.mts_start.text())
        end = float(self.mts_end.text())
        min_dist = float(self.mts_min_intersect.text())

        delays = [x for x in range(initial, final + 1, interval)]
        areas = []

        for i in range(initial, final + 1, interval):
            areas.append(self.areaTester(start, end, min_dist, i))

        plt.plot(delays, areas)
        plt.show()

