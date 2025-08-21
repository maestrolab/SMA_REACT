# -*- coding: utf-8 -*-
"""
Created on Wed May  7 10:06:26 2025

@author: 362490
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'smaeat_gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys
import os
from pathlib import Path
# Add src/ to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, parent_dir)
from src.preprocessor.data_reader import reader
from src.preprocessor.analyze_mts_only import analyze_mts
from src.preprocessor.analyze_fluke_and_mts import analyze_fmts
from src.preprocessor.Geometry_Code_In_Console import Geometry_input
from src.preprocessor.plot_dsc import plotDSC
from src.preprocessor.troubleshoot_window import TroubleshootWindow
import cgitb
cgitb.enable(format="text")

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        screen_w, screen_h = screen.width(), screen.height()
        MainWindow.setObjectName("MainWindow")
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        MainWindow.resize(int(screen.width() * 1), int(screen.height() * 1))
        MainWindow.showMaximized()
        bold_font = QtGui.QFont()
        bold_font.setPointSize(15)
        bold_font.setBold(True)
        bold_font.setWeight(75)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mts_data_file_input_button = QtWidgets.QPushButton(self.centralwidget)
        self.mts_data_file_input_button.setGeometry(QtCore.QRect(int(screen_w * .1000), int(screen_h * 0.0500), int(screen_w * 0.0938), int(screen_h * 0.0288)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.mts_data_file_input_button.setFont(font)
        self.mts_data_file_input_button.setCheckable(False)
        self.mts_data_file_input_button.setChecked(False)
        self.mts_data_file_input_button.setObjectName("mts_data_file_input_button")
        self.file_input_label = QtWidgets.QLabel(self.centralwidget)
        self.file_input_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.0125), int(screen_w * 0.1263), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.file_input_label.setFont(font)
        self.file_input_label.setObjectName("file_input_label")
        self.mts_data_input_label = QtWidgets.QLabel(self.centralwidget)
        self.mts_data_input_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.0500), int(screen_w * 0.0762), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.mts_data_input_label.setFont(font)
        self.mts_data_input_label.setObjectName("mts_data_input_label")
        self.mts_data_file_display_label = QtWidgets.QLabel(self.centralwidget)
        self.mts_data_file_display_label.setGeometry(QtCore.QRect(int(screen_w * 0.2000), int(screen_h * 0.0537), int(screen_w * 0.1875), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.mts_data_file_display_label.setFont(font)
        self.mts_data_file_display_label.setObjectName("mts_data_file_display_label")
        self.fluke_data_input_label = QtWidgets.QLabel(self.centralwidget)
        self.fluke_data_input_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.0838), int(screen_w * 0.0887), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.fluke_data_input_label.setFont(font)
        self.fluke_data_input_label.setObjectName("fluke_data_input_label")
        self.fluke_data_file_input_button = QtWidgets.QPushButton(self.centralwidget)
        self.fluke_data_file_input_button.setGeometry(QtCore.QRect(int(screen_w * 0.1000), int(screen_h * 0.0838), int(screen_w * 0.0938), int(screen_h * 0.0288)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.fluke_data_file_input_button.setFont(font)
        self.fluke_data_file_input_button.setCheckable(False)
        self.fluke_data_file_input_button.setChecked(False)
        self.fluke_data_file_input_button.setObjectName("fluke_data_file_input_button")
        self.fluke_data_file_display_label = QtWidgets.QLabel(self.centralwidget)
        self.fluke_data_file_display_label.setGeometry(QtCore.QRect(int(screen_w * 0.2000), int(screen_h * 0.0875), int(screen_w * 0.1875), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.fluke_data_file_display_label.setFont(font)
        self.fluke_data_file_display_label.setObjectName("fluke_data_file_display_label")
        self.optional_label_file = QtWidgets.QLabel(self.centralwidget)
        self.optional_label_file.setGeometry(QtCore.QRect(int(screen_w * 0.0138), int(screen_h * 0.1087), int(screen_w * 0.0762), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.optional_label_file.setFont(font)
        self.optional_label_file.setObjectName("optional_label_file")
        self.horizontal_separator1 = QtWidgets.QFrame(self.centralwidget)
        self.horizontal_separator1.setGeometry(QtCore.QRect(int(screen_w * 0.0000), int(screen_h * 0.1375), int(screen_w * 1.0000), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.horizontal_separator1.setFont(font)
        self.horizontal_separator1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontal_separator1.setLineWidth(1)
        self.horizontal_separator1.setMidLineWidth(2)
        self.horizontal_separator1.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_separator1.setObjectName("horizontal_separator1")
        self.time_sync_label = QtWidgets.QLabel(self.centralwidget)
        self.time_sync_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.0000), int(screen_w * 0.2762), int(screen_h * 0.0387)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.time_sync_label.setFont(font)
        self.time_sync_label.setObjectName("time_sync_label")
        self.vertical_separator_file_time = QtWidgets.QFrame(self.centralwidget)
        self.vertical_separator_file_time.setGeometry(QtCore.QRect(int(screen_w * 0.3750), int(screen_h * 0.0000), int(screen_w * 0.0250), int(screen_h * 0.1512)))
        self.vertical_separator_file_time.setFrameShadow(QtWidgets.QFrame.Plain)
        self.vertical_separator_file_time.setMidLineWidth(2)
        self.vertical_separator_file_time.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_separator_file_time.setObjectName("vertical_separator_file_time")
        self.time_interval_label = QtWidgets.QLabel(self.centralwidget)
        self.time_interval_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.0437), int(screen_w * 0.1375), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.time_interval_label.setFont(font)
        self.time_interval_label.setObjectName("time_interval_label")
        self.time_interval_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.time_interval_line_edit.setGeometry(QtCore.QRect(int(screen_w * 0.5437), int(screen_h * 0.0437), int(screen_w * 0.0638), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.time_interval_line_edit.setFont(font)
        self.time_interval_line_edit.setText("") # MTS Start time, no idea why they called it interval
        self.time_interval_line_edit.setObjectName("time_interval_line_edit")
        self.time_interval_line_edit.setEnabled(False)
        self.end_time_label = QtWidgets.QLabel(self.centralwidget)
        self.end_time_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.0813), int(screen_w * 0.1263), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.end_time_label.setFont(font)
        self.end_time_label.setObjectName("end_time_label")
        self.end_time_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.end_time_line_edit.setGeometry(QtCore.QRect(int(screen_w * 0.5437), int(screen_h * 0.0813), int(screen_w * 0.0638), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.end_time_line_edit.setFont(font)
        self.end_time_line_edit.setText("")
        self.end_time_line_edit.setObjectName("end_time_line_edit")
        self.delay_label = QtWidgets.QLabel(self.centralwidget)
        self.delay_label.setGeometry(QtCore.QRect(int(screen_w * 0.6875), int(screen_h * 0.1187), int(screen_w * 0.0688), int(screen_h * 0.0250)))
        self.delay_label.setText("Estimated Instrument Delay (s):")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(50)
        self.delay_label.setFont(font)
        self.delay_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.delay_line_edit.setGeometry(QtCore.QRect(int(screen_w * 0.7625), int(screen_h * 0.1187), int(screen_w * 0.0638), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.delay_line_edit.setFont(font)
        self.delay_line_edit.setObjectName("delay_line_edit")
        self.delay_line_edit.setEnabled(False)
        self.default_delay_label = QtWidgets.QLabel(self.centralwidget)
        self.default_delay_label.setGeometry(QtCore.QRect(int(screen_w * 0.8375), int(screen_h * 0.1187), int(screen_w * 0.0688), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.default_delay_label.setFont(font)
        self.default_delay_label.setObjectName("default_delay_label")
        self.default_delay_label.setText("*Default*")
        self.default_delay_label.hide()
        self.delay_blurb = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.delay_blurb.setFont(font)
        self.delay_blurb.setText("Delay quantifies the difference in start time between the fluke start and MTS start. A negative delay indicates that the fluke begin recording data before the MTS.")
        self.delay_blurb.setWordWrap(True)
        self.delay_blurb.setGeometry(QtCore.QRect(int(screen_w * 0.6875), int(screen_h * 0.0312), int(screen_w * 0.2000), int(screen_h * 0.0938)))
        self.vertical_separator_time_glitch = QtWidgets.QFrame(self.centralwidget)
        self.vertical_separator_time_glitch.setGeometry(QtCore.QRect(int(screen_w * 0.6750), int(screen_h * 0.1500), int(screen_w * 0.0250), int(screen_h * 0.1363)))
        self.vertical_separator_time_glitch.setFrameShadow(QtWidgets.QFrame.Plain)
        self.vertical_separator_time_glitch.setMidLineWidth(2)
        self.vertical_separator_time_glitch.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_separator_time_glitch.setObjectName("vertical_separator_time_glitch")
        self.glitch_text_text = QtWidgets.QLabel(self.centralwidget)
        self.glitch_text_text.setGeometry(QtCore.QRect(int(screen_w * 0.7000), int(screen_h * 0.1688), int(screen_w * 0.2888), int(screen_h * 0.1013)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.glitch_text_text.setFont(font)
        self.glitch_text_text.setAutoFillBackground(False)
        self.glitch_text_text.setWordWrap(True)
        self.glitch_text_text.setObjectName("glitch_text_text")
        self.glitch_check_label = QtWidgets.QLabel(self.centralwidget)
        self.glitch_check_label.setGeometry(QtCore.QRect(int(screen_w * 0.7000), int(screen_h * 0.1562), int(screen_w * 0.2762), int(screen_h * 0.0387)))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.glitch_check_label.setFont(font)
        self.glitch_check_label.setObjectName("glitch_check_label")
        self.glitch_check_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.glitch_check_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.7000), int(screen_h * 0.2500), int(screen_w * 0.1388), int(screen_h * 0.0275)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.glitch_check_dropdown.setFont(font)
        self.glitch_check_dropdown.setObjectName("glitch_check_dropdown")
        self.glitch_check_dropdown.addItem("")
        self.glitch_check_dropdown.addItem("")
        self.glitch_check_dropdown.addItem("")
        self.mts_data_selection_label = QtWidgets.QLabel(self.centralwidget)
        self.mts_data_selection_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.1625), int(screen_w * 0.2512), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.mts_data_selection_label.setFont(font)
        self.mts_data_selection_label.setObjectName("mts_data_selection_label")
        self.mts_temp_select_label = QtWidgets.QLabel(self.centralwidget)
        self.mts_temp_select_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.2000), int(screen_w * 0.1013), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.mts_temp_select_label.setFont(font)
        self.mts_temp_select_label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.mts_temp_select_label.setObjectName("mts_temp_select_label")
        self.mts_temp_select_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.mts_temp_select_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.1250), int(screen_h * 0.1988), int(screen_w * 0.1375), int(screen_h * 0.0275)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.mts_temp_select_dropdown.setFont(font)
        self.mts_temp_select_dropdown.setObjectName("mts_temp_select_dropdown")
        self.mts_temp_select_dropdown.addItem("")
        self.disp_label = QtWidgets.QLabel(self.centralwidget)
        self.disp_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.2400), int(screen_w * 0.1013), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.disp_label.setFont(font)
        self.disp_label.setObjectName("disp_label")
        self.disp_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.disp_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.1250), int(screen_h * 0.2375), int(screen_w * 0.1375), int(screen_h * 0.0275)))
        self.disp_dropdown.setObjectName("disp_dropdown")
        self.disp_dropdown.addItem("")
        self.vertical_separator_data_select = QtWidgets.QFrame(self.centralwidget)
        self.vertical_separator_data_select.setGeometry(QtCore.QRect(int(screen_w * 0.3125), int(screen_h * 0.1500), int(screen_w * 0.0250), int(screen_h * 0.1350)))
        self.vertical_separator_data_select.setFrameShadow(QtWidgets.QFrame.Plain)
        self.vertical_separator_data_select.setMidLineWidth(2)
        self.vertical_separator_data_select.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_separator_data_select.setObjectName("vertical_separator_data_select")
        self.fluke_data_select_label = QtWidgets.QLabel(self.centralwidget)
        self.fluke_data_select_label.setGeometry(QtCore.QRect(int(screen_w * 0.3375), int(screen_h * 0.1625), int(screen_w * 0.2637), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.fluke_data_select_label.setFont(font)
        self.fluke_data_select_label.setObjectName("fluke_data_select_label")
        self.fluke_temp_label = QtWidgets.QLabel(self.centralwidget)
        self.fluke_temp_label.setGeometry(QtCore.QRect(int(screen_w * 0.3375), int(screen_h * 0.2000), int(screen_w * 0.1013), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fluke_temp_label.setFont(font)
        self.fluke_temp_label.setObjectName("fluke_temp_label")
        self.fluke_temp_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.fluke_temp_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.4500), int(screen_h * 0.1988), int(screen_w * 0.1138), int(screen_h * 0.0275)))
        self.fluke_temp_dropdown.setObjectName("fluke_temp_dropdown")
        self.fluke_temp_dropdown.addItem("")
        self.fluke_temp_dropdown.setEnabled(False)
        self.fluke_temp_blurb = QtWidgets.QLabel(self.centralwidget)
        self.fluke_temp_blurb.setGeometry(QtCore.QRect(int(screen_w * 0.3450), int(screen_h * 0.2275), int(screen_w * 0.2137), int(screen_h * 0.0387)))
        self.fluke_temp_blurb.setAlignment(QtCore.Qt.AlignCenter)
        self.fluke_temp_blurb.setWordWrap(True)
        self.fluke_temp_blurb.setObjectName("fluke_temp_blurb")
        self.horizontal_separator2 = QtWidgets.QFrame(self.centralwidget)
        self.horizontal_separator2.setGeometry(QtCore.QRect(int(screen_w * 0.0000), int(screen_h * 0.2750), int(screen_w * 1.0137), int(screen_h * 0.0200)))
        self.horizontal_separator2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontal_separator2.setMidLineWidth(2)
        self.horizontal_separator2.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_separator2.setObjectName("horizontal_separator2")
        self.cross_section_label = QtWidgets.QLabel(self.centralwidget)
        self.cross_section_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.3000), int(screen_w * 0.3387), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.cross_section_label.setFont(font)
        self.cross_section_label.setObjectName("cross_section_label")
        self.shape_label = QtWidgets.QLabel(self.centralwidget)
        self.shape_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.3375), int(screen_w * 0.0512), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.shape_label.setFont(font)
        self.shape_label.setObjectName("shape_label")
        self.shape_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.shape_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.1125), int(screen_h * 0.3350), int(screen_w * 0.1138), int(screen_h * 0.0275)))
        self.shape_dropdown.setObjectName("shape_dropdown")
        self.shape_dropdown.addItem("")
        self.shape_dropdown.addItem("")
        self.shape_dropdown.addItem("")
        self.shape_dropdown.addItem("")
        self.shape_dropdown.addItem("")
        self.input_unit_label = QtWidgets.QLabel(self.centralwidget)
        self.input_unit_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.3750), int(screen_w * 0.0762), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.input_unit_label.setFont(font)
        self.input_unit_label.setObjectName("input_unit_label")
        self.input_unit_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.input_unit_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.1125), int(screen_h * 0.3725), int(screen_w * 0.1138), int(screen_h * 0.0275)))
        self.input_unit_dropdown.setObjectName("input_unit_dropdown")
        self.input_unit_dropdown.addItem("")
        self.input_unit_dropdown.addItem("")
        self.input_unit_dropdown.addItem("")
        self.input_unit_dropdown.addItem("")
        self.output_unit_label = QtWidgets.QLabel(self.centralwidget)
        self.output_unit_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.4100), int(screen_w * 0.0887), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.output_unit_label.setFont(font)
        self.output_unit_label.setObjectName("output_unit_label")
        self.output_unit_dropdown = QtWidgets.QComboBox(self.centralwidget)
        self.output_unit_dropdown.setGeometry(QtCore.QRect(int(screen_w * 0.1125), int(screen_h * 0.4100), int(screen_w * 0.1138), int(screen_h * 0.0275)))
        self.output_unit_dropdown.setObjectName("output_unit_dropdown")
        self.output_unit_dropdown.addItem("")
        self.output_unit_dropdown.addItem("")
        self.output_unit_dropdown.addItem("")
        self.output_unit_dropdown.addItem("")
        self.measurement_label = QtWidgets.QLabel(self.centralwidget)
        self.measurement_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.4475), int(screen_w * 0.1013), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setStrikeOut(False)
        self.measurement_label.setFont(font)
        self.measurement_label.setObjectName("measurement_label")
        self.measurement_input = QtWidgets.QLineEdit(self.centralwidget)
        self.measurement_input.setGeometry(QtCore.QRect(int(screen_w * 0.1125), int(screen_h * 0.4475), int(screen_w * 0.1138), int(screen_h * 0.0250)))
        self.measurement_input.setObjectName("measurement_input")
        self.width_label = QtWidgets.QLabel(self.centralwidget)
        self.width_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.4850), int(screen_w * 0.0688), int(screen_h * 0.0325)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.width_label.setFont(font)
        self.width_label.setObjectName("width_label")
        self.width_input = QtWidgets.QLineEdit(self.centralwidget)
        self.width_input.setGeometry(QtCore.QRect(int(screen_w * 0.1125), int(screen_h * 0.4850), int(screen_w * 0.1138), int(screen_h * 0.0250)))
        self.width_input.setObjectName("width_input")
        self.vertical_separator_csect_movavg = QtWidgets.QFrame(self.centralwidget)
        self.vertical_separator_csect_movavg.setGeometry(QtCore.QRect(int(screen_w * 0.3787), int(screen_h * 0.2850), int(screen_w * 0.0250), int(screen_h * 0.3063)))
        self.vertical_separator_csect_movavg.setFrameShadow(QtWidgets.QFrame.Plain)
        self.vertical_separator_csect_movavg.setMidLineWidth(2)
        self.vertical_separator_csect_movavg.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_separator_csect_movavg.setObjectName("vertical_separator_csect_movavg")
        self.movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.2925), int(screen_w * 0.3387), int(screen_h * 0.0387)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.movavg_label.setFont(font)
        self.movavg_label.setObjectName("movavg_label")
        self.movavg_blurb = QtWidgets.QLabel(self.centralwidget)
        self.movavg_blurb.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.3275), int(screen_w * 0.5513), int(screen_h * 0.0638)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.movavg_blurb.setFont(font)
        self.movavg_blurb.setWordWrap(True)
        self.movavg_blurb.setObjectName("movavg_blurb")
        self.mts_temp_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.mts_temp_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.5000), int(screen_w * 0.4637), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mts_temp_movavg_label.setFont(font)
        self.mts_temp_movavg_label.setObjectName("mts_temp_movavg_label")
        self.load_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.load_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.4688), int(screen_w * 0.4637), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.load_movavg_label.setFont(font)
        self.load_movavg_label.setObjectName("load_movavg_label")
        self.fluke_temp_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.fluke_temp_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.5312), int(screen_w * 0.4637), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fluke_temp_movavg_label.setFont(font)
        self.fluke_temp_movavg_label.setObjectName("fluke_temp_movavg_label")
        self.disp_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.disp_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.4375), int(screen_w * 0.4637), int(screen_h * 0.0200)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.disp_movavg_label.setFont(font)
        self.disp_movavg_label.setObjectName("disp_movavg_label")
        self.disp_movavg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.disp_movavg_input.setGeometry(QtCore.QRect(int(screen_w * 0.8500), int(screen_h * 0.4375), int(screen_w * 0.1412), int(screen_h * 0.0250)))
        self.disp_movavg_input.setObjectName("disp_movavg_input")
        self.load_movavg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.load_movavg_input.setGeometry(QtCore.QRect(int(screen_w * 0.8500), int(screen_h * 0.4688), int(screen_w * 0.1412), int(screen_h * 0.0250)))
        self.load_movavg_input.setObjectName("load_movavg_input")
        self.mts_temp_movavg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.mts_temp_movavg_input.setGeometry(QtCore.QRect(int(screen_w * 0.8500), int(screen_h * 0.5000), int(screen_w * 0.1412), int(screen_h * 0.0250)))
        self.mts_temp_movavg_input.setObjectName("mts_temp_movavg_input")
        self.fluke_temp_movavg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.fluke_temp_movavg_input.setGeometry(QtCore.QRect(int(screen_w * 0.8500), int(screen_h * 0.5312), int(screen_w * 0.1412), int(screen_h * 0.0250)))
        self.fluke_temp_movavg_input.setObjectName("fluke_temp_movavg_input")
        self.horizontal_separator3 = QtWidgets.QFrame(self.centralwidget)
        self.horizontal_separator3.setGeometry(QtCore.QRect(int(screen_w * 0.0000), int(screen_h * 0.5875), int(screen_w * 1.0000), int(screen_h * 0.0037)))
        self.horizontal_separator3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.horizontal_separator3.setMidLineWidth(2)
        self.horizontal_separator3.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontal_separator3.setObjectName("horizontal_separator3")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(int(screen_w * 0.7875), int(screen_h * 0.7875), int(screen_w * 0.1875), int(screen_h * 0.0750)))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.temp_movavg_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.temp_movavg_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.4000), int(screen_w * 0.1263), int(screen_h * 0.0213)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.temp_movavg_checkbox.setFont(font)
        self.temp_movavg_checkbox.setObjectName("temp_movavg_checkbox")
        self.disp_movavg_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.disp_movavg_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.5375), int(screen_h * 0.4000), int(screen_w * 0.1263), int(screen_h * 0.0213)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.disp_movavg_checkbox.setFont(font)
        self.disp_movavg_checkbox.setObjectName("disp_movavg_checkbox")
        self.load_movavg_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.load_movavg_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.6750), int(screen_h * 0.4000), int(screen_w * 0.0875), int(screen_h * 0.0213)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.load_movavg_checkbox.setFont(font)
        self.load_movavg_checkbox.setObjectName("load_movavg_checkbox")
        self.none_movavg_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.none_movavg_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.7500), int(screen_h * 0.4000), int(screen_w * 0.0875), int(screen_h * 0.0213)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.none_movavg_checkbox.setFont(font)
        self.none_movavg_checkbox.setObjectName("none_movavg_checkbox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(int(screen_w * 0.0000), int(screen_h * 0.0000), int(screen_w * 1.0000), int(screen_h * 0.0262)))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.satisfaction_label = QtWidgets.QLabel(self.centralwidget)
        self.satisfaction_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.5625), int(screen_w * 0.5250), int(screen_h * 0.0163)))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.satisfaction_label.setFont(font)
        self.satisfaction_label.setObjectName("satisfaction_label")
        self.satisfaction_label.setText("*If you are not satisfied with the plotted data, adjust inputs for the filter and rerun.*")
        # get the right location for the images
        if hasattr(sys, "_MEIPASS"):
            parent_dir = sys._MEIPASS
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.abspath(os.path.join(script_dir, ".."))
        # cross section images
        self.circle_img = QtWidgets.QLabel(self.centralwidget)
        self.circle_img.setGeometry(QtCore.QRect(int(screen_w * 0.2500), int(screen_h * 0.3312), int(screen_w * 0.09), int(screen_w * 0.09)))
        self.circle_img.setObjectName("circle_img")
        circle_path = os.path.join(parent_dir, "src", "preprocessor", "media", "circle.png")
        self.circle_img.setPixmap(QtGui.QPixmap(circle_path))
        self.circle_img.setScaledContents(True)
        self.circle_img.hide()
        self.rectangle_img = QtWidgets.QLabel(self.centralwidget)
        self.rectangle_img.setGeometry(QtCore.QRect(int(screen_w * 0.2500), int(screen_h * 0.3312), int(screen_w * 0.09), int(screen_w * 0.06)))
        self.rectangle_img.setObjectName("rectangle_img")
        rectangle_path = os.path.join(parent_dir, "src", "preprocessor", "media", "rectangle.png")
        self.rectangle_img.setPixmap(QtGui.QPixmap(rectangle_path))
        self.rectangle_img.setScaledContents(True)
        self.rectangle_img.hide()
        self.square_img = QtWidgets.QLabel(self.centralwidget)
        self.square_img.setGeometry(QtCore.QRect(int(screen_w * 0.2500), int(screen_h * 0.3312), int(screen_w * 0.09), int(screen_w * 0.09)))
        self.square_img.setObjectName("square_img")
        square_path = os.path.join(parent_dir, "src", "preprocessor", "media", "square.png")
        self.square_img.setPixmap(QtGui.QPixmap(square_path))
        self.square_img.setScaledContents(True)
        self.square_img.hide()
        self.circle_in_square_img = QtWidgets.QLabel(self.centralwidget)
        self.circle_in_square_img.setGeometry(QtCore.QRect(int(screen_w * 0.2500), int(screen_h * 0.3312), int(screen_w * 0.09), int(screen_w * 0.09)))
        self.circle_in_square_img.setObjectName("circle_in_square_img")
        circle_square_path = os.path.join(parent_dir, "src", "preprocessor", "media", "cintraquad.png")
        self.circle_in_square_img.setPixmap(QtGui.QPixmap(circle_square_path))
        self.circle_in_square_img.setScaledContents(True)
        self.circle_in_square_img.hide()
        self.custom_img = QtWidgets.QLabel(self.centralwidget)
        self.custom_img.setGeometry(QtCore.QRect(int(screen_w * 0.2500), int(screen_h * 0.3312), int(screen_w * 0.09), int(screen_w * 0.09)))
        self.custom_img.setObjectName("custom_img")
        custom_path = os.path.join(parent_dir, "src", "preprocessor", "media", "custom.png")
        self.custom_img.setPixmap(QtGui.QPixmap(custom_path))
        self.custom_img.setScaledContents(True)
        self.custom_img.hide()
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(int(screen_w * .96000), int(screen_h * 0.0000), int(screen_w * 0.0400), int(screen_w * 0.04)))
        self.logo.setObjectName("logo")
        logo_path = os.path.join(parent_dir, "src", "preprocessor", "media", "maestro_logo.png")
        self.logo.setPixmap(QtGui.QPixmap(logo_path))
        self.logo.setScaledContents(True)
        self.default_end_time_label = QtWidgets.QLabel(self.centralwidget)
        self.default_end_time_label.setGeometry(QtCore.QRect(int(screen_w * 0.6150), int(screen_h * 0.0813), int(screen_w * 0.0688), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.default_end_time_label.setFont(font)
        self.default_end_time_label.setObjectName("default_end_time_label")
        self.default_end_time_label.setText("*Default*")
        self.default_end_time_label.hide()
        self.start_time_label = QtWidgets.QLabel(self.centralwidget)
        self.start_time_label.setGeometry(QtCore.QRect(int(screen_w * 0.4000), int(screen_h * 0.1187), int(screen_w * 0.1263), int(screen_h * 0.0262)))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.start_time_label.setFont(font)
        self.start_time_label.setObjectName("start_time_label")
        self.start_time_label.setText("Start Count (s):")
        self.start_time_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.start_time_line_edit.setGeometry(QtCore.QRect(int(screen_w * 0.5437), int(screen_h * 0.1187), int(screen_w * 0.0638), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.start_time_line_edit.setFont(font)
        self.start_time_line_edit.setText("0")
        self.start_time_line_edit.setObjectName("start_time_line_edit")
        self.default_start_time_label = QtWidgets.QLabel(self.centralwidget)
        self.default_start_time_label.setGeometry(QtCore.QRect(int(screen_w * 0.6150), int(screen_h * 0.1187), int(screen_w * 0.0688), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.default_start_time_label.setFont(font)
        self.default_start_time_label.setObjectName("default_start_time_label")
        self.default_start_time_label.setText("*Default*")
        self.strain_input_label = QtWidgets.QLabel(self.centralwidget)
        self.strain_input_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.5938), int(screen_w * 0.3387), int(screen_h * 0.0387)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.strain_input_label.setFont(font)
        self.strain_input_label.setObjectName("strain_input_label")
        self.strain_input_label.setText("Strain Input")
        self.length_label = QtWidgets.QLabel(self.centralwidget)
        self.length_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.6500), int(screen_w * 0.1250), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.length_label.setFont(font)
        self.length_label.setObjectName("length_label")
        self.length_label.setText("Original Length (units maintained from above):")
        self.length_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.length_line_edit.setGeometry(QtCore.QRect(int(screen_w * 0.1375), int(screen_h * 0.6500), int(screen_w * 0.0938), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.length_line_edit.setFont(font)
        self.vertical_separator_length_dsc = QtWidgets.QFrame(self.centralwidget)
        self.vertical_separator_length_dsc.setGeometry(QtCore.QRect(int(screen_w * 0.2437), int(screen_h * 0.5900), int(screen_w * 0.0250), int(screen_h * 0.3750)))
        self.vertical_separator_length_dsc.setFrameShadow(QtWidgets.QFrame.Plain)
        self.vertical_separator_length_dsc.setMidLineWidth(2)
        self.vertical_separator_length_dsc.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_separator_length_dsc.setObjectName("vertical_separator_length_dsc")
        self.dsc_label = QtWidgets.QLabel(self.centralwidget)
        self.dsc_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.5938), int(screen_w * 0.0500), int(screen_h * 0.0387)))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.dsc_label.setFont(font)
        self.dsc_label.setObjectName("dsc_label")
        self.dsc_label.setText("DSC")
        self.dsc_data_label = QtWidgets.QLabel(self.centralwidget)
        self.dsc_data_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.6312), int(screen_w * 0.1250), int(screen_h * 0.0250)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dsc_data_label.setFont(font)
        self.dsc_data_label.setObjectName("dsc_data_label")
        self.dsc_data_label.setText("Data File (runs independently):")
        self.num_cycle_label = QtWidgets.QLabel(self.centralwidget)
        self.num_cycle_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.6625), int(screen_w * 0.1000), int(screen_h * 0.0500)))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.num_cycle_label.setFont(font)
        self.num_cycle_label.setObjectName("num_cycle_label")
        self.num_cycle_label.setText("Steps to plot:")
        self.num_cycle_label.setWordWrap(True)
        self.dsc_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.dsc_data_button.setGeometry(QtCore.QRect(int(screen_w * 0.3563), int(screen_h * 0.6312), int(screen_w * 0.0938), int(screen_h * 0.0288)))
        self.dsc_data_button.setText("Browse File")
        self.dsc_data_button.setObjectName("dsc_data_button")
        self.dsc_data_display_label = QtWidgets.QLabel(self.centralwidget)
        self.dsc_data_display_label.setGeometry(QtCore.QRect(int(screen_w * 0.4625), int(screen_h * 0.6312), int(screen_w * 0.1500), int(screen_h * 0.0262)))
        self.dsc_data_display_label.setText("DSC_DATA")
        self.dsc_data_display_label.setObjectName("dsc_data_display_label")
        self.dsc_data_display_label.hide()
        self.num_cycle_input = QtWidgets.QLineEdit(self.centralwidget)
        self.num_cycle_input.setGeometry(QtCore.QRect(int(screen_w * 0.3812), int(screen_h * 0.6750), int(screen_w * 0.0312), int(screen_h * 0.0288)))
        self.num_cycle_input.setObjectName("num_cycle_input")
        self.to_label = QtWidgets.QLabel(self.centralwidget)
        self.to_label.setGeometry(QtCore.QRect(int(screen_w * 0.4188), int(screen_h * 0.6750), int(screen_w * 0.0187), int(screen_h * 0.0288)))
        self.to_label.setText("to")
        self.to_label.setObjectName("to_label")
        self.num_cycle_input2 = QtWidgets.QLineEdit(self.centralwidget)
        self.num_cycle_input2.setGeometry(QtCore.QRect(int(screen_w * 0.4375), int(screen_h * 0.6750), int(screen_w * 0.0312), int(screen_h * 0.0288)))
        self.num_cycle_input2.setObjectName("num_cycle_input2")
        self.steps_button = QtWidgets.QPushButton(self.centralwidget)
        self.steps_button.setGeometry(QtCore.QRect(int(screen_w * 0.4938), int(screen_h * 0.6750), int(screen_w * 0.0938), int(screen_h * 0.0288)))
        self.steps_button.setObjectName("steps_button")
        self.steps_button.setText("Show Steps")
        self.vertical_separator_start_dsc = QtWidgets.QFrame(self.centralwidget)
        self.vertical_separator_start_dsc.setGeometry(QtCore.QRect(int(screen_w * 0.6250), int(screen_h * 0.5900), int(screen_w * 0.0250), int(screen_h * 0.3750)))
        self.vertical_separator_start_dsc.setFrameShadow(QtWidgets.QFrame.Plain)
        self.vertical_separator_start_dsc.setMidLineWidth(2)
        self.vertical_separator_start_dsc.setFrameShape(QtWidgets.QFrame.VLine)
        self.vertical_separator_start_dsc.setObjectName("vertical_separator_start_dsc")
        self.dsc_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.dsc_movavg_label.setObjectName("dsc_movavg_label")
        self.dsc_movavg_label.setText("Would you like to apply a moving average filter?")
        self.dsc_movavg_label.setFont(font)
        self.dsc_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.7125), int(screen_w * 0.1875), int(screen_h * 0.0500)))
        self.dsc_movavg_label.setWordWrap(True)
        self.dsc_movavg_yes_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dsc_movavg_yes_checkbox.setFont(font)
        self.dsc_movavg_yes_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.4750), int(screen_h * 0.7250), int(screen_w * 0.1425), int(screen_h * 0.0375)))
        self.dsc_movavg_yes_checkbox.setObjectName("dsc_movavg_yes_checkbox")
        self.yes_label = QtWidgets.QLabel(self.centralwidget)
        self.yes_label.setFont(font)
        self.yes_label.setObjectName("yes_label")
        self.yes_label.setText("Yes")
        self.yes_label.setGeometry(QtCore.QRect(int(screen_w * 0.4975), int(screen_h * 0.7275), int(screen_w * 0.0375), int(screen_h * 0.0288)))
        self.dsc_movavg_no_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.dsc_movavg_no_checkbox.setFont(font)
        self.dsc_movavg_no_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.5625), int(screen_h * 0.7250), int(screen_w * 0.1425), int(screen_h * 0.0375)))
        self.dsc_movavg_no_checkbox.setObjectName("dsc_movavg_no_checkbox")
        self.no_label = QtWidgets.QLabel(self.centralwidget)
        self.no_label.setFont(font)
        self.no_label.setObjectName("no_label")
        self.no_label.setText("No")
        self.no_label.setGeometry(QtCore.QRect(int(screen_w * 0.5850), int(screen_h * 0.7275), int(screen_w * 0.0375), int(screen_h * 0.0288)))
        self.x_axis_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.x_axis_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.7500), int(screen_w * 0.2500), int(screen_h * 0.0500)))
        self.x_axis_movavg_label.setFont(font)
        self.x_axis_movavg_label.setText("Number of Datapoints for x-axis:")
        self.x_axis_movavg_label.hide()
        self.y_axis_movavg_label = QtWidgets.QLabel(self.centralwidget)
        self.y_axis_movavg_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.7750), int(screen_w * 0.2500), int(screen_h * 0.0500)))
        self.y_axis_movavg_label.setFont(font)
        self.y_axis_movavg_label.setText("Number of Datapoints for y-axis:")
        self.y_axis_movavg_label.hide()
        self.x_movavg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.x_movavg_input.setFont(font)
        self.x_movavg_input.setGeometry(QtCore.QRect(int(screen_w * 0.35), int(screen_h * 0.7650), int(screen_w * 0.0500), int(screen_h * 0.0200)))
        self.x_movavg_input.hide()
        self.y_movavg_input = QtWidgets.QLineEdit(self.centralwidget)
        self.y_movavg_input.setFont(font)
        self.y_movavg_input.setGeometry(QtCore.QRect(int(screen_w * 0.35), int(screen_h * 0.790), int(screen_w * 0.05), int(screen_h * 0.0200)))
        self.y_movavg_input.hide()
        self.x_axis_label = QtWidgets.QLabel(self.centralwidget)
        self.x_axis_label.setFont(font)
        self.x_axis_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.8250), int(screen_w * 0.0750), int(screen_h * 0.0288)))
        self.x_axis_label.setText("X-axis:")
        self.y_axis_label = QtWidgets.QLabel(self.centralwidget)
        self.y_axis_label.setFont(font)
        self.y_axis_label.setGeometry(QtCore.QRect(int(screen_w * 0.2750), int(screen_h * 0.8625), int(screen_w * 0.0750), int(screen_h * 0.0288)))
        self.y_axis_label.setText("Y-axis:")
        self.x_axis_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.x_axis_combobox.setFont(font)
        self.x_axis_combobox.setGeometry(QtCore.QRect(int(screen_w * 0.3438), int(screen_h * 0.8250), int(screen_w * 0.1875), int(screen_h * 0.0288)))
        self.x_axis_combobox.addItem("Select...")
        self.y_axis_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.y_axis_combobox.setFont(font)
        self.y_axis_combobox.setGeometry(QtCore.QRect(int(screen_w * 0.3438), int(screen_h * 0.8688), int(screen_w * 0.1875), int(screen_h * 0.0288)))
        self.y_axis_combobox.addItem("Select...")
        self.clear_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_all_button.setGeometry(QtCore.QRect(int(screen_w * 0.6500), int(screen_h * 0.8500), int(screen_w * 0.1250), int(screen_h * 0.0375)))
        font.setBold(True)
        self.clear_all_button.setFont(font)
        self.clear_all_button.setObjectName("clear_all_button")
        self.clear_all_button.setText("Clear All")
        self.shape_dropdown.addItem("Custom")
        self.clear_csect_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_csect_button.setGeometry(QtCore.QRect(int(screen_w * 0.0063), int(screen_h * 0.5500), int(screen_w * 0.1125), int(screen_h * 0.0338)))
        font.setBold(False)
        self.clear_csect_button.setFont(font)
        self.clear_csect_button.setObjectName("clear_csect_button")
        self.clear_csect_button.setText("Clear Section")
        self.clear_movavg_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_movavg_button.setGeometry(QtCore.QRect(int(screen_w * 0.8438), int(screen_h * 0.3937), int(screen_w * 0.1125), int(screen_h * 0.0338)))
        self.clear_movavg_button.setFont(font)
        self.clear_movavg_button.setObjectName("clear_movavg_button")
        self.clear_movavg_button.setText("Clear Section")
        self.clear_dsc_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_dsc_button.setGeometry(QtCore.QRect(int(screen_w * 0.5212), int(screen_h * 0.5938), int(screen_w * 0.1125), int(screen_h * 0.0338)))
        self.clear_dsc_button.setFont(font)
        self.clear_dsc_button.setObjectName("clear_dsc_button")
        self.clear_dsc_button.setText("Clear Section")
        self.bandpass_blurb = QtWidgets.QLabel(self.centralwidget)
        self.bandpass_blurb.setText("Would you like to apply a bandpass filter to strain? (future work)")
        self.bandpass_blurb.setWordWrap(True)
        self.bandpass_blurb.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.6875), int(screen_w * 0.1625), int(screen_h * 0.0563)))
        self.bandpass_blurb.setFont(font)
        self.bandpass_yes_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.bandpass_yes_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.1875), int(screen_h * 0.6813), int(screen_w * 0.1425), int(screen_h * 0.0375)))
        self.bandpass_yes_checkbox.setEnabled(False)
        self.bandpass_no_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.bandpass_no_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.1875), int(screen_h * 0.7125), int(screen_w * 0.1425), int(screen_h * 0.0375)))
        self.bandpass_no_checkbox.setEnabled(False)
        self.bandpass_yes_label = QtWidgets.QLabel(self.centralwidget)
        self.bandpass_yes_label.setText("Yes")
        self.bandpass_yes_label.setFont(font)
        self.bandpass_yes_label.setGeometry(QtCore.QRect(int(screen_w * 0.2125), int(screen_h * 0.6887), int(screen_w * 0.0375), int(screen_h * 0.0187)))
        self.bandpass_no_label = QtWidgets.QLabel(self.centralwidget)
        self.bandpass_no_label.setText("No")
        self.bandpass_no_label.setFont(font)
        self.bandpass_no_label.setGeometry(QtCore.QRect(int(screen_w * 0.2125), int(screen_h * 0.7200), int(screen_w * 0.0375), int(screen_h * 0.0187)))
        self.lowpass_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.lowpass_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.0500), int(screen_h * 0.7500), int(screen_w * 0.1425), int(screen_h * 0.0375)))
        self.highpass_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.highpass_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.1500), int(screen_h * 0.7500), int(screen_w * 0.1425), int(screen_h * 0.0375)))
        self.low_label = QtWidgets.QLabel(self.centralwidget)
        self.low_label.setGeometry(QtCore.QRect(int(screen_w * 0.0712), int(screen_h * 0.7562), int(screen_w * 0.0375), int(screen_h * 0.0213)))
        self.low_label.setText("Low")
        self.low_label.setFont(font)
        self.high_label = QtWidgets.QLabel(self.centralwidget)
        self.high_label.setGeometry(QtCore.QRect(int(screen_w * 0.1713), int(screen_h * 0.7562), int(screen_w * 0.0375), int(screen_h * 0.0213)))
        self.high_label.setText("High")
        self.high_label.setFont(font)
        self.order_input = QtWidgets.QLineEdit(self.centralwidget)
        self.order_input.setGeometry(QtCore.QRect(int(screen_w * 0.1500), int(screen_h * 0.7937), int(screen_w * 0.0750), int(screen_h * 0.0250)))
        self.order_input.setFont(font)
        self.sample_rate_input = QtWidgets.QLineEdit(self.centralwidget)
        self.sample_rate_input.setGeometry(QtCore.QRect(int(screen_w * 0.1500), int(screen_h * 0.8313), int(screen_w * 0.0750), int(screen_h * 0.0250)))
        self.sample_rate_input.setFont(font)
        self.cutoff_freq_input = QtWidgets.QLineEdit(self.centralwidget)
        self.cutoff_freq_input.setGeometry(QtCore.QRect(int(screen_w * 0.1500), int(screen_h * 0.8688), int(screen_w * 0.0750), int(screen_h * 0.0250)))
        self.cutoff_freq_input.setFont(font)
        self.order_label = QtWidgets.QLabel(self.centralwidget)
        self.order_label.setText("Order:")
        self.order_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.7937), int(screen_w * 0.1250), int(screen_h * 0.0250)))
        self.order_label.setFont(font)
        self.sample_rate_label = QtWidgets.QLabel(self.centralwidget)
        self.sample_rate_label.setText("Sample Rate:")
        self.sample_rate_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.8313), int(screen_w * 0.1250), int(screen_h * 0.0250)))
        self.sample_rate_label.setFont(font)
        self.cutoff_freq_label = QtWidgets.QLabel(self.centralwidget)
        self.cutoff_freq_label.setText("Cutoff Frequency:")
        self.cutoff_freq_label.setGeometry(QtCore.QRect(int(screen_w * 0.0125), int(screen_h * 0.8688), int(screen_w * 0.1250), int(screen_h * 0.0250)))
        self.cutoff_freq_label.setFont(font)
        self.cutoff_freq_label.hide()
        self.sample_rate_label.hide()
        self.order_label.hide()
        self.order_input.hide()
        self.cutoff_freq_input.hide()
        self.sample_rate_input.hide()
        self.low_label.hide()
        self.lowpass_checkbox.hide()
        self.high_label.hide()
        self.highpass_checkbox.hide()
        self.troubleshoot_button = QtWidgets.QPushButton(self.centralwidget)
        self.troubleshoot_button.setGeometry(QtCore.QRect(int(screen_w * 0.9000), int(screen_h * 0.1163), int(screen_w * 0.0938), int(screen_h * 0.0250)))
        self.troubleshoot_button.setText("Troubleshoot")
        self.load_defaults_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_defaults_button.setText("Load Defaults")
        self.load_defaults_button.setGeometry(QtCore.QRect(int(screen_w * 0.6500), int(screen_h * 0.7625), int(screen_w * 0.1250), int(screen_h * 0.0375)))
        font.setBold(True)
        self.load_defaults_button.setFont(font)
        font.setBold(False)
        self.cycles_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.cycles_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.7625), int(screen_h * 0.7000), int(screen_w * 0.1500), int(screen_h * 0.0250)))
        self.cycles_checkbox.setText("Plot Without Cycles")
        cycles_title = QtWidgets.QLabel(self.centralwidget)
        cycles_title.setFont(bold_font)
        cycles_title.setGeometry(QtCore.QRect(int(screen_w * 0.6500), int(screen_h * 0.5875), int(screen_w * 0.1875), int(screen_h * 0.0500)))
        cycles_title.setText("Cycles")
        cycles_blurb = QtWidgets.QLabel(self.centralwidget)
        cycles_blurb.setText("Would you like to apply thermal cycle recognition from ASMADA based off either Fluke or MTS data? MTS is chosen for single input unless overriden.")
        cycles_blurb.setFont(font)
        cycles_blurb.setGeometry(QtCore.QRect(int(screen_w * 0.7525), int(screen_h * 0.61000), int(screen_w * 0.1500), int(screen_h * 0.0250)))
        cycles_blurb.setWordWrap(True)
        self.fluke_cycle_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.fluke_cycle_checkbox.setText("Fluke")
        self.fluke_cycle_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.7125), int(screen_h * 0.6687), int(screen_w * 0.0938), int(screen_h * 0.0375)))
        self.mts_cycle_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.mts_cycle_checkbox.setText("MTS")
        self.mts_cycle_checkbox.setGeometry(QtCore.QRect(int(screen_w * 0.8750), int(screen_h * 0.6687), int(screen_w * 0.0938), int(screen_h * 0.0375)))
        self.mts_cycle_checkbox.setDisabled(True)
        self.fluke_cycle_checkbox.setDisabled(True)
        start_cycle_sep = QtWidgets.QFrame(self.centralwidget)
        start_cycle_sep.setGeometry(QtCore.QRect(int(screen_w * 0.6375), int(screen_h * 0.7188), int(screen_w * 0.3750), int(screen_h * 0.0250)))
        sep_font = QtGui.QFont()
        sep_font.setPointSize(8)
        sep_font.setBold(False)
        sep_font.setWeight(50)
        sep_font.setStrikeOut(False)
        start_cycle_sep.setFont(sep_font)
        start_cycle_sep.setFrameShadow(QtWidgets.QFrame.Plain)
        start_cycle_sep.setLineWidth(1)
        start_cycle_sep.setMidLineWidth(2)
        start_cycle_sep.setFrameShape(QtWidgets.QFrame.HLine)
        version_number = QtWidgets.QLabel(self.centralwidget)
        version_number.setText("Ver. 0.9.6.0")
        version_number.setGeometry(QtCore.QRect(int(screen_w * 0.95), int(screen_h * 0.9000), int(screen_w * 0.1250), int(screen_h * 0.0312)))



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #  FILE INPUT SECTION
        # button clicks
        self.mts_data_file_input_button.clicked.connect(self.browseMTSFile)
        self.fluke_data_file_input_button.clicked.connect(self.browseFlukeFile)
        # hiding and wrapping labels
        self.mts_data_file_display_label.setHidden(True)
        self.mts_data_file_display_label.setWordWrap(True)
        self.fluke_data_file_display_label.setHidden(True)
        self.fluke_data_file_display_label.setWordWrap(True)

        # TIME SYNC SECTION
        self.time_interval_line_edit.textChanged.connect(self.getTimeInfo)
        self.end_time_line_edit.textChanged.connect(self.getTimeInfo)
        self.start_time_line_edit.textChanged.connect(self.getTimeInfo)
        self.delay_line_edit.textChanged.connect(self.getTimeInfo)
        self.troubleshoot_button.clicked.connect(self.troubleshoot)

        # GLITCH CHECK SECTION
        self.glitch_check_dropdown.currentIndexChanged.connect(self.getGlitchCheck)

        # CROSS SECTION INFORMATION
        # hiding labels
        self.width_label.setHidden(True)
        self.width_input.setHidden(True)
        self.width_label.setWordWrap(True)
        self.measurement_input.setHidden(True)
        self.measurement_label.setHidden(True)
        # signals
        self.shape_dropdown.currentIndexChanged.connect(self.measurement_input.clear)
        self.shape_dropdown.currentIndexChanged.connect(self.width_input.clear)
        self.shape_dropdown.currentIndexChanged.connect(self.getCSect)
        self.input_unit_dropdown.currentIndexChanged.connect(self.getCSect)
        self.output_unit_dropdown.currentIndexChanged.connect(self.getCSect)
        self.measurement_input.textChanged.connect(self.getCSect)
        self.width_input.textChanged.connect(self.getCSect)


        # MOVING AVERAGE FILTER SECTION
        # hiding labels
        self.mts_temp_movavg_input.setHidden(True)
        self.mts_temp_movavg_label.setHidden(True)
        self.fluke_temp_movavg_label.setHidden(True)
        self.fluke_temp_movavg_input.setHidden(True)
        self.disp_movavg_label.setHidden(True)
        self.disp_movavg_input.setHidden(True)
        self.load_movavg_label.setHidden(True)
        self.load_movavg_input.setHidden(True)
        # signals
        self.temp_movavg_checkbox.stateChanged.connect(self.getMovAvgInfo)
        self.disp_movavg_checkbox.stateChanged.connect(self.getMovAvgInfo)
        self.load_movavg_checkbox.stateChanged.connect(self.getMovAvgInfo)
        self.none_movavg_checkbox.stateChanged.connect(self.getMovAvgInfo)
        self.mts_temp_movavg_input.textChanged.connect(self.getMovAvgInfo)
        self.fluke_temp_movavg_input.textChanged.connect(self.getMovAvgInfo)
        self.disp_movavg_input.textChanged.connect(self.getMovAvgInfo)
        self.load_movavg_input.textChanged.connect(self.getMovAvgInfo)


        # MTS DATA SELECTION SECTION
        self.mts_temp_select_dropdown.currentIndexChanged.connect(self.getMTSSelections)
        self.disp_dropdown.currentIndexChanged.connect(self.getMTSSelections)


        # START SECTION
        self.start_button.clicked.connect(self.startAnalysis)
        self.load_defaults_button.clicked.connect(self.loadDefaults)


        # CYCLES SECTION
        self.cycles_checkbox.stateChanged.connect(self.checkCycles)
        self.mts_cycle_checkbox.stateChanged.connect(self.getCycleDeterminer)
        self.fluke_cycle_checkbox.stateChanged.connect(self.getCycleDeterminer)
        


        # FLUKE DATA
        self.fluke_temp_dropdown.currentIndexChanged.connect(self.getFlukeTemp)


        # STRAIN SECTION (BANDPASS AND LENGTH)
        self.length_line_edit.textChanged.connect(self.getLength)
        self.bandpass_yes_checkbox.stateChanged.connect(self.checkBandpass)
        self.bandpass_no_checkbox.stateChanged.connect(self.checkBandpass)
        self.order_input.textChanged.connect(self.getBandpass)
        self.sample_rate_input.textChanged.connect(self.getBandpass)
        self.cutoff_freq_input.textChanged.connect(self.getBandpass)
        self.lowpass_checkbox.stateChanged.connect(self.getBandpass)
        self.highpass_checkbox.stateChanged.connect(self.getBandpass)


        # DSC
        self.num_cycle_input.textChanged.connect(self.getDSCSteps)
        self.num_cycle_input2.textChanged.connect(self.getDSCSteps)
        self.dsc_data_button.clicked.connect(self.getDSC)
        self.steps_button.clicked.connect(self.showDSCSteps)
        self.dsc_movavg_yes_checkbox.stateChanged.connect(self.showDSCMovAvg)
        self.dsc_movavg_no_checkbox.stateChanged.connect(self.showDSCMovAvg)
        self.x_movavg_input.textChanged.connect(self.getDSCMovAvg)
        self.y_movavg_input.textChanged.connect(self.getDSCMovAvg)
        self.x_axis_combobox.currentIndexChanged.connect(self.getDSCAxes)
        self.y_axis_combobox.currentIndexChanged.connect(self.getDSCAxes)


        # clear buttons
        self.clear_all_button.clicked.connect(self.clearAll)
        self.clear_csect_button.clicked.connect(self.clearCrossSection)
        self.clear_movavg_button.clicked.connect(self.clearMovAvg)
        self.clear_dsc_button.clicked.connect(self.clearDSC)
        


        # DICTIONARY FOR ALL DATA
        self.all_data = {}
        self.dsc_data = {}


        # INITIAL CONDITION CHECK
        self.checkCycles()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SMA Analysis"))
        self.mts_data_file_input_button.setText(_translate("MainWindow", "Browse File"))
        self.file_input_label.setText(_translate("MainWindow", "File Input"))
        self.mts_data_input_label.setText(_translate("MainWindow", "MTS Data:"))
        self.mts_data_file_display_label.setText(_translate("MainWindow", "MTS_DATA.txt"))
        self.fluke_data_input_label.setText(_translate("MainWindow", "Fluke Data:"))
        self.fluke_data_file_input_button.setText(_translate("MainWindow", "Browse File"))
        self.fluke_data_file_display_label.setText(_translate("MainWindow", "FLUKE_DATA.csv"))
        self.optional_label_file.setText(_translate("MainWindow", "(Optional)"))
        self.time_sync_label.setText(_translate("MainWindow", "Time Synchronization"))
        self.time_interval_label.setText(_translate("MainWindow", "MTS Absolute Start (HH:MM:SS):\nMatch Fluke If Unsure"))
        self.end_time_label.setText(_translate("MainWindow", "End Count (s):"))
        self.glitch_text_text.setText(_translate("MainWindow", "Would you like to delete all spurious zeroes? (features to be expanded upon)"))
        self.glitch_check_label.setText(_translate("MainWindow", "Data Spike Remover"))
        self.glitch_check_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.glitch_check_dropdown.setItemText(1, _translate("MainWindow", "Yes"))
        self.glitch_check_dropdown.setItemText(2, _translate("MainWindow", "No"))
        self.mts_data_selection_label.setText(_translate("MainWindow", "MTS Data Selection"))
        self.mts_temp_select_label.setText(_translate("MainWindow", "Temperature:"))
        self.mts_temp_select_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.disp_label.setText(_translate("MainWindow", "Displacement:"))
        self.disp_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.fluke_data_select_label.setText(_translate("MainWindow", "Fluke Data Selection"))
        self.fluke_temp_label.setText(_translate("MainWindow", "Temperature:"))
        self.fluke_temp_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.fluke_temp_blurb.setText(_translate("MainWindow", "(Not needed if there is no fluke data to analyze.)"))
        self.cross_section_label.setText(_translate("MainWindow", "Cross Section Information"))
        self.shape_label.setText(_translate("MainWindow", "Shape:"))
        self.shape_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.shape_dropdown.setItemText(1, _translate("MainWindow", "Circle"))
        self.shape_dropdown.setItemText(2, _translate("MainWindow", "Square"))
        self.shape_dropdown.setItemText(3, _translate("MainWindow", "Rectangle"))
        self.shape_dropdown.setItemText(4, _translate("MainWindow", "Cintraquad"))
        self.input_unit_label.setText(_translate("MainWindow", "Input Unit:"))
        self.input_unit_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.input_unit_dropdown.setItemText(1, _translate("MainWindow", "in"))
        self.input_unit_dropdown.setItemText(2, _translate("MainWindow", "mm"))
        self.input_unit_dropdown.setItemText(3, _translate("MainWindow", "m"))
        self.output_unit_label.setText(_translate("MainWindow", "Output Unit:"))
        self.output_unit_dropdown.setItemText(0, _translate("MainWindow", "Select..."))
        self.output_unit_dropdown.setItemText(1, _translate("MainWindow", "in"))
        self.output_unit_dropdown.setItemText(2, _translate("MainWindow", "mm"))
        self.output_unit_dropdown.setItemText(3, _translate("MainWindow", "m"))
        self.measurement_label.setText(_translate("MainWindow", "Side Length:"))
        self.width_label.setText(_translate("MainWindow", "Width:"))
        self.movavg_label.setText(_translate("MainWindow", "Moving Average Filter"))
        self.movavg_blurb.setText(_translate("MainWindow", "A moving average filter can be applied to temperature, load, or displacement. Would you like to apply a moving average filter to any or all of these measurements?"))
        self.mts_temp_movavg_label.setText(_translate("MainWindow", "Number of datapoints for MTS temperature moving average:"))
        self.load_movavg_label.setText(_translate("MainWindow", "Number of datapoints for load moving average:"))
        self.fluke_temp_movavg_label.setText(_translate("MainWindow", "Number of datapoints for Fluke temperature moving average:"))
        self.disp_movavg_label.setText(_translate("MainWindow", "Number of datapoints for displacement moving average:"))
        self.start_button.setText(_translate("MainWindow", "Start Analysis"))
        self.temp_movavg_checkbox.setText(_translate("MainWindow", "Temperature"))
        self.disp_movavg_checkbox.setText(_translate("MainWindow", "Displacement"))
        self.load_movavg_checkbox.setText(_translate("MainWindow", "Load"))
        self.none_movavg_checkbox.setText(_translate("MainWindow", "None"))


    # file input for mts data file
    def browseMTSFile(self):
        fileloc = QFileDialog.getOpenFileName(None, "Open MTS Data File", "", "All Files(*);;Text Files(*.txt);;CSV Files(*.csv);;Excel Files(*.xlsx)")
        if fileloc:
            mtsloc = str(fileloc[0])
            filename = mtsloc[mtsloc.rindex("/") + 1:]
            self.mts_data_file_display_label.setText(filename)
            self.mts_data_file_display_label.show()
            mts = reader(mtsloc)
            mts.extract()
            mts_data = mts.dataframe.copy()
            self.mts_temp_select_dropdown.clear()
            self.mts_temp_select_dropdown.addItem("Select...")
            self.disp_dropdown.clear()
            self.disp_dropdown.addItem("Select...")
            for col in mts_data.columns.tolist():
                self.mts_temp_select_dropdown.addItem(col)
                self.disp_dropdown.addItem(col)
            self.all_data["MTS File Name"] = mtsloc
            self.end_time_line_edit.setText(str(mts_data[mts_data.columns.tolist()[0]].tolist()[-1]))
            self.default_end_time_label.show()


    # file input for fluke data file
    def browseFlukeFile(self):
        fileloc = QFileDialog.getOpenFileName(None, "Open MTS Data File", "", "All Files(*);;Text Files(*.txt);;CSV Files(*.csv);;Excel Files(*.xlsx)")
        if fileloc:
            flukeloc = str(fileloc[0])
            filename = flukeloc[flukeloc.rindex("/") + 1:]
            self.fluke_data_file_display_label.setText(filename)
            self.fluke_data_file_display_label.show()
            # self.all_data["Fluke File Name"] = flukeloc
            # self.displayFlukeHeaders()
            fluke = reader(flukeloc)
            fluke.extract_fluke()
            self.all_data["Fluke"] = flukeloc
            self.resetComboBox(self.fluke_temp_dropdown)
            for label in fluke.dataframe.columns:
                self.fluke_temp_dropdown.addItem(label)
            self.delay_line_edit.setEnabled(True)
            self.mts_cycle_checkbox.setEnabled(True)
            self.fluke_cycle_checkbox.setEnabled(True)
            self.time_interval_line_edit.setEnabled(True)
            self.fluke_temp_dropdown.setEnabled(True)
            if (self.delay_line_edit.text() == ""):
                self.default_delay_label.show()
                self.delay_line_edit.setText("0")
            self.none_movavg_checkbox.setChecked(True)


    def getDSC(self):
        fileloc = QFileDialog.getOpenFileName(None, "Open MTS Data File", "", "All Files(*);;Text Files(*.txt);;CSV Files(*.csv);;Excel Files(*.xlsx)")
        if fileloc:
            dscloc = str(fileloc[0])
            filename = dscloc[dscloc.rindex("/") + 1:]
            self.dsc_data_display_label.setText(filename)
            self.dsc_data_display_label.show()
            self.dsc_data["DSC File Name"] = dscloc
            dsc = reader(dscloc)
            steps = dsc.extract_DSC()
            self.x_axis_combobox.clear()
            self.y_axis_combobox.clear()
            self.x_axis_combobox.addItem("Select...")
            self.y_axis_combobox.addItem("Select...")
            self.num_cycle_input.setText(str(min(dsc.dataframe["Step"])))
            self.num_cycle_input2.setText(str(max(dsc.dataframe["Step"])))
            for column in dsc.dataframe.columns:
                self.x_axis_combobox.addItem(column)
                self.y_axis_combobox.addItem(column)


    def getDSCSteps(self):
        try:
            self.dsc_data["DSC Step Initial"] = int(self.num_cycle_input.text())
        except:
            self.num_cycle_input.setText(self.num_cycle_input.text()[:-1])
        try:
            self.dsc_data["DSC Step Final"] = int(self.num_cycle_input2.text())
        except:
            self.num_cycle_input2.setText(self.num_cycle_input2.text()[:-1])


    def showDSCSteps(self):
        try:
            dsc = reader(self.dsc_data["DSC File Name"])
            steps = dsc.extract_DSC()
            QMessageBox.about(MainWindow, "Steps", steps)
        except KeyError:
            error = QtWidgets.QMessageBox(self.centralwidget)
            error.setIcon(QMessageBox.Critical)
            error.setText("Please input a file first")
            error.setWindowTitle("Error")
            error.show()


    def showDSCMovAvg(self):
        self.dsc_movavg_no_checkbox.setEnabled(True)
        self.dsc_movavg_yes_checkbox.setEnabled(True)
        self.x_axis_movavg_label.hide()
        self.y_axis_movavg_label.hide()
        self.x_movavg_input.hide()
        self.y_movavg_input.hide()
        if self.dsc_movavg_yes_checkbox.isChecked():
            self.x_axis_movavg_label.show()
            self.y_axis_movavg_label.show()
            self.x_movavg_input.show()
            self.y_movavg_input.show()
            self.dsc_movavg_no_checkbox.setEnabled(False)
            self.dsc_data["DSC Filter Choice"] = True
        if self.dsc_movavg_no_checkbox.isChecked():
            self.dsc_movavg_yes_checkbox.setEnabled(False)
            self.dsc_data["DSC Filter Choice"] = False


    def getDSCMovAvg(self):
        try:
            self.dsc_data["DSC x_movavg"] = int(self.x_movavg_input.text())
        except:
            self.x_movavg_input.setText(self.x_movavg_input.text()[:-1])
        try:
            self.dsc_data["DSC y_movavg"] = int(self.y_movavg_input.text())
        except:
            self.y_movavg_input.setText(self.y_movavg_input.text()[:-1])


    def getDSCAxes(self):
        self.dsc_data["DSC X"] = self.x_axis_combobox.currentText()
        self.dsc_data["DSC Y"] = self.y_axis_combobox.currentText()


    def getFlukeTemp(self):
        self.all_data["Fluke Temperature Title"] = self.fluke_temp_dropdown.currentText()


    # get time interval and end time
    def getTimeInfo(self):
        time_data = {}
        interval = self.time_interval_line_edit.text()# is this is MTS start time in HH:MM:SS??
        time_data["Interval"] = interval
        start_time = self.start_time_line_edit.text()
        end_time = self.end_time_line_edit.text()
        # try:
        #     if len(interval) > 0:
        #         time_data["Interval"] = float(interval)
        # except:
        #     self.time_interval_line_edit.setText(interval[:-1])
        if self.end_time_line_edit.isModified():
            self.default_end_time_label.hide()
        try:
            if len(end_time) > 0:
                time_data["End Time"] = float(end_time)
        except:
            self.end_time_line_edit.setText(end_time[:-1])
        if self.start_time_line_edit.isModified():
            self.default_start_time_label.hide()
        try:
            if len(start_time) > 0:
                time_data["Start Time"] = float(start_time)
        except:
            self.start_time_line_edit.setText(start_time[:-1])
        if self.delay_line_edit.isModified():
            self.default_delay_label.hide()
        if self.delay_line_edit.isEnabled():
            try:
                time_data["Delay"] = float(self.delay_line_edit.text())
            except:
                self.delay_line_edit.setText(self.delay_line_edit.text()[:-1])
        self.all_data["Time Data"] = time_data


    # get glitch check info
    def getGlitchCheck(self):
        choice = self.glitch_check_dropdown.currentText()
        self.all_data["Glitch"] = choice


    # get cross section information
    def getCSect(self):
        shape = self.shape_dropdown.currentText()
        input_unit = self.input_unit_dropdown.currentText()
        output_unit = self.output_unit_dropdown.currentText()
        csect_info = {"Shape": shape, "Input Unit": input_unit, "Output Unit": output_unit}
        if shape == "Circle":
            self.clearShapes()
            self.circle_img.show()
            self.measurement_label.setText("Diameter:")
            self.measurement_input.show()
            self.measurement_label.show()
            self.width_label.setHidden(True)
            self.width_input.setHidden(True)
            diameter = self.measurement_input.text()
            if len(diameter) > 0:
                csect_info["Measurement1"] = float(diameter)
                self.all_data["Shape"] = shape
                self.all_data["Output Unit"] = output_unit
                self.all_data["Area"] = Geometry_input(shape, input_unit, output_unit, csect_info["Measurement1"])
        elif shape == "Rectangle":
            self.clearShapes()
            self.rectangle_img.show()
            self.measurement_input.show()
            self.measurement_label.show()
            self.measurement_label.setText("Length:")
            self.width_label.setText("Width:")
            self.width_label.show()
            self.width_input.show()
            length = self.measurement_input.text()
            width = self.width_input.text()
            if len(length) > 0 and len(width) > 0:
                csect_info["Measurement1"] = float(length)
                csect_info["Measurement2"] = float(width)
                self.all_data["Shape"] = shape
                self.all_data["Output Unit"] = output_unit
                self.all_data["Area"] = Geometry_input(shape, input_unit, output_unit, csect_info["Measurement1"], csect_info["Measurement2"])
        elif shape == "Square":
            self.clearShapes()
            self.square_img.show()
            self.measurement_input.show()
            self.measurement_label.show()
            self.measurement_label.setText("Side Length:")
            self.width_label.setHidden(True)
            self.width_input.setHidden(True)
            side = self.measurement_input.text()
            if len(side) > 0:
                csect_info["Measurement1"] = float(side)
                self.all_data["Shape"] = shape
                self.all_data["Output Unit"] = output_unit
                self.all_data["Area"] = Geometry_input(shape, input_unit, output_unit, csect_info["Measurement1"])
        elif shape == "Cintraquad":
            self.clearShapes()
            self.circle_in_square_img.show()
            self.measurement_input.show()
            self.measurement_label.show()
            self.width_label.show()
            self.width_input.show()
            self.measurement_label.setText("Side Length:")
            self.width_label.setText("Hole Diameter:")
            side = self.measurement_input.text()
            diameter = self.width_input.text()
            if len(side) > 0 and len(diameter) > 0:
                csect_info["Measurement1"] = side
                csect_info["Measurement2"] = diameter
                self.all_data["Shape"] = shape
                self.all_data["Output Unit"] = output_unit
                self.all_data["Area"] = Geometry_input(shape, input_unit, output_unit, csect_info["Measurement1"], csect_info["Measurement2"])
        elif shape == "Custom":
            self.clearShapes()
            self.custom_img.show()
            self.measurement_input.show()
            self.measurement_label.show()
            self.measurement_label.setText("Area:")
            self.width_label.setHidden(True)
            self.width_input.setHidden(True)
            try:
                csect_info["Measurement1"] = float(self.measurement_input.text())
                self.all_data["Shape"] = shape
                self.all_data["Output Unit"] = output_unit
                self.all_data["Area"] = Geometry_input(shape, input_unit, output_unit, csect_info["Measurement1"])
            except:
                self.measurement_input.setText(self.measurement_input.text()[:-1])
        self.all_data["Cross Section Info"] = csect_info



    def getMovAvgInfo(self):
        self.temp_movavg_checkbox.setEnabled(True)
        self.disp_movavg_checkbox.setEnabled(True)
        self.load_movavg_checkbox.setEnabled(True)
        movavg_conditions = set()
        movavg_datapoints = {}
        movavg_data = {"Conditions": movavg_conditions, "Datapoints": movavg_datapoints}
        if self.none_movavg_checkbox.isChecked():
            movavg_conditions.clear()
            self.mts_temp_movavg_input.setHidden(True)
            self.mts_temp_movavg_label.setHidden(True)
            self.fluke_temp_movavg_label.setHidden(True)
            self.fluke_temp_movavg_input.setHidden(True)
            self.disp_movavg_label.setHidden(True)
            self.disp_movavg_input.setHidden(True)
            self.load_movavg_label.setHidden(True)
            self.load_movavg_input.setHidden(True)
            self.temp_movavg_checkbox.setEnabled(False)
            self.disp_movavg_checkbox.setEnabled(False)
            self.load_movavg_checkbox.setEnabled(False)
            self.temp_movavg_checkbox.setCheckState(False)
            self.disp_movavg_checkbox.setCheckState(False)
            self.load_movavg_checkbox.setCheckState(False)
            self.mts_temp_movavg_input.clear()
            self.fluke_temp_movavg_input.clear()
            self.disp_movavg_input.clear()
            self.load_movavg_input.clear()
            movavg_conditions.add("none")
        else:
            if self.temp_movavg_checkbox.isChecked() and self.disp_movavg_checkbox.isChecked() and self.load_movavg_checkbox.isChecked():
                movavg_conditions.add("all")
                self.mts_temp_movavg_input.show()
                self.mts_temp_movavg_label.show()
                if self.fluke_data_file_display_label.text() != "FLUKE_DATA.csv":
                    self.fluke_temp_movavg_input.show()
                    self.fluke_temp_movavg_label.show()
                self.disp_movavg_input.show()
                self.disp_movavg_label.show()
                self.load_movavg_input.show()
                self.load_movavg_label.show()
                try:
                    movavg_datapoints["MTS Temperature"] = int(self.mts_temp_movavg_input.text())
                except:
                    self.mts_temp_movavg_input.setText(self.mts_temp_movavg_input.text()[:-1])
                try:
                    movavg_datapoints["Fluke Temperature"] = int(self.fluke_temp_movavg_input.text())
                except:
                    self.fluke_temp_movavg_input.setText(self.fluke_temp_movavg_input.text()[:-1])
                try:
                    movavg_datapoints["Displacement"] = int(self.disp_movavg_input.text())
                except:
                    self.disp_movavg_input.setText(self.disp_movavg_input.text()[:-1])
                try:
                    movavg_datapoints["Load"] = int(self.load_movavg_input.text())
                except:
                    self.load_movavg_input.setText(self.load_movavg_input.text()[:-1])
            else:
                if self.temp_movavg_checkbox.isChecked():
                    movavg_conditions.add("temperature")
                    self.mts_temp_movavg_input.show()
                    self.mts_temp_movavg_label.show()
                    if self.fluke_data_file_display_label.text() != "FLUKE_DATA.csv":
                        self.fluke_temp_movavg_input.show()
                        self.fluke_temp_movavg_label.show()
                    try:
                        movavg_datapoints["MTS Temperature"] = int(self.mts_temp_movavg_input.text())
                    except:
                        self.mts_temp_movavg_input.setText(self.mts_temp_movavg_input.text()[:-1])
                    try:
                        movavg_datapoints["Fluke Temperature"] = int(self.fluke_temp_movavg_input.text())
                    except:
                        self.fluke_temp_movavg_input.setText(self.fluke_temp_movavg_input.text()[:-1])
                else:
                    self.mts_temp_movavg_input.setHidden(True)
                    self.mts_temp_movavg_label.setHidden(True)
                    self.fluke_temp_movavg_input.setHidden(True)
                    self.fluke_temp_movavg_label.setHidden(True)
                    self.mts_temp_movavg_input.clear()
                    self.fluke_temp_movavg_input.clear()
                if self.disp_movavg_checkbox.isChecked():
                    movavg_conditions.add("displacement")
                    self.disp_movavg_input.show()
                    self.disp_movavg_label.show()
                    try:
                        movavg_datapoints["Displacement"] = int(self.disp_movavg_input.text())
                    except:
                        self.disp_movavg_input.setText(self.disp_movavg_input.text()[:-1])
                else:
                    self.disp_movavg_input.setHidden(True)
                    self.disp_movavg_label.setHidden(True)
                    self.disp_movavg_input.clear()
                if self.load_movavg_checkbox.isChecked():
                    movavg_conditions.add("load")
                    self.load_movavg_input.show()
                    self.load_movavg_label.show()
                    try:
                        movavg_datapoints["Load"] = int(self.load_movavg_input.text())
                    except:
                        self.load_movavg_input.setText(self.load_movavg_input.text()[:-1])
                else:
                    self.load_movavg_input.setHidden(True)
                    self.load_movavg_label.setHidden(True)
                    self.load_movavg_input.clear()
        self.all_data["Moving Average Data"] = movavg_data



    def getMTSSelections(self):
        mts_temp_header = self.mts_temp_select_dropdown.currentText()
        mts_disp_header = self.disp_dropdown.currentText()
        mts_data = {"Temp Header": mts_temp_header, "Disp Header": mts_disp_header}
        self.all_data["MTS Data"] = mts_data


    def startAnalysis(self):
        # try:
        if self.dsc_data_display_label.text() != "DSC_DATA":
            if self.dsc_movavg_yes_checkbox.isChecked():
                dsc_fig = plotDSC(self.dsc_data["DSC File Name"], self.dsc_data["DSC Step Initial"], self.dsc_data["DSC Step Final"], self.dsc_data["DSC X"],
                              self.dsc_data["DSC Y"], self.dsc_data["DSC Filter Choice"], self.dsc_data["DSC x_movavg"], self.dsc_data["DSC y_movavg"])
            else:
                dsc_fig = plotDSC(self.dsc_data["DSC File Name"], self.dsc_data["DSC Step Initial"],
                                  self.dsc_data["DSC Step Final"], self.dsc_data["DSC X"],
                                  self.dsc_data["DSC Y"], self.dsc_data["DSC Filter Choice"])

            self.dsc_window = AnotherWindow(dsc_fig, "DSC Data")
            self.dsc_window.show()
        if self.fluke_data_file_display_label.text() == "FLUKE_DATA.csv" and self.mts_data_file_display_label.text() != "MTS_DATA.txt":
            plots, colorbar_error, cycle_error = analyze_mts(self.all_data["MTS File Name"], self.all_data["Time Data"]["End Time"], self.all_data["Time Data"]["Start Time"], self.all_data["Glitch"],
                        self.all_data["MTS Data"]["Temp Header"], self.all_data["MTS Data"]["Disp Header"], self.all_data["Shape"], self.all_data["Output Unit"],
                        self.all_data["Area"], self.all_data["Moving Average Data"]["Conditions"], self.all_data["Moving Average Data"]["Datapoints"], self.all_data["Length"],
                                                             {}, self.all_data["No Cycles"])
            self.temp_vs_strain_plot = AnotherWindow(plots[0], "Temperature vs. Strain")
            self.temp_vs_stress_vs_strain_plot = AnotherWindow(plots[1], "Temperature vs. Stress vs. Strain")
            self.temp_vs_strain_plot.show()
            self.temp_vs_stress_vs_strain_plot.show()
            if (len(plots) == 3):
                self.mts_mov_avg_plot = AnotherWindow(plots[2], "MTS Moving Average Plots")
                self.mts_mov_avg_plot.show()
            if colorbar_error or cycle_error:
                error = QtWidgets.QMessageBox(self.centralwidget)
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle("Some features did not work")
                error_msg = ''
                if colorbar_error:
                    error_msg += 'The colorbar failed so it was disabled.\n'
                if cycle_error:
                    error_msg += 'Cycle detection failed so it was disabled'
                error.setText(error_msg)
                error.show()
        elif self.fluke_data_file_display_label.text() != "FLUKE_DATA.csv" and self.mts_data_file_display_label.text() != "MTS_DATA.txt":
            plots, colorbar_error, cycle_error = analyze_fmts(mts_temp_title=self.all_data["MTS Data"]["Temp Header"],
                                 fluke_temp_title=self.all_data["Fluke Temperature Title"],
                                 disp_title=self.all_data["MTS Data"]["Disp Header"], area=self.all_data["Area"],
                                 area_unit=self.all_data["Output Unit"], orig_length=self.all_data["Length"],
                                 mov_avg_set=self.all_data["Moving Average Data"]["Conditions"],
                                 datapoints=self.all_data["Moving Average Data"]["Datapoints"],
                                 bandpass={},
                                 mts_start_time=self.all_data["Time Data"]["Interval"],
                                 no_cycles=self.all_data["No Cycles"], glitch_check=self.all_data["Glitch"],
                                 cycle_determiner=self.all_data["Cycle Determiner"],
                                 relative_start_time=self.all_data["Time Data"]["Start Time"],
                                 relative_end_time=self.all_data["Time Data"]["End Time"],
                                 mts_file_name=self.all_data["MTS File Name"], fluke_file_name=self.all_data["Fluke"])
            self.temp_vs_strain_plot = AnotherWindow(plots[0], "Temperature vs. Strain")
            self.temp_vs_stress_vs_strain_plot = AnotherWindow(plots[1], "Temperature vs. Stress vs. Strain")
            self.temp_vs_strain_plot.show()
            self.temp_vs_stress_vs_strain_plot.show()
            if (len(plots) == 4):
                self.mts_mov_avg_plot = AnotherWindow(plots[2], "MTS Moving Average Plots")
                self.fluke_mov_avg_plot = AnotherWindow(plots[3], "Fluke Moving Average Plots")
                self.mts_mov_avg_plot.show()
                self.fluke_mov_avg_plot.show()
            if colorbar_error or cycle_error:
                error = QtWidgets.QMessageBox(self.centralwidget)
                error.setIcon(QMessageBox.Warning)
                error.setWindowTitle("Some features did not work")
                error_msg = ''
                if colorbar_error:
                    error_msg += 'The colorbar failed so it was disabled.\n'
                if cycle_error:
                    error_msg += 'Cycle detection failed so it was disabled'
                error.setText(error_msg)
                error.show()
        # except KeyError:
        #     error = QtWidgets.QMessageBox(self.centralwidget)
        #     error.setIcon(QMessageBox.Critical)
        #     error.setText("One or more inputs have been left blank.\nPlease enter all required data and try again.")
        #     error.setWindowTitle("Error")
        #     error.show()


    def clearShapes(self):
        self.circle_in_square_img.hide()
        self.square_img.hide()
        self.circle_img.hide()
        self.rectangle_img.hide()
        self.custom_img.hide()

    def resetComboBox(self, combo_box):
        for i in range(1, combo_box.count()):
            combo_box.removeItem(i)


    def getLength(self):
        try:
            self.all_data["Length"] = float(self.length_line_edit.text())
        except:
            self.length_line_edit.setText(self.length_line_edit.text()[:-1])


    def checkBandpass(self):
        try:
            del self.all_data["Bandpass"]
        except:
            pass
        self.bandpass_yes_checkbox.setEnabled(True)
        self.bandpass_no_checkbox.setEnabled(True)
        self.cutoff_freq_label.hide()
        self.sample_rate_label.hide()
        self.order_label.hide()
        self.order_input.hide()
        self.cutoff_freq_input.hide()
        self.sample_rate_input.hide()
        self.low_label.hide()
        self.lowpass_checkbox.hide()
        self.high_label.hide()
        self.highpass_checkbox.hide()
        self.all_data["Bandpass"] = {}
        if self.bandpass_yes_checkbox.isChecked():
            self.bandpass_no_checkbox.setEnabled(False)
            self.low_label.show()
            self.high_label.show()
            self.lowpass_checkbox.show()
            self.highpass_checkbox.show()
            self.order_label.show()
            self.order_input.show()
            self.sample_rate_label.show()
            self.sample_rate_input.show()
            self.cutoff_freq_label.show()
            self.cutoff_freq_input.show()
            self.all_data["Bandpass"]["Choice"] = True
            try:
                self.sample_rate_input.setText(str(1/self.all_data["Time Data"]["Interval"]))
            except:
                pass
        elif self.bandpass_no_checkbox.isChecked():
            self.bandpass_yes_checkbox.setEnabled(False)
            self.all_data["Bandpass"]["Choice"] = False


    def getBandpass(self):
        self.lowpass_checkbox.setEnabled(True)
        self.highpass_checkbox.setEnabled(True)
        if self.lowpass_checkbox.isChecked():
            self.highpass_checkbox.setDisabled(True)
            self.all_data["Bandpass"]["Type"] = "low"
        elif self.highpass_checkbox.isChecked():
            self.all_data["Bandpass"]["Type"] = "high"
            self.lowpass_checkbox.setDisabled(True)
        try:
            self.all_data["Bandpass"]["Order"] = int(self.order_input.text())
        except:
            self.order_input.setText(self.order_input.text()[:-1])
        try:
            self.all_data["Bandpass"]["Sample Rate"] = float(self.sample_rate_input.text())
        except:
            self.sample_rate_input.setText(self.sample_rate_input.text()[:-1])
        try:
            self.all_data["Bandpass"]["Cutoff Frequency"] = float(self.cutoff_freq_input.text())
        except:
            self.cutoff_freq_input.setText(self.cutoff_freq_input.text()[:-1])


    def clearAll(self):
        self.all_data.clear()
        self.dsc_data.clear()
        # file input
        self.mts_data_file_display_label.setText("MTS_DATA.txt")
        self.mts_data_file_display_label.hide()
        self.fluke_data_file_display_label.setText("FLUKE_DATA.csv")
        self.fluke_data_file_display_label.hide()

        # time info
        self.start_time_line_edit.setText("0")
        self.end_time_line_edit.setText("")
        self.time_interval_line_edit.setText("")
        self.default_end_time_label.hide()
        self.default_start_time_label.hide()
        self.delay_line_edit.setText("0")

        # glitch check
        self.glitch_check_dropdown.setCurrentIndex(0)

        # mts/fluke data select
        self.resetComboBox(self.mts_temp_select_dropdown)
        self.resetComboBox(self.fluke_temp_dropdown)
        self.resetComboBox(self.disp_dropdown)

        # cross section
        self.shape_dropdown.setCurrentIndex(0)
        self.input_unit_dropdown.setCurrentIndex(0)
        self.output_unit_dropdown.setCurrentIndex(0)
        self.measurement_input.setText("")
        self.measurement_input.hide()
        self.measurement_label.hide()
        self.width_label.hide()
        self.width_input.setText("")
        self.width_input.hide()
        self.clearShapes()

        # moving average
        self.temp_movavg_checkbox.setCheckState(False)
        self.disp_movavg_checkbox.setCheckState(False)
        self.load_movavg_checkbox.setCheckState(False)
        self.none_movavg_checkbox.setCheckState(False)
        self.mts_temp_movavg_input.setText("")
        self.mts_temp_movavg_input.hide()
        self.mts_temp_movavg_label.hide()
        self.fluke_temp_movavg_input.setText("")
        self.fluke_temp_movavg_input.hide()
        self.fluke_temp_movavg_label.hide()
        self.disp_movavg_input.setText("")
        self.disp_movavg_input.hide()
        self.disp_movavg_label.hide()
        self.load_movavg_input.setText("")
        self.load_movavg_input.hide()
        self.load_movavg_label.hide()

        # strain
        self.length_line_edit.setText("")

        # dsc
        self.dsc_data_display_label.setText("DSC_DATA")
        self.dsc_data_display_label.hide()
        self.num_cycle_input.setText("")
        self.num_cycle_input2.setText("")
        self.dsc_movavg_no_checkbox.setCheckState(False)
        self.dsc_movavg_yes_checkbox.setCheckState(False)
        self.x_movavg_input.setText("")
        self.x_movavg_input.hide()
        self.x_axis_movavg_label.hide()
        self.y_movavg_input.setText("")
        self.y_movavg_input.hide()
        self.y_axis_movavg_label.hide()
        self.resetComboBox(self.x_axis_combobox)
        self.resetComboBox(self.y_axis_combobox)
        


    def clearCrossSection(self):
        del self.all_data["Cross Section Info"]
        self.shape_dropdown.setCurrentIndex(0)
        self.input_unit_dropdown.setCurrentIndex(0)
        self.output_unit_dropdown.setCurrentIndex(0)
        self.measurement_input.setText("")
        self.measurement_input.hide()
        self.measurement_label.hide()
        self.width_label.hide()
        self.width_input.setText("")
        self.width_input.hide()


    def clearMovAvg(self):
        del self.all_data["Moving Average Data"]
        self.temp_movavg_checkbox.setCheckState(False)
        self.disp_movavg_checkbox.setCheckState(False)
        self.load_movavg_checkbox.setCheckState(False)
        self.none_movavg_checkbox.setCheckState(False)
        self.mts_temp_movavg_input.setText("")
        self.mts_temp_movavg_input.hide()
        self.mts_temp_movavg_label.hide()
        self.fluke_temp_movavg_input.setText("")
        self.fluke_temp_movavg_input.hide()
        self.fluke_temp_movavg_label.hide()
        self.disp_movavg_input.setText("")
        self.disp_movavg_input.hide()
        self.disp_movavg_label.hide()
        self.load_movavg_input.setText("")
        self.load_movavg_input.hide()
        self.load_movavg_label.hide()


    def clearDSC(self):
        self.dsc_data_display_label.setText("DSC_DATA")
        self.dsc_data_display_label.hide()
        self.num_cycle_input.setText("")
        self.num_cycle_input2.setText("")
        self.dsc_movavg_no_checkbox.setCheckState(False)
        self.dsc_movavg_yes_checkbox.setCheckState(False)
        self.x_movavg_input.setText("")
        self.x_movavg_input.hide()
        self.x_axis_movavg_label.hide()
        self.y_movavg_input.setText("")
        self.y_movavg_input.hide()
        self.y_axis_movavg_label.hide()
        self.resetComboBox(self.x_axis_combobox)
        self.resetComboBox(self.y_axis_combobox)
        self.dsc_data.clear()


    def loadDefaults(self):
        self.none_movavg_checkbox.setChecked(True)
        self.bandpass_no_checkbox.setChecked(True)
        self.shape_dropdown.setCurrentIndex(1)
        self.input_unit_dropdown.setCurrentIndex(2)
        self.output_unit_dropdown.setCurrentIndex(2)
        self.measurement_input.setText("10")
        self.length_line_edit.setText("10")
        self.glitch_check_dropdown.setCurrentIndex(2)
        if self.fluke_data_file_display_label.text() != "FLUKE_DATA.csv":
            self.fluke_cycle_checkbox.setChecked(True)


    def troubleshoot(self):
        self.troubleshooter = TroubleshootWindow()
        self.troubleshooter.delay_updated.connect(self.getDelay)
        self.troubleshooter.start_time_updated.connect(self.getStartTime)
        self.troubleshooter.end_time_updated.connect(self.getEndTime)
        self.troubleshooter.show()


    def getStartTime(self):
        start = self.troubleshooter.getStartTime()
        self.default_start_time_label.hide()
        self.start_time_line_edit.setText(str(start))


    def getEndTime(self):
        end = self.troubleshooter.getEndTime()
        self.default_end_time_label.hide()
        self.end_time_line_edit.setText(str(end))


    def getDelay(self):
        delay = self.troubleshooter.getDelay()
        self.delay_line_edit.setEnabled(True)
        self.delay_line_edit.setText(str(delay))
          

    def getCycleDeterminer(self):
        if self.mts_cycle_checkbox.isChecked():
            self.fluke_cycle_checkbox.setDisabled(True)
            self.all_data["Cycle Determiner"] = "mts"
        else:
            self.fluke_cycle_checkbox.setDisabled(False)
            # If neither is checked, remove the entry
            if not self.fluke_cycle_checkbox.isChecked():
                self.all_data.pop("Cycle Determiner", None)
    
        if self.fluke_cycle_checkbox.isChecked():
            self.mts_cycle_checkbox.setDisabled(True)
            self.all_data["Cycle Determiner"] = "fluke"
        else:
            self.mts_cycle_checkbox.setDisabled(False)
            # If neither is checked, remove the entry
            if not self.mts_cycle_checkbox.isChecked():
                self.all_data.pop("Cycle Determiner", None)
                
    def checkCycles(self): #mild bad logic going on here with the false case
        if (self.cycles_checkbox.isChecked()):
            self.all_data["No Cycles"] = True
            self.fluke_cycle_checkbox.setDisabled(True)
            self.mts_cycle_checkbox.setDisabled(True)
        else:
            self.all_data["No Cycles"] = False
            
         


class AnotherWindow(QWidget):
    def __init__(self, graph, title):
        super().__init__()
        self.setWindowTitle(title)
        self.canvas = FigureCanvas(graph)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.draw()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)

def main_cli():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main_cli()
