'''
Defines all model, algorithmic, and optimization parameters
for calibration of the Lagoudas 1-D SMA model with smooth hardening :cite:p:`lagoudas_constitutive_2012`
'''

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap

from matplotlib.figure import Figure
from matplotlib import rcParams as rc
from matplotlib import font_manager
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import shutil
import tempfile

#def log_error(msg):
#    import os
#    try:
#        # Use the user's home directory for safety
#        log_path = os.path.expanduser("~/pyapp_error_log_cal.txt")
#        with open(log_path, "a") as f:
#            f.write(msg + "\n")
#    except Exception as log_fail:
#        # Last resort if even logging fails
#        print("Logging failed!")
#        print(f"Type: {type(log_fail)}")
#        print(f"Error: {log_fail}")
#        print("Traceback:")
#        traceback.print_exc()
#        pass

class CalibrationParametersWidget(QtWidgets.QWidget):
    '''
    Widget to define the tab where all the calibration parameters
    can be defined (active design variables, bounds, specified values,
    optimization parameters).
    '''
        
    def __init__(self):
        '''
        Initialize the tab.

        Returns
        -------
        None.

        '''
        super().__init__()

        header_font_size = 8
        header_weight = 75
        normal_font_size = 8
        normal_weight = 50

        lineEdit_height = 30
        lineEdit_width = 100

        parameter_label_height = 60
        parameter_label_width = 200

        spacer_item_height = lineEdit_height
        spacer_item_small_width = 5
        spacer_item_width = 30
        #create ''master'' spacer item to use throughout
        regular_spacer = QtWidgets.QSpacerItem(
            spacer_item_width,
            spacer_item_height,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
            )

        small_spacer = QtWidgets.QSpacerItem(
            spacer_item_small_width,
            spacer_item_height,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
            )

        self.grid_layout = QtWidgets.QGridLayout(self)
        # self.centralwidget = QtWidgets.QWidget(self)
        # self.grid_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.grid_layout.setSpacing(20)
        # DV_flags is an array of booleans (T/F) that determines whether
        # a specific design variable is active
        # True = Active (unconstrained)
        # False = Inactive (constrained)
        #Right now, we have 17 design variables possible. Need to revisit this
        self.DV_flags = np.array(np.ones(shape=17),dtype=bool)
        self.flags = {}
        self.flags['modulus_flag'] = False
        self.flags['slope_flag'] = False
        self.flags['smooth_hardening_flag'] = False

        self.known_values = {} #known values is slaved to DV_flags
        # Elastic properties
        #%% E_M
        self.E_M = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.E_M,
            "E_M",
            "Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% E_A
        self.E_A = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.E_A,
            "E_A",
            "Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        # Transformation temperatures
        #%%M_s
        self.M_s = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.M_s,
            "M_s",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% A_s
        self.A_s = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.A_s,
            "A_s",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% M_s - M_f
        self.M_s_M_f = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.M_s_M_f,
            "M_s-M_f",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% A_f - A_s
        self.A_f_A_s = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.A_f_A_s,
            "A_f-A_s",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% C_A
        self.C_A = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.C_A,
            "C_A",
            "Pa/K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% C_M
        self.C_M = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.C_M,
            "C_M",
            "MPa/K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        # Transformation strain properties
        #%% H_min
        self.H_min = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.H_min,
            "H_{min}",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% H_max - H_min
        self.H_max_H_min = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.H_max_H_min,
            "H_{max} - H_{min}",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% sigma_0
        self.sigma_0 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.sigma_0,
            r"\sigma_0",
            "Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% k
        self.k = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.k,
            "k",
            "1/Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        # Other properties
        #%% n_1
        self.n_1 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_1,
            "n_1",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% n_2
        self.n_2 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_2,
            "n_2",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )


        #%% n_3
        self.n_3 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_3,
            "n_3",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% n_4
        self.n_4 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_4,
            "n_4",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% alpha
        self.alpha = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.alpha,
            r"\alpha",
            "1/m",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% Left labels
        self.left_labels = QtWidgets.QHBoxLayout()
        # self.left_labels.setContentsMargins(0, -1, 5, -1)
        self.parameter_label = QtWidgets.QLabel(self)

        self.create_label(
                self.parameter_label,
                "Parameter",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.parameter_label)
        # self.left_labels.addItem(small_spacer)
        self.lower_bound_label = QtWidgets.QLabel(self)

        self.create_label(
                self.lower_bound_label,
                "Lower Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.lower_bound_label)
        # self.left_labels.addItem(regular_spacer)


        self.upper_bound_label = QtWidgets.QLabel(self)

        self.create_label(
                self.upper_bound_label,
                "Upper Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.upper_bound_label)

        # self.left_labels.addItem(regular_spacer)

        self.specify_label = QtWidgets.QLabel(self)

        self.create_label(
                self.specify_label,
                "Specify?",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.specify_label)
        # self.left_labels.addItem(regular_spacer)
        self.value_label = QtWidgets.QLabel(self)

        self.create_label(
                self.value_label,
                "Value",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.value_label)

        #%% Right labels
        self.right_labels = QtWidgets.QHBoxLayout()
        self.right_labels.setContentsMargins(0, -1, 5, -1)

        self.parameter_label_right = QtWidgets.QLabel(self)
        self.lower_bound_label_right = QtWidgets.QLabel(self)
        self.upper_bound_label_right = QtWidgets.QLabel(self)
        self.specify_label_right = QtWidgets.QLabel(self)
        self.value_label_right = QtWidgets.QLabel(self)

        self.create_label(
                self.parameter_label_right,
                "Parameter",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.parameter_label_right)
        # self.right_labels.addItem(small_spacer)

        self.create_label(
                self.lower_bound_label_right,
                "Lower Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.lower_bound_label_right)
        # self.right_labels.addItem(regular_spacer)

        self.create_label(
                self.upper_bound_label_right,
                "Upper Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.upper_bound_label_right)
        # self.right_labels.addItem(regular_spacer)

        self.create_label(
                self.specify_label_right,
                "Specify?",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.specify_label_right)

        # self.right_labels.addItem(regular_spacer)

        self.create_label(
                self.value_label_right,
                "Value",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.value_label_right)

        #%% Pushbuttons
        self.buttons = QtWidgets.QHBoxLayout()

        font_size = 14
        font_weight = 75

        font = self.create_font(
            font_size,
            font_weight,
            bold_flag = False
            )

        # self.buttons.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self)


        # self.pushButton.setMinimumSize(QtCore.QSize(200, 100))
        # self.pushButton.setMaximumSize(QtCore.QSize(200, 100))
        self.pushButton.setFont(font)
        self.pushButton.setText('Calibrate')
        self.buttons.addWidget(self.pushButton)

        #%% Design variable flags
        self.prop_constraints_label = QtWidgets.QHBoxLayout()
        self.prop_constraints_label.setContentsMargins(-1, -1, 5, -1)

        # Header
        self.prop_constraints_header = QtWidgets.QLabel(self)
        self.prop_constraints_header.setText('Material property constraints')

        header_font = self.create_font(
            header_font_size,
            header_weight,
            bold_flag = True
            )

        self.prop_constraints_header.setFont(header_font)
        self.prop_constraints_header.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.prop_constraints_label.addStretch()
        self.prop_constraints_label.addWidget(self.prop_constraints_header)
        self.prop_constraints_label.addStretch()

        #Modulus Flag

        self.modulus_flag = QtWidgets.QHBoxLayout()

        self.create_constraint(
            self.modulus_flag,
            "modulus_flag",
            r"$E_A = E_M$",
            text_width = 200,
            text_height = 43,
            font_weight = 75,
            font_size = 12,
            latex_flag = True
            )

        # Slope flag

        self.slope_flag = QtWidgets.QHBoxLayout()
        self.create_constraint(
            self.slope_flag,
            "slope_flag",
            r"$C_A = C_M$",
            text_width = 200,
            text_height = 43,
            font_weight = 75,
            font_size = 12,
            latex_flag = True
            )

        self.smooth_hardening_flag = QtWidgets.QHBoxLayout()

        self.create_constraint(
            self.smooth_hardening_flag,
            "smooth_hardening_flag",
            r"$n_1=n_2=n_3=n_4$",
            text_width = 200,
            text_height = 43,
            font_weight = 75,
            font_size = 12,
            latex_flag = True
            )


        #%% Algorithmic parameters

        self.alg_params_label = QtWidgets.QHBoxLayout()
        self.alg_params_label.setContentsMargins(-1, -1, 5, -1)

        # Header
        self.alg_param_header = QtWidgets.QLabel(self)
        self.alg_param_header.setText('Algorithmic Parameters')

        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))

        self.alg_param_header.setFont(header_font)
        self.alg_param_header.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.alg_params_label.addStretch()
        self.alg_params_label.addWidget(self.alg_param_header)
        self.alg_params_label.addStretch()

        self.non_op_params = QtWidgets.QHBoxLayout()
        self.non_op_params.setContentsMargins(-1, -1, 5, -1)


        # delta
        self.delta = QtWidgets.QHBoxLayout()

        self.create_parameter(
                parameter_object=self.delta,
                name='delta',
                text=r"$\delta$",
                text_width=200,
                text_height=43,
                text_size=12,
                text_weight=75,
                lineEdit_width=lineEdit_width,
                lineEdit_height=lineEdit_height,
                latex_flag = True,
                )

        self.sigma_cal = QtWidgets.QHBoxLayout()

        self.create_parameter(
                parameter_object=self.sigma_cal,
                name='sigma_cal',
                text=r"$\sigma_{cal}$",
                text_width=200,
                text_height=43,
                text_size=12,
                text_weight=75,
                lineEdit_width=lineEdit_width,
                lineEdit_height=lineEdit_height,
                latex_flag = True,
                )

        #MVF_tolerance
        normal_font = self.create_font(
            normal_font_size,
            normal_weight,
            bold_flag = False
            )

        self.MVF_tol = QtWidgets.QHBoxLayout()
        self.MVF_tol.setContentsMargins(-1, -1, 5, -1)


        self.MVF_tol.label = QtWidgets.QLabel(self)
        self.MVF_tol.label.setText('MVF Tolerance')

        #self.gen_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.gen_label.setMaximumSize(QtCore.QSize(90, 16777215))



        self.MVF_tol.label.setFont(normal_font)
        self.MVF_tol.label.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.MVF_tol.label.setMaximumSize(
            QtCore.QSize(
                200,
                1000))
        self.MVF_tol.addWidget(self.MVF_tol.label)
        # self.MVF_tol.addStretch()
        self.MVF_tol.lineEdit = QtWidgets.QLineEdit(self)

        self.MVF_tol.lineEdit.setMaximumSize(
            QtCore.QSize(
                lineEdit_width,
                lineEdit_height
                )
            )



        # self.gen_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        # self.gen_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.MVF_tol.addWidget(self.MVF_tol.lineEdit)

        # self.create_parameter(
        #         parameter_object=self.MVF_tol,
        #         name='MVF_tol',
        #         text="MVF Tol",
        #         text_width=200,
        #         text_height=43,
        #         text_size=12,
        #         text_weight=75,
        #         lineEdit_width=lineEdit_width,
        #         lineEdit_height=lineEdit_height,
        #         latex_flag = False,
        #         bold_flag = False,
        #         )

        #%%Optimization parameters
        #Might need to make this a grid with labels on the left and line edits on the right

        self.op_params_label = QtWidgets.QHBoxLayout()
        self.op_params_label.setContentsMargins(-1, -1, 5, -1)

        # Header
        self.opt_param_header = QtWidgets.QLabel(self)
        self.opt_param_header.setText('Optimization Parameters')
        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))

        self.opt_param_header.setFont(header_font)
        self.opt_param_header.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.op_params_label.addStretch()
        self.op_params_label.addWidget(self.opt_param_header)
        self.op_params_label.addStretch()

        # Number of generations
        self.num_gens = QtWidgets.QHBoxLayout()
        self.num_gens.setContentsMargins(-1, -1, 5, -1)


        self.gen_label = QtWidgets.QLabel(self)
        self.gen_label.setText('Number of generations')

        #self.gen_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.gen_label.setMaximumSize(QtCore.QSize(90, 16777215))



        self.gen_label.setFont(normal_font)
        self.gen_label.setAlignment(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.num_gens.addWidget(self.gen_label)
        self.num_gens.addStretch()
        self.gen_line = QtWidgets.QLineEdit(self)



        # self.gen_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        # self.gen_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.num_gens.addWidget(self.gen_line)

        self.pop_size = QtWidgets.QHBoxLayout()
        self.pop_size.setContentsMargins(-1, -1, 5, -1)

        self.pop_label = QtWidgets.QLabel(self)
        self.pop_label.setText('Population size')



        #self.pop_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.pop_label.setMaximumSize(QtCore.QSize(90, 16777215))

        self.pop_label.setFont(normal_font)
        self.pop_label.setAlignment(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.pop_size.addWidget(self.pop_label)
        self.pop_size.addStretch()
        self.pop_line = QtWidgets.QLineEdit(self)



        # self.pop_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        # self.pop_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))

        self.pop_size.addWidget(self.pop_line)

        self.num_iters = QtWidgets.QHBoxLayout()
        self.num_iters.setContentsMargins(-1, -1, 5, -1)

        self.iter_label = QtWidgets.QLabel(self)
        self.iter_label.setText('Gradient-based iterations')

        #self.iter_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.iter_label.setMaximumSize(QtCore.QSize(90, 16777215))

        self.iter_label.setFont(normal_font)
        self.iter_label.setAlignment(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.num_iters.addWidget(self.iter_label)
        self.num_iters.addStretch()
        self.iter_line = QtWidgets.QLineEdit(self)


        # self.iter_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        # self.iter_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))

        self.num_iters.addWidget(self.iter_line)


        #%% Grid layout commands
        #Will need to figure out grid_layout at a later date.
        #Elastic properties
        self.grid_layout.addLayout(self.E_M, 1, 0, 1, 1)
        self.grid_layout.addLayout(self.E_A, 1, 1, 1, 1)
        #Phase diagram properties
        self.grid_layout.addLayout(self.M_s, 2, 0, 1, 1)
        self.grid_layout.addLayout(self.M_s_M_f, 2, 1, 1, 1)
        self.grid_layout.addLayout(self.A_s, 3, 0, 1, 1)
        self.grid_layout.addLayout(self.A_f_A_s, 3, 1, 1, 1)
        self.grid_layout.addLayout(self.C_M, 4, 0, 1, 1)
        self.grid_layout.addLayout(self.C_A, 4, 1, 1, 1)
        #Transformation strain properties
        self.grid_layout.addLayout(self.H_min, 5, 0, 1, 1)
        self.grid_layout.addLayout(self.H_max_H_min, 5, 1, 1, 1)
        self.grid_layout.addLayout(self.sigma_0, 6, 0, 1, 1)
        self.grid_layout.addLayout(self.k, 6, 1, 1, 1)
        #Other properties
        self.grid_layout.addLayout(self.n_1, 7, 0, 1, 1)
        self.grid_layout.addLayout(self.n_2, 7, 1, 1, 1)
        self.grid_layout.addLayout(self.n_3, 8, 0, 1, 1)
        self.grid_layout.addLayout(self.n_4, 8, 1, 1, 1)
        self.grid_layout.addLayout(self.alpha, 9, 0, 1, 1)

        self.grid_layout.addLayout(self.prop_constraints_label,0,2,1,1)
        self.grid_layout.addLayout(self.modulus_flag,1,2,1,1)
        self.grid_layout.addLayout(self.slope_flag,2,2,1,1)
        self.grid_layout.addLayout(self.smooth_hardening_flag,3,2,1,1)

        #Algorithmic parameters
        self.grid_layout.addLayout(self.alg_params_label,4,2,1,1)
        self.grid_layout.addLayout(self.delta,5,2,1,1)
        self.grid_layout.addLayout(self.sigma_cal,6,2,1,1)
        self.grid_layout.addLayout(self.MVF_tol,7,2,1,1)

        #Optimization parameters
        self.grid_layout.addLayout(self.op_params_label, 8, 2, 1, 1)
        self.grid_layout.addLayout(self.num_gens, 9, 2, 1, 1)
        self.grid_layout.addLayout(self.pop_size, 10, 2, 1, 1)
        self.grid_layout.addLayout(self.num_iters, 11, 2, 1, 1)
        #Buttons and Labels

        self.grid_layout.addLayout(self.buttons, 12, 2, 2, 2)
        self.grid_layout.addLayout(self.right_labels, 0, 1, 1, 1)
        self.grid_layout.addLayout(self.left_labels, 0, 0, 1, 1)


        #%% Alignment commands need to be after the grid layout
        self.prop_constraints_label.setAlignment(QtCore.Qt.AlignRight)
        self.modulus_flag.setAlignment(QtCore.Qt.AlignRight)
        self.slope_flag.setAlignment(QtCore.Qt.AlignRight)
        self.smooth_hardening_flag.setAlignment(QtCore.Qt.AlignRight)


        self.pop_line.setAlignment(QtCore.Qt.AlignRight)
        self.iter_line.setAlignment(QtCore.Qt.AlignRight)


        self.num_gens.setAlignment(QtCore.Qt.AlignLeft)
        self.pop_size.setAlignment(QtCore.Qt.AlignLeft)
        self.num_iters.setAlignment(QtCore.Qt.AlignLeft)

        #%% Initial conditions
        self.loadDefaults()

    # %% Functions
    def uncheck(self,state):
        '''
        Translates all of the checkboxes for each
        material parameter to different DV flags.
        Toggle function to refresh every time a specified value
        box is unchecked. 
        The current implementation is brute-force (i.e., each
        sender is a different if-else loop), so this could be 
        refactored.

        Parameters
        ----------
        state : QtCore.Qt.Checked
            state, either unchecked or checked, for each DV and
            the other flags.

        Returns
        -------
        None.

        '''
        if state == QtCore.Qt.Checked:
            if self.E_M.sender() == self.E_M.checkBox:
                print('The E_M checkbox is checked')
                self.DV_flags[0] = False

            if self.E_A.sender() == self.E_A.checkBox:
                print('The E_A checkbox is checked')
                # if self.flags['modulus_flag'] == True:
                #     self.E_A.specified_value.setEnabled(False)

                self.DV_flags[1] = False

            if self.M_s.sender() == self.M_s.checkBox:
                print('The M_s checkbox is checked')
                self.DV_flags[2] = False

            if self.M_s_M_f.sender() == self.M_s_M_f.checkBox:
                print('The M_s - M_f checkbox is checked')
                self.DV_flags[3] = False

            if self.A_s.sender() == self.A_s.checkBox:
                print('The A_s checkbox is checked')
                self.DV_flags[4] = False

            if self.A_f_A_s.sender() == self.A_f_A_s.checkBox:
                print('The A_f - A_s checkbox is checked')
                self.DV_flags[5] = False

            if self.C_M.sender() == self.C_M.checkBox:
                print('The C_M checkbox is checked')
                self.DV_flags[6] = False

            if self.C_A.sender() == self.C_A.checkBox:
                print('The C_A checkbox is checked')
                self.DV_flags[7] = False

            if self.H_min.sender() == self.H_min.checkBox:
                print('The H_min checkbox is checked')
                self.DV_flags[8] = False

            if self.H_max_H_min.sender() == self.H_max_H_min.checkBox:
                print('The H_max - H_min checkbox is checked')
                self.DV_flags[9] = False

            if self.k.sender() == self.k.checkBox:
                print('The k checkbox is checked')
                self.DV_flags[10] = False

            if self.n_1.sender() == self.n_1.checkBox:
                print('The n_1 checkbox is checked')
                self.DV_flags[11] = False

            if self.n_2.sender() == self.n_2.checkBox:
                print('The n_2 checkbox is checked')
                self.DV_flags[12] = False

            if self.n_3.sender() == self.n_3.checkBox:
                print('The n_3 checkbox is checked')
                self.DV_flags[13] = False

            if self.n_4.sender() == self.n_4.checkBox:
                print('The n_4 checkbox is checked')
                self.DV_flags[14] = False

            if self.sigma_0.sender() == self.sigma_0.checkBox:
                print('The sigma_0 checkbox is checked')
                self.DV_flags[15] = False

            if self.alpha.sender() == self.alpha.checkBox:
                print('The alpha checkbox is checked')
                self.DV_flags[16] = False

            if self.modulus_flag.sender() == self.modulus_flag.checkbox:
                # The modulus flag does the following:
                    # 1. Eliminates the design variable for E_A from the opt. problem.
                    # 2. Sets the modulus flag = True s.t. E_A = E_M
                    # 3. Clears and disables the text edit for E_A specified
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Modulus flag checked')
                self.DV_flags[1]=False
                self.flags['modulus_flag'] = True
                self.E_A.checkBox.setEnabled(False)
                self.E_A.minimum_bound.setEnabled(False)
                self.E_A.maximum_bound.setEnabled(False)
                self.E_A.specified_value.setEnabled(False)
                self.E_A.specified_value.setText('')

            if self.slope_flag.sender() == self.slope_flag.checkbox:
                # The slope flag does the following:
                    # 1. Eliminates the design variable for C_A from the opt. problem.
                    # 2. Sets the slope flag = True s.t. C_A = C_M
                    # 3. Clears and disables the text edit for C_A specified
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Slope flag checked')
                self.DV_flags[7]=False
                self.flags['slope_flag'] = True
                self.C_A.checkBox.setEnabled(False)
                self.C_A.minimum_bound.setEnabled(False)
                self.C_A.maximum_bound.setEnabled(False)
                self.C_A.specified_value.setEnabled(False)
                self.C_A.specified_value.setText('')

            if self.smooth_hardening_flag.sender() == self.smooth_hardening_flag.checkbox:
                # The smooth hardening flag does the following:
                    # 1. Eliminates the design variables for n_2, n_3
                    #    n_4 from the opt. problem.
                    # 2. Sets the smooth hardening flag = True s.t.
                    #    n_1 = n_2 = n_3 = n_4
                    # 3. Clears and disables the text edit for n_2_n_4 specified
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Smooth hardening flag checked')
                self.DV_flags[12]=False #n_2
                self.DV_flags[13]=False #n_3
                self.DV_flags[14]=False #n_4
                self.flags['smooth_hardening_flag'] = True

                #n_2
                self.n_2.checkBox.setEnabled(False)
                self.n_2.minimum_bound.setEnabled(False)
                self.n_2.maximum_bound.setEnabled(False)
                self.n_2.specified_value.setEnabled(False)
                self.n_2.specified_value.setText('')

                #n_3
                self.n_3.checkBox.setEnabled(False)
                self.n_3.minimum_bound.setEnabled(False)
                self.n_3.maximum_bound.setEnabled(False)
                self.n_3.specified_value.setEnabled(False)
                self.n_3.specified_value.setText('')

                #n_4
                self.n_4.checkBox.setEnabled(False)
                self.n_4.minimum_bound.setEnabled(False)
                self.n_4.maximum_bound.setEnabled(False)
                self.n_4.specified_value.setEnabled(False)
                self.n_4.specified_value.setText('')

        elif state == QtCore.Qt.Unchecked:
            if self.E_M.sender() == self.E_M.checkBox:
                print('The E_M checkbox is unchecked')
                self.DV_flags[0] = True

            if self.E_A.sender() == self.E_A.checkBox:
                print('The E_A checkbox is unchecked')
                self.DV_flags[1] = True

            if self.M_s.sender() == self.M_s.checkBox:
                print('The M_s checkbox is unchecked')
                self.DV_flags[2] = True

            if self.M_s_M_f.sender() == self.M_s_M_f.checkBox:
                print('The M_s - M_f checkbox is unchecked')
                self.DV_flags[3] = True

            if self.A_s.sender() == self.A_s.checkBox:
                print('The A_s checkbox is unchecked')
                self.DV_flags[4] = True

            if self.A_f_A_s.sender() == self.A_f_A_s.checkBox:
                print('The A_f - A_s checkbox is unchecked')
                self.DV_flags[5] = True

            if self.C_M.sender() == self.C_M.checkBox:
                print('The C_M checkbox is unchecked')
                self.DV_flags[6] = True

            if self.C_A.sender() == self.C_A.checkBox:
                print('The C_A checkbox is unchecked')
                self.DV_flags[7] = True

            if self.H_min.sender() == self.H_min.checkBox:
                print('The H_min checkbox is unchecked')
                self.DV_flags[8] = True

            if self.H_max_H_min.sender() == self.H_max_H_min.checkBox:
                print('The H_max - H_min checkbox is unchecked')
                self.DV_flags[9] = True

            if self.k.sender() == self.k.checkBox:
                print('The k checkbox is unchecked')
                self.DV_flags[10] = True

            if self.n_1.sender() == self.n_1.checkBox:
                print('The n_1 checkbox is unchecked')
                self.DV_flags[11] = True

            if self.n_2.sender() == self.n_2.checkBox:
                print('The n_2 checkbox is unchecked')
                self.DV_flags[12] = True

            if self.n_3.sender() == self.n_3.checkBox:
                print('The n_3 checkbox is unchecked')
                self.DV_flags[13] = True

            if self.n_4.sender() == self.n_4.checkBox:
                print('The n_4 checkbox is unchecked')
                self.DV_flags[14] = True

            if self.sigma_0.sender() == self.sigma_0.checkBox:
                print('The sigma_0 checkbox is unchecked')
                self.DV_flags[15] = True

            if self.alpha.sender() == self.alpha.checkBox:
                print('The alpha checkbox is unchecked')
                self.DV_flags[16] = True

            if self.modulus_flag.sender() == self.modulus_flag.checkbox:
                # The modulus flag does the following:
                    # 1. Eliminates the design variable for E_A from the opt. problem.
                    # 2. Sets the modulus flag = True s.t. E_A = E_M
                    # 3. Clears and disables the text edit for E_A specified
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Modulus flag unchecked')
                self.DV_flags[1]=True
                self.flags['modulus_flag'] = False
                self.E_A.checkBox.setEnabled(True)
                self.E_A.checkBox.setChecked(False)
                self.E_A.minimum_bound.setEnabled(True)
                self.E_A.maximum_bound.setEnabled(True)
                self.E_A.specified_value.setEnabled(False)
                self.E_A.specified_value.setText('')

            if self.slope_flag.sender() == self.slope_flag.checkbox:
                # The slope flag does the following:
                    # 1. Eliminates the design variable for C_A from the opt. problem.
                    # 2. Sets the slope flag = True s.t. C_A = C_M
                    # 3. Clears and disables the text edit for C_A specified
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Slope flag unchecked')
                self.DV_flags[7]=True
                self.flags['slope_flag'] = False
                self.C_A.checkBox.setEnabled(True)
                self.C_A.checkBox.setChecked(False)
                self.C_A.minimum_bound.setEnabled(True)
                self.C_A.maximum_bound.setEnabled(True)
                self.C_A.specified_value.setEnabled(False)
                self.C_A.specified_value.setText('')

            if self.smooth_hardening_flag.sender() == self.smooth_hardening_flag.checkbox:
                # The smooth hardening flag does the following:
                    # 1. Eliminates the design variables for n_2, n_3
                    #    n_4 from the opt. problem.
                    # 2. Sets the smooth hardening flag = True s.t.
                    #    n_1 = n_2 = n_3 = n_4
                    # 3. Clears and disables the text edit for n_2_n_4 specified
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Smooth hardening flag unchecked')
                self.DV_flags[12]=True #n_2
                self.DV_flags[13]=True #n_3
                self.DV_flags[14]=True #n_4
                self.flags['smooth_hardening_flag'] = False

                #n_2
                self.n_2.checkBox.setEnabled(True)
                self.n_2.checkBox.setChecked(False)
                self.n_2.minimum_bound.setEnabled(True)
                self.n_2.maximum_bound.setEnabled(True)
                self.n_2.specified_value.setEnabled(False)
                self.n_2.specified_value.setText('')

                #n_3
                self.n_3.checkBox.setEnabled(True)
                self.n_3.checkBox.setChecked(False)
                self.n_3.minimum_bound.setEnabled(True)
                self.n_3.maximum_bound.setEnabled(True)
                self.n_3.specified_value.setEnabled(False)
                self.n_3.specified_value.setText('')

                #n_4
                self.n_4.checkBox.setEnabled(True)
                self.n_4.checkBox.setChecked(False)
                self.n_4.minimum_bound.setEnabled(True)
                self.n_4.maximum_bound.setEnabled(True)
                self.n_4.specified_value.setEnabled(False)
                self.n_4.specified_value.setText('')

        print(self.DV_flags)

    def loadDefaults(self):
        '''
        Imports default values for lower and upper bounds
        of all DVs.
        Default values are hard-coded below, but should
        be moved to a more transparent data source.

        Returns
        -------
        None.

        '''
        #Current order:
            #E_M, E_A, M_s, M_s-M_f, A_s, A_f - A_s, C_M, C_A, H_min,
            #H_max - H_min, k, n_1, n_2, n_3, n_4, sigma_crit, alpha
        lower_bound_defaults = [20E9,20E9,425.0,10.0,450.0,10.0,2E6,2E6,0.0,
                                0.01,1E-8,0.01,0.01,0.01,0.01,0.0,0.0]
        upper_bound_defaults = [110E9,110E9,500.0,50.0,525.0,50.0,15E6,15E6,0.03,
                                0.05,1E-6,1.0,1.0,1.0,1.0,60E6,1E-6]

        objects = [
            self.E_M,
            self.E_A,
            self.M_s,
            self.M_s_M_f,
            self.A_s,
            self.A_f_A_s,
            self.C_M,
            self.C_A,
            self.H_min,
            self.H_max_H_min,
            self.k,
            self.n_1,
            self.n_2,
            self.n_3,
            self.n_4,
            self.sigma_0,
            self.alpha,
            ]

        variable_formats = [
            "{:.2e}",
            "{:.2e}",
            "{:.0f}",
            "{:.0f}",
            "{:.0f}",
            "{:.0f}",
            "{:.2e}",
            "{:.2e}",
            "{:.2f}",
            "{:.2f}",
            "{:.2e}",
            "{:.2f}",
            "{:.2f}",
            "{:.2f}",
            "{:.2f}",
            "{:.2e}",
            "{:.2e}"
            ]

        for property_object,lower_bound,upper_bound,variable_format in \
            zip(objects,lower_bound_defaults,upper_bound_defaults,variable_formats):

            property_object.minimum_bound.setText(variable_format.format(lower_bound))
            property_object.maximum_bound.setText(variable_format.format(upper_bound))

        #delta
        self.delta.lineEdit.setText('1e-6')

        #sigma cal
        self.sigma_cal.lineEdit.setText('100e6')

        #MVF_tol
        self.MVF_tol.lineEdit.setText('1e-4')

        #number of generations
        self.gen_line.setText('15')

        #population size
        self.pop_line.setText('20')

        #number of iterations
        self.iter_line.setText('100')

    def updateVal(self):
        '''
        Updates the values of upper and lower DV bounds, both in the
        sliders and in the optimization limits.

        Returns
        -------
        None.

        '''
        for i in range(1, 10):
            for j in range(2):
                if i == 9 and j == 1:
                    break
                upper_bound = float(self.grid_layout.itemAtPosition(i, j).itemAt(4).widget().text())
                lower_bound = float(self.grid_layout.itemAtPosition(i, j).itemAt(2).widget().text())
                slider_val = self.grid_layout.itemAtPosition(i, j).itemAt(3).widget().value()
                guess = self.grid_layout.itemAtPosition(i, j).itemAt(6).widget()
                step = (upper_bound - lower_bound)/100
                guess.setText(str(slider_val * step + lower_bound))

    def updateSlider(self):
        '''
        Update slider values based on upper and lower bounds.

        Returns
        -------
        None.

        '''
        for i in range(1, 10):
            for j in range(2):
                if i == 9 and j == 1:
                    break
                val = self.grid_layout.itemAtPosition(i, j).itemAt(6).widget().text()
                if not val == "":
                    upper_bound = float(
                        self.grid_layout.itemAtPosition(i, j).itemAt(4).widget().text()
                        )
                    lower_bound = float(
                        self.grid_layout.itemAtPosition(i, j).itemAt(2).widget().text()
                        )
                    if float(val) < lower_bound:
                        print('Setting lower bound to specified value for visualization')
                        lower_bound = self.grid_layout.itemAtPosition(
                            i, j
                            ).itemAt(2).widget().setText(str(val))
                    elif float(val) > upper_bound:
                        print('Setting upper bound to specified value for visualization')
                        upper_bound = self.grid_layout.itemAtPosition(
                            i, j
                            ).itemAt(4).widget().setText(str(val))
                    upper_bound = float(
                        self.grid_layout.itemAtPosition(
                            i, j
                            ).itemAt(4).widget().text())
                    lower_bound = float(
                        self.grid_layout.itemAtPosition(
                            i, j
                            ).itemAt(2).widget().text())
                    step = (upper_bound - lower_bound)/100

                    val = float(val)
                    normalized_value = int(val/step-int(lower_bound)/step)
                    self.grid_layout.itemAtPosition(
                        i, j
                        ).itemAt(3).widget().setValue(normalized_value)

    def getBounds(self):
        '''
        Creates the bounds list of lists, that is used in the optimizer.
        This could be refactored to be more agile by refactoring the bounds
        object to something other than a list of lists. 

        Returns
        -------
        bounds : LIST
            List of lists containing all DV bounds.

        '''
        # initialize bounds list of lists
        bounds = []

        #E_M
        bounds.append([float(self.E_M.minimum_bound.text()),
                       float(self.E_M.maximum_bound.text())])

        #E_A
        # if self.flags['modulus_flag'] == False:
        bounds.append([float(self.E_A.minimum_bound.text()),
                       float(self.E_A.maximum_bound.text())])

        #M_s
        bounds.append([float(self.M_s.minimum_bound.text()),
                       float(self.M_s.maximum_bound.text())])

        #M_s-M_f
        bounds.append([float(self.M_s_M_f.minimum_bound.text()),
                       float(self.M_s_M_f.maximum_bound.text())])

        #A_s
        bounds.append([float(self.A_s.minimum_bound.text()),
                       float(self.A_s.maximum_bound.text())])

        #A_f - A_s
        bounds.append([float(self.A_f_A_s.minimum_bound.text()),
                       float(self.A_f_A_s.maximum_bound.text())])

        #C_M
        bounds.append([float(self.C_M.minimum_bound.text()),
                       float(self.C_M.maximum_bound.text())])

        #C_A
        # if self.flags['slope_flag'] == False:
        bounds.append([float(self.C_A.minimum_bound.text()),
                        float(self.C_A.maximum_bound.text())])

        #H_min
        bounds.append([float(self.H_min.minimum_bound.text()),
                       float(self.H_min.maximum_bound.text())])
        #H_max - H_min
        bounds.append([float(self.H_max_H_min.minimum_bound.text()),
                       float(self.H_max_H_min.maximum_bound.text())])
        #k
        bounds.append([float(self.k.minimum_bound.text()),
                       float(self.k.maximum_bound.text())])

        #n_1
        bounds.append([float(self.n_1.minimum_bound.text()),
                       float(self.n_1.maximum_bound.text())])

        #n_2
        # if self.flags['smooth_hardening_flag'] == False:
        bounds.append([float(self.n_2.minimum_bound.text()),
                       float(self.n_2.maximum_bound.text())])

        #n_3
        bounds.append([float(self.n_3.minimum_bound.text()),
                       float(self.n_3.maximum_bound.text())])

        #n_4
        bounds.append([float(self.n_4.minimum_bound.text()),
                       float(self.n_4.maximum_bound.text())])

        #sigma_crit
        bounds.append([float(self.sigma_0.minimum_bound.text()),
                       float(self.sigma_0.maximum_bound.text())])

        #alpha
        bounds.append([float(self.alpha.minimum_bound.text()),
                       float(self.alpha.maximum_bound.text())])

        specified_parameter_indices = [i for i, x in enumerate(self.DV_flags) if x==False]
        #Remove all bounds that are already specified.
        for index in sorted(specified_parameter_indices,reverse=True):
            del bounds[index]


        return bounds

    def getSpecifiedValues(self):
        '''
        Get the values that were specified to be constrained.
        Once again, this could be refactored to be more flexible with different models.

        Returns
        -------
        None.

        '''
        #
        ## MAYBE: ONLY MAKE THE TEXT BOXES ABLE TO BE ACCESSED WHEN THE ASSOCIATED
        ## CHECKBOX IS CLICKED


        DV_order = ['E_M','E_A', 'M_s', 'M_s-M_f', 'A_s', 'A_f - A_s', 'C_M', 'C_A', 'H_min',
                    'H_max - H_min', 'k', 'n_1', 'n_2', 'n_3', 'n_4', 'sig_crit', 'alpha']


        lineEdits = [
            self.E_M.specified_value,
            self.E_A.specified_value,
            self.M_s.specified_value,
            self.M_s_M_f.specified_value,
            self.A_s.specified_value,
            self.A_f_A_s.specified_value,
            self.C_M.specified_value,
            self.C_A.specified_value,
            self.H_min.specified_value,
            self.H_max_H_min.specified_value,
            self.k.specified_value,
            self.n_1.specified_value,
            self.n_2.specified_value,
            self.n_3.specified_value,
            self.n_4.specified_value,
            self.sigma_0.specified_value,
            self.alpha.specified_value,
            ]

        for counter in range(len(DV_order)):
            if DV_order[counter] == 'E_A' and self.flags['modulus_flag'] == True:
                pass
            elif DV_order[counter] == 'C_A' and self.flags['slope_flag'] == True:
                pass
            elif DV_order[counter] in ['n_2','n_3','n_4'] and \
                self.flags['smooth_hardening_flag'] == True:
                    pass
            elif self.DV_flags[counter] == False:
                self.known_values[DV_order[counter]] = float(lineEdits[counter].text())

        self.delta.value = float(self.delta.lineEdit.text())
        self.sigma_cal.value = float(self.sigma_cal.lineEdit.text())
        self.MVF_tol.value = float(self.MVF_tol.lineEdit.text())

        self.num_gens = float(self.gen_line.text())
        self.pop_size = float(self.pop_line.text())
        self.num_iters = float(self.iter_line.text())

    def create_label(
            self,
            label_object,
            label_text,
            font_size,
            font_weight,
            parameter_label_width,
            parameter_label_height,
            ):
        '''
        Utility function to create a QLabel object. 
        Sets the font and alignment of the label.
        
        Parameters
        ----------
        label_object : qlabel object
            empty label
        label_text : str
            string to display in the label
        font_size : float
            size of the font to be displayed.
        font_weight : float
            weight of the font (0-100).
        parameter_label_width : int
            width of the label (pixels).
        parameter_label_height : int
            height of the label (pixels).

        Returns
        -------
        None.

        '''

        label_object.setWordWrap(True)
        label_object.setText(label_text)

        font = self.create_font(
            font_size,
            font_weight,
            bold_flag = True
            )

        label_object.setFont(font)
        label_object.setAlignment(QtCore.Qt.AlignCenter)

    def create_material_property(
            self,
            property_object,
            name,
            units,
            parameter_label_width,
            parameter_label_height,
            line_edit_width,
            line_edit_height,
            small_spacer,
            regular_spacer):
        '''
        Utility function to create all the necessary components
        of a material property (label, upper and lower bounds, 
        specified value, and checkbox). 

        Parameters
        ----------
        property_object : class
            class to contain all objects under a material property
        name : str
            name of the property.
        units : str
            units (SI) of the property.
        parameter_label_width : int
            label width (pixels)
        parameter_label_height : int
            label height (pixels)
        line_edit_width : int
            line edit width (pixels).
        line_edit_height : int
            line edit height (pixels).
        small_spacer : class
            spacer class to give everything room to breathe.
        regular_spacer : class
            spacer class to give everything room to breathe.

        Returns
        -------
        None.

        '''

        property_object.label = self.textToLatex(
            r"$"+name+r"$ [$\mathrm{"+str(units)+"}$]:",
            parameter_label_width,
            parameter_label_height,
            )
        property_object.addWidget(property_object.label)

        # property_object.addItem(small_spacer)

        property_object.minimum_bound = QtWidgets.QLineEdit(self)

        # property_object.minimum_bound.setMinimumSize(
        #     QtCore.QSize(line_edit_width, line_edit_height)
        #     )
        property_object.minimum_bound.setMaximumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.addWidget(property_object.minimum_bound)

        # property_object.addItem(regular_spacer)

        property_object.maximum_bound = QtWidgets.QLineEdit(self)

        # property_object.maximum_bound.setMinimumSize(
        #     QtCore.QSize(line_edit_width, line_edit_height)
        #     )
        property_object.maximum_bound.setMaximumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.addWidget(property_object.maximum_bound)

        # property_object.addItem(regular_spacer)

        property_object.checkBox = QtWidgets.QCheckBox(self)
        property_object.checkBox.stateChanged.connect(self.uncheck)
        property_object.checkBox.setText("")
        property_object.addWidget(property_object.checkBox)

        # property_object.addItem(regular_spacer)

        property_object.specified_value = QtWidgets.QLineEdit(
            self
            )
        # property_object.specified_value.setMinimumSize(
        #     QtCore.QSize(line_edit_width, line_edit_height)
        #     )
        property_object.specified_value.setMaximumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.addWidget(property_object.specified_value)

        # property_object.addItem(regular_spacer)
        property_object.specified_value.setEnabled(False)
        property_object.checkBox.toggled.connect(
            property_object.specified_value.setEnabled
            )
        property_object.checkBox.toggled.connect(
            property_object.maximum_bound.setDisabled
            )
        property_object.checkBox.toggled.connect(
            property_object.minimum_bound.setDisabled
            )

    def create_constraint(
            self,
            constraint_object,
            name,
            text,
            text_width,
            text_height,
            font_weight,
            font_size,
            latex_flag = False):
        '''
        Utility function to create a constraint box. 
        A constraint box is something like "E_A = E_M"

        Parameters
        ----------
        constraint_object : class
            class to contain all objects under a material property
        name : str
            constraint name.
        text : str
            text to display. May require latex if latex_flag = True.
        text_width : int
            bounding box width of the text (pixels).
        text_height : int
            bounding box height of the text (pixels).
        font_weight : int
            font weight (0-100)
        font_size : int
            font size (pts).
        latex_flag : bool, optional
            flag to use latex to render the text. The default is False.

        Returns
        -------
        None.

        '''

        constraint_object.setContentsMargins(-1, -1, 5, -1)

        if latex_flag == False:
            pass
        else:
            constraint_object.label = self.textToLatex(
                text,
                text_width,
                text_height,
                )

        font = self.create_font(
            font_size,
            font_weight,
            bold_flag = True,
            )

        constraint_object.label.setFont(font)
        constraint_object.label.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        constraint_object.addWidget(constraint_object.label)

        constraint_object.checkbox = QtWidgets.QCheckBox(self)
        constraint_object.checkbox.stateChanged.connect(self.uncheck)
        constraint_object.checkbox.setText("")
        constraint_object.addWidget(constraint_object.checkbox)

    def create_parameter(
            self,
            parameter_object,
            name,
            text,
            text_width,
            text_height,
            text_size,
            text_weight,
            lineEdit_width,
            lineEdit_height,
            latex_flag = False,
            bold_flag = True,
            ):
        '''
        Utility function to create a label, line edit, bounds, 
        and a checkbox. 

        Parameters
        ----------
        parameter_object : class
            class to contain all objects that fall in this one parameter
        name : str
            property name.
        text : str
            text to display with the property (needs Latex if latex_flag=True).
        text_width : int
            text width (pixels)
        text_height : int
            text height (pixels)
        text_size : int
            text size (pts).
        text_weight : int
            text weight (0-100).
        line_edit_width : int
            line edit width (pixels).
        line_edit_height : int
            line edit height (pixels).
        latex_flag : bool, optional
            flag to use latex to render the text. The default is False.
        bold_flag : bool, optional
            flag to make text bold. The default is True.
            
        Returns
        -------
        None.

        '''

        parameter_object.setContentsMargins(-1, -1, 5, -1)


        if latex_flag == True:
            parameter_object.label = self.textToLatex(
                text,
                text_width,
                text_height,
                )
        else:
            parameter_object.label = QtWidgets.QLabel(self)
            parameter_object.label.setText(text)


        # parameter_object.label.setMinimumSize(
        #     QtCore.QSize(
        #         text_width,
        #         0
        #         )
        #     )
        parameter_object.label.setMaximumSize(
            QtCore.QSize(
                text_width,
                16777215
                )
            )

        font = self.create_font(
            text_size,
            text_weight,
            bold_flag = bold_flag,
            )

        parameter_object.label.setFont(font)

        parameter_object.label.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )

        parameter_object.addWidget(parameter_object.label)


        parameter_object.lineEdit = QtWidgets.QLineEdit(self)


        # parameter_object.lineEdit.setMinimumSize(QtCore.QSize(
        #     lineEdit_width,
        #     lineEdit_height
        #     )
        #     )
        parameter_object.lineEdit.setMaximumSize(
            QtCore.QSize(
                lineEdit_width,
                lineEdit_height
                )
            )
        parameter_object.addWidget(parameter_object.lineEdit)

    def set_size_policy(
            self,
            lineEdit,
            ):
        '''
        Creates a generic size policy to keep line count down in code.

        Parameters
        ----------
        lineEdit : class
            line edit class to which the size policy will be applied.

        Returns
        -------
        sizePolicy : QtWidgets.QSizePolicy
            generic size policy.

        '''
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            lineEdit.sizePolicy().hasHeightForWidth()
            )
        return sizePolicy

    def create_font(
            self,
            font_size,
            font_weight,
            bold_flag = False,
            ):
        '''
        Creates a QFont object with size, weight, and
        a flag to determine if it's bold.         

        Parameters
        ----------
        font_size : int
            font size (pts).
        font_weight : int
            font weight (0-100)
        bold_flag : bool, optional
            flag to make the font bold. The default is False.

        Returns
        -------
        font : QFont object
            font with size, weight, and bold.

        '''
        
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(bold_flag)
        font.setWeight(font_weight)

        return font

    def textToLatex(self, text, width, height):
        '''
        Creates a png from text to render latex 

        Parameters
        ----------
        text : str
            text to render.
        width : int
            size of the text box (pixels).
        height : int
            size of the text box (pixels).

        Returns
        -------
        label : QLabel object
            png with latex rendered font .

        '''
        # Check if 'Palatino Linotype' is available
        available_fonts = set(f.name for f in font_manager.fontManager.ttflist)

        if "Palatino Linotype" in available_fonts:
            rc["font.serif"] = ["Palatino Linotype"]
        else:
            #print("'Palatino Linotype' not found. Falling back to default serif.")
            # You can list common serif fallbacks if you want
            rc["font.serif"] = ["DejaVu Serif", "Times New Roman", "Georgia"]

        # Always set the general family to 'serif' to activate the list above
        rc["font.family"] = "serif"
        
        
        if shutil.which("latex"):
            #print("LaTeX found, using it for rendering.")
            rc["text.usetex"] = True
        else:
            #print("LaTeX not found, rendering without it.")
            rc["text.usetex"] = False

        dpi = 125
        fig = Figure(figsize=(width/dpi, height/dpi), dpi=dpi)
        canvas = FigureCanvas(fig)
        ax = fig.gca()
        ax.text(0.0,0.0,text,va='center',ha='center',fontsize=10)

        ax.axis('off')
        ax.margins(0)
        ax.patch.set_facecolor('none')
        fig.patch.set_facecolor('none')

        canvas.draw()
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
            tmp_path = tmpfile.name

        canvas.print_figure(tmp_path, facecolor=fig.get_facecolor())
        
        pixmap = QPixmap(tmp_path)

        label = QLabel(self)
        label.setPixmap(pixmap)
        import os
        os.remove(tmp_path)
        label.setMinimumSize(QSize(width, height))

        return label
