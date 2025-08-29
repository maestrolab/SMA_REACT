# IMPORT STATEMENTS
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QFileDialog, QComboBox, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from sklearn.preprocessing import minmax_scale
from PyQt5.QtCore import pyqtSignal
import datetime
from collections import Counter
import cgitb

import pandas as pd
import numpy as np

from src.preprocessor.data_reader import reader
from src.preprocessor.sync_window import SyncWindow

cgitb.enable(format="text")



class TroubleshootWindow(QWidget):
    delay_updated = pyqtSignal()
    start_time_updated = pyqtSignal()
    end_time_updated = pyqtSignal()
    def __init__(self):
        super().__init__()

        # SET UP
        self.resize(800, 600)
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Troubleshooter")


        # ALL FONTS
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setWeight(50)
        title_font.setBold(True)

        text_font = QFont()
        text_font.setPointSize(8)

        bold_text_font = QFont()
        bold_text_font.setPointSize(10)
        bold_text_font.setBold(True)



        # FILE IMPORT SECTION
        self.file_import_layout = QGridLayout()
        file_import_header = QLabel()
        file_import_header.setText("File Import")
        file_import_header.setFont(title_font)
        file_import_header.setMaximumHeight(30)

        mts_label = QLabel()
        mts_label.setMaximumWidth(25)
        mts_label.setText("MTS:")
        mts_label.setFont(text_font)
        fluke_label = QLabel()
        fluke_label.setText("Fluke:")
        fluke_label.setFont(text_font)
        self.mts_file = QLabel(self)
        self.mts_file.setText("placeholder")
        self.mts_file.setFont(text_font)
        self.mts_file.hide()
        self.fluke_file = QLabel(self)
        self.fluke_file.setText("placeholder")
        self.fluke_file.setFont(text_font)
        self.fluke_file.hide()

        self.mts_file_button = QPushButton(self)
        self.mts_file_button.setText("Browse File")
        self.fluke_file_button = QPushButton(self)
        self.fluke_file_button.setText("Browse File")

        self.horizontal_spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer2 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer3 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer4 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer5 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer6 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer7 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer8 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.file_import_layout.addWidget(self.fluke_file, 2, 2)
        self.file_import_layout.addWidget(self.mts_file, 1, 2)
        self.file_import_layout.addItem(self.horizontal_spacer, 1, 3)
        self.file_import_layout.addItem(self.horizontal_spacer2, 2, 3)
        self.file_import_layout.addWidget(file_import_header, 0, 0)
        self.file_import_layout.addWidget(mts_label, 1, 0)
        self.file_import_layout.addWidget(fluke_label, 2, 0)
        self.file_import_layout.addWidget(self.mts_file_button, 1, 1)
        self.file_import_layout.addWidget(self.fluke_file_button, 2, 1)


        # DATA SELECTION SECTION
        self.disp = ""
        self.temp = ""
        self.mts_temp = []
        self.data_select_layout = QGridLayout()
        data_select_header = QLabel()
        data_select_header.setFont(title_font)
        data_select_header.setText("Data Selection")
        data_select_header.setMaximumHeight(30)

        temperature_label = QLabel()
        temperature_label.setText("Fluke Temperature:")
        temperature_label.setFont(text_font)
        displacement_label = QLabel()
        displacement_label.setFont(text_font)
        displacement_label.setText("Displacement:")
        mts_temp_label = QLabel()
        mts_temp_label.setText("MTS Temperature:")
        mts_temp_label.setFont(text_font)
        mts_start_time_label = QLabel()
        mts_start_time_label.setText("MTS Start Time (HH:MM:SS):")
        mts_start_time_label.setFont(text_font)
        self.horizontal_spacer9 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontal_spacer10 = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.temp_dropdown = QComboBox(self)
        self.temp_dropdown.setMaximumWidth(100)
        self.disp_dropdown = QComboBox(self)
        self.disp_dropdown.setMinimumWidth(100)
        self.temp_dropdown.setEnabled(False)
        self.disp_dropdown.setEnabled(False)
        self.mts_temp_dropdown = QComboBox(self)
        self.mts_temp_dropdown.setMaximumWidth(100)
        self.mts_temp_dropdown.setEnabled(False)
        self.mts_start_input = QLineEdit(self)
        self.mts_start_input.setMaximumWidth(100)
        self.mts_start_input.setEnabled(False)

        self.data_select_layout.addWidget(data_select_header, 0, 0)
        self.data_select_layout.addWidget(temperature_label, 1, 0)
        self.data_select_layout.addWidget(displacement_label, 2, 0)
        self.data_select_layout.addWidget(self.temp_dropdown, 1, 1)
        self.data_select_layout.addWidget(self.disp_dropdown, 2, 1)
        self.data_select_layout.addItem(self.horizontal_spacer4, 2, 5)
        self.data_select_layout.addWidget(mts_temp_label, 1, 3)
        self.data_select_layout.addWidget(self.mts_temp_dropdown, 1, 4)
        self.data_select_layout.addItem(self.horizontal_spacer3, 1, 5)
        self.data_select_layout.addWidget(mts_start_time_label, 2, 3)
        self.data_select_layout.addWidget(self.mts_start_input, 2, 4)
        self.data_select_layout.addItem(self.horizontal_spacer9, 1, 2)
        self.data_select_layout.addItem(self.horizontal_spacer10, 2, 2)


        # GRAPHS SECTIOM
        self.mts_figure = Figure()
        self.mts_graph = FigureCanvas(self.mts_figure)
        self.mts_toolbar = NavigationToolbar(self.mts_graph, self)
        self.fluke_figure = Figure()
        self.fluke_graph = FigureCanvas(self.fluke_figure)
        self.fluke_toolbar = NavigationToolbar(self.fluke_graph, self)


        # POINT SELECTION SECTION
        self.selected_mts_points = np.zeros([2, 1])
        self.selected_fluke_points = np.zeros([2, 1])
        instructions1 = QLabel()
        instructions1.setText("Click point on graph to sync with.")
        instructions1.setFont(bold_text_font)
        instructions1.setMaximumHeight(20)
        instructions2 = QLabel()
        instructions2.setText("Click point on graph to sync with.")
        instructions2.setFont(bold_text_font)
        instructions2.setMaximumHeight(20)
        self.mts_point_display = QLabel(self)
        self.mts_point_display.setFont(text_font)
        self.mts_point_display.setText("Points in range of click selection: ")
        self.mts_point_display.setMaximumHeight(70)
        self.mts_point_display.setWordWrap(True)
        self.fluke_point_display = QLabel(self)
        self.fluke_point_display.setFont(text_font)
        self.fluke_point_display.setText("Points in range of click selection: ")
        self.fluke_point_display.setMaximumHeight(70)
        self.fluke_point_display.setWordWrap(True)

        self.mts_point_select = QHBoxLayout()
        self.point_blurb = QLabel()
        self.point_blurb.setFont(text_font)
        self.point_blurb.setText("Finer point selection:")
        self.point_blurb.setMaximumHeight(20)
        self.mts_point_dropdown = QComboBox(self)
        self.mts_point_dropdown.setMaximumWidth(100)
        self.mts_point_dropdown.setEnabled(False)
        self.mts_point_select.addWidget(self.point_blurb, 0)
        self.mts_point_select.addWidget(self.mts_point_dropdown, 1)
        self.mts_point_select.addItem(self.horizontal_spacer5)

        self.fluke_point_select = QHBoxLayout()
        self.point_blurb2 = QLabel()
        self.point_blurb2.setFont(text_font)
        self.point_blurb2.setText("Finer point selection:")
        self.point_blurb2.setMaximumHeight(20)
        self.fluke_point_dropdown = QComboBox(self)
        self.fluke_point_dropdown.setMaximumWidth(100)
        self.fluke_point_dropdown.setEnabled(False)
        self.fluke_point_select.addWidget(self.point_blurb2, 0)
        self.fluke_point_select.addWidget(self.fluke_point_dropdown, 1)
        self.fluke_point_select.addItem(self.horizontal_spacer6)
        self.mts_x = 0
        self.fluke_x = 0


        # BUTTON SECTION
        self.button_layout = QHBoxLayout()
        self.test_sync_button = QPushButton(self)
        self.test_sync_button.setText("Dive Deeper")
        self.test_sync_button.setFont(bold_text_font)
        self.sync_button = QPushButton(self)
        self.sync_button.setText("Apply Sync")
        self.sync_button.setFont(bold_text_font)
        self.button_layout.addItem(self.horizontal_spacer7)
        self.button_layout.addWidget(self.test_sync_button)
        self.button_layout.addWidget(self.sync_button)
        self.button_layout.addItem(self.horizontal_spacer8)


        # DELAY/SYNC
        self.delay = 0
        self.mts_time = []
        self.fluke_time = []
        self.temperature = []
        self.temperature = []
        self.displacement = []


        # ADDING TO FINAL LAYOUT
        self.main_layout.addLayout(self.file_import_layout, 0, 0)
        self.main_layout.addLayout(self.data_select_layout, 0, 1)
        self.main_layout.addWidget(self.mts_toolbar, 1, 0)
        self.main_layout.addWidget(self.fluke_toolbar, 1, 1)
        self.main_layout.addWidget(self.mts_graph, 2, 0)
        self.main_layout.addWidget(self.fluke_graph, 2, 1)
        self.main_layout.addWidget(instructions1, 3, 0)
        self.main_layout.addWidget(instructions2, 3, 1)
        self.main_layout.addWidget(self.mts_point_display, 4, 0)
        self.main_layout.addWidget(self.fluke_point_display, 4, 1)
        self.main_layout.addLayout(self.mts_point_select, 5, 0)
        self.main_layout.addLayout(self.fluke_point_select, 5, 1)
        self.main_layout.addLayout(self.button_layout, 6, 0, 1, 2)


        # SIGNALS
        self.mts_file_button.clicked.connect(self.getMTSFile)
        self.fluke_file_button.clicked.connect(self.getFlukeFile)
        self.disp_dropdown.currentIndexChanged.connect(self.getDispAndPlot)
        self.temp_dropdown.currentIndexChanged.connect(self.getTempAndPlot)
        self.mts_figure.canvas.mpl_connect('pick_event', self.on_pick_mts)
        self.fluke_figure.canvas.mpl_connect('pick_event', self.on_pick_fluke)
        self.mts_point_dropdown.currentIndexChanged.connect(self.getMTSPoint)
        self.fluke_point_dropdown.currentIndexChanged.connect(self.getFlukePoint)
        self.test_sync_button.clicked.connect(self.plotTestSync)
        self.sync_button.clicked.connect(self.sync)
        self.mts_temp_dropdown.currentIndexChanged.connect(self.getMTSTemp)
        self.mts_start_input.editingFinished.connect(self.getMTSStartAndSync)

        # INITIAL CONDITIONS
        self.start_time = 0
        self.end_time = 0



    # FUNCTIONS
    def getMTSFile(self):
        fileloc = QFileDialog.getOpenFileName(None, "Open MTS Data File", "", "All Files(*);;Text Files(*.txt)")
        if fileloc:
            mtsloc = str(fileloc[0])
            filename = mtsloc[mtsloc.rindex("/") + 1:]
            mts = reader(mtsloc)
            mts.extract_txt()
            self.mts_temp_dropdown.blockSignals(True)
            self.disp_dropdown.blockSignals(True)
            self.disp_dropdown.addItems(mts.dataframe.columns)
            self.mts_temp_dropdown.addItems(mts.dataframe.columns)
            self.mts_data = mts.dataframe
            self.mts_file.setText(filename)
            self.mts_file.show()
            self.disp_dropdown.setEnabled(True)
            self.disp_dropdown.blockSignals(False)
            self.mts_temp_dropdown.setEnabled(True)
            self.mts_temp_dropdown.blockSignals(False)
            self.mts_start_input.setEnabled(True)


    def getFlukeFile(self):
        fileloc = QFileDialog.getOpenFileName(None, "Open Fluke Data File", "",
                                              "CSV Files(*.csv);;Excel Files(*.xlsx)")
        if fileloc:
            flukeloc = str(fileloc[0])
            filename = flukeloc[flukeloc.rindex("/") + 1:]
            fluke = reader(flukeloc)
            fluke.extract_fluke()
            self.temp_dropdown.blockSignals(True)
            self.temp_dropdown.addItems(fluke.dataframe.columns)
            self.fluke_data = fluke.dataframe
            self.fluke_start_time = fluke.start_time
            self.fluke_file.setText(filename)
            self.fluke_file.show()
            self.temp_dropdown.setEnabled(True)
            self.temp_dropdown.blockSignals(False)


    def getDispAndPlot(self):
        self.disp = self.disp_dropdown.currentText()
        self.mts_figure.clear()
        ax = self.mts_figure.add_subplot(111)
        time = self.mts_data[self.mts_data.columns.tolist()[0]]
        disps = self.mts_data[self.disp]
        ax.plot(time, disps, picker=True, pickradius=1)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(self.disp)
        ax.set_title("Displacement over Time")

        self.mts_graph.draw()


    def getTempAndPlot(self):
        self.temp = self.temp_dropdown.currentText()
        temps = self.fluke_data[self.temp]
        temps = [float(x) for x in temps]
        self.fluke_figure.clear()
        ax = self.fluke_figure.add_subplot(111)
        time = self.fluke_data["Duration"]
        ax.plot(time, temps, picker=True, pickradius=1)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(self.temp)
        ax.set_title("Temperature over Time")

        self.fluke_graph.draw()


    def getMTSTemp(self):
        temp = self.mts_temp_dropdown.currentText()
        self.mts_temp = self.mts_data[temp]


    def getMTSStartAndSync(self):
        start = self.mts_start_input.text()
        mts = self.mts_data.copy()
        fluke = self.fluke_data.copy()
        fluke_start_day = self.fluke_start_time.split()[0]
        if ("/" in fluke["Start Time"].iloc[0]):
            fluke["Start Time"] = [datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S.%f") for x in fluke["Start Time"]]
        else:
            fluke["Start Time"] = [
                datetime.datetime.strptime("{} {}".format(fluke_start_day, x), "%m/%d/%Y %H:%M:%S.%f")
                for x in fluke["Start Time"]]
        for col in fluke.columns:
            try:
                fluke[col] = fluke[col].astype(float)
            except:
                pass

        time_col = mts.iloc[:, 0]
        mts_start = datetime.datetime.strptime("{} {}".format(fluke_start_day, start), "%m/%d/%Y %H:%M:%S")
        abs_times = [mts_start + datetime.timedelta(seconds=time) for time in time_col]
        mts.insert(0, "Global Time", abs_times)

        mts_diffs = [str(x)[str(x).index(".") + 1:] for x in np.diff(np.array(abs_times))]
        for i in range(len(mts_diffs)):
            idx = len(mts_diffs[i]) - 1
            while mts_diffs[i][idx] == "0":
                idx -= 1
            mts_diffs[i] = len(mts_diffs[i][:idx + 1])
        occurrences = Counter(mts_diffs)
        num_digit_sep = 0
        for k in range(max(mts_diffs), -1, -1):
            if occurrences[k] / len(mts_diffs) * 100 > 4.6:
                num_digit_sep = k
                break
        min_time_sep = 1 / (10 ** num_digit_sep)

        sep = "{}S".format(min_time_sep)
        mts = mts.set_index("Global Time").resample(sep).interpolate()
        fluke = fluke.set_index("Start Time").resample(sep).interpolate()

        self.combined_data = pd.concat([fluke, mts], axis=1)


    def on_pick_mts(self, event):
        self.mts_point_dropdown.setEnabled(True)
        self.mts_point_dropdown.clear()
        line = event.artist
        xdata, ydata = line.get_data()
        ind = event.ind
        self.selected_mts_points = np.array([xdata[ind], ydata[ind]])
        text = "Points in range of selection: "
        for i in range(len(self.selected_mts_points[0])):
            point = "(" + str(self.selected_mts_points[0][i]) + ", " + str(self.selected_mts_points[1][i]) + ")"
            self.mts_point_dropdown.addItem(point)
            text += point
            if i != len(self.selected_mts_points[0]) - 1:
                text += ", "
        self.mts_point_display.setText(text)


    def on_pick_fluke(self, event):
        self.fluke_point_dropdown.setEnabled(True)
        self.fluke_point_dropdown.clear()
        line = event.artist
        xdata, ydata = line.get_data()
        ind = event.ind
        self.selected_fluke_points = np.array([xdata[ind], ydata[ind]])
        text = "Points in range of selection: "
        for i in range(len(self.selected_fluke_points[0])):
            point = "(" + str(self.selected_fluke_points[0][i]) + ", " + str(self.selected_fluke_points[1][i]) + ")"
            self.fluke_point_dropdown.addItem(point)
            text += point
            if i != len(self.selected_fluke_points[0]) - 1:
                text += ", "
        self.fluke_point_display.setText(text)


    def getMTSPoint(self):
        text = self.mts_point_dropdown.currentText()
        self.mts_x = float(text[text.index("(") + 1:text.index(",")])


    def getFlukePoint(self):
        text = self.fluke_point_dropdown.currentText()
        self.fluke_x = float(text[text.index("(") + 1:text.index(",")])


    def plotTestSync(self):
        # extract data
        mts_time = self.mts_data[self.mts_data.columns[0]].tolist()
        self.mts_time = mts_time
        fluke_time = self.fluke_data["Duration"].tolist()
        self.fluke_time = fluke_time
        temp = self.fluke_data[self.temp].tolist()
        temp = [float(x) for x in temp]
        disp = self.mts_data[self.disp].tolist()

        # get indexes that correlate to chosen points
        mts_start_ind = mts_time.index(self.mts_x)
        fluke_start_ind = fluke_time.index(self.fluke_x)

        # synchronize times
        mts_factor = mts_time[mts_start_ind]
        fluke_factor = fluke_time[fluke_start_ind]
        mts_time = [x - (mts_factor - fluke_factor) for x in mts_time]
        disp = minmax_scale(disp, feature_range=(0, 1))
        temp = minmax_scale(temp, feature_range=(0, 1))
        self.temperature = temp
        self.displacement = disp


        test_sync_fig = Figure()
        ax = test_sync_fig.add_subplot(111)
        ax.plot(mts_time, disp, label="Displacement")
        ax.plot(fluke_time, temp, label="Temperature")
        ax.set_xlabel("Time (s)")
        ax.set_title("Fluke Temperature and Displacement")
        ax.legend(loc="best")

        self.delay = mts_factor - fluke_factor
        self.delay_updated.emit()

        self.sync_window = SyncWindow(test_sync_fig, max(mts_time[-1], fluke_time[-1]), self.delay, self.mts_time,
                                self.fluke_time, self.temperature, self.displacement, self.mts_temp, self.combined_data,
                                      self.disp, self.temp)
        self.sync_window.show()
        self.sync_window.delay_changed.connect(self.updateDelay)
        self.sync_window.start_time_changed.connect(self.updateStartTime)
        self.sync_window.end_time_changed.connect(self.updateEndTime)


    def getDelay(self):
        return self.delay


    def sync(self):
        mts_time = self.mts_data[self.mts_data.columns.tolist()[0]].tolist()
        fluke_time = self.fluke_data["Duration"].tolist()
        mts_start_ind = mts_time.index(self.mts_x)
        fluke_start_ind = fluke_time.index(self.fluke_x)
        mts_factor = mts_time[mts_start_ind]
        fluke_factor = fluke_time[fluke_start_ind]
        self.delay = mts_factor - fluke_factor
        self.delay_updated.emit()

        self.close()


    def updateDelay(self):
        self.delay = self.sync_window.getDelay()
        self.delay_updated.emit()


    def updateStartTime(self):
        self.start_time = self.sync_window.returnStartTime()
        self.start_time_updated.emit()


    def updateEndTime(self):
        self.end_time = self.sync_window.returnEndTime()
        self.end_time_updated.emit()


    def getStartTime(self):
        return self.start_time


    def getEndTime(self):
        return self.end_time



# if __name__ == "__main__":
#     import sys
#     app = QApplication([])
#     window = TroubleshootWindow()
#     window.show()
#     sys.exit(app.exec())