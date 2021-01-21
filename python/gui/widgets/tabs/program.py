import json
import os
import threading
from copy import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QPushButton,
    QButtonGroup,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QCheckBox,
    QComboBox,
    QScrollArea,
    QTabBar,
    QHBoxLayout, QRadioButton)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from python.gui.widgets.worker import Worker
from python.zaf2.fishfeed import run


class ProgramTab(QTabBar):
    early_stop_signal = pyqtSignal()

    def __init__(self, parent, name=None):
        super().__init__()
        self.parent = parent
        self.name = name

        self.layout = QHBoxLayout()

        self.setMovable(True)
        self.is_running = False
        self.is_enabled_checkbox = QCheckBox(self.name)
        self.is_enabled_checkbox.stateChanged.connect(lambda: self.record_log("Enabled", self.is_enabled_checkbox.isChecked()))

        self.num_tanks = 30
        self.num_quantity = ["1", "2", "3", "4"]
        self.program_settings = {
            "Program_name": self.name,
            "Enabled": self.is_enabled_checkbox.isChecked(),
            "Type": "Feeding&Washing",
            "Day": None,
            "Time": None,
            "Tanks": [None] * self.num_tanks
        }
        program_default = copy(self.program_settings)

        # Layout left
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)

        self.button_startstop = QPushButton("Run", self)
        self.button_startstop.setFixedSize(QtCore.QSize(100, 35))
        self.button_startstop.setCheckable(True)
        self.button_startstop.clicked.connect(lambda: self.start_program())
        self.button_reset = QPushButton("Reset", self)
        self.button_reset.setFixedSize(QtCore.QSize(100, 35))
        self.button_reset.clicked.connect(lambda: self.reset(program_default))
        self.button_reset.clicked.connect(lambda: self.repaint())
        self.button_duplicate = QPushButton("Duplicate", self)
        self.button_duplicate.setFixedSize(QtCore.QSize(100, 35))
        self.button_duplicate.clicked.connect(lambda: self.duplicate())
        self.button_delete = QPushButton("Delete", self)
        self.button_delete.setFixedSize(QtCore.QSize(100, 35))
        self.button_delete.clicked.connect(lambda: self.delete_tab())

        self.first_button_row_layout = QHBoxLayout()
        self.first_button_row_layout.setAlignment(Qt.AlignLeft)
        self.first_button_row_layout.addWidget(self.button_startstop)
        self.first_button_row_layout.addWidget(self.button_reset)

        self.second_button_row_layout = QHBoxLayout()
        self.second_button_row_layout.setAlignment(Qt.AlignLeft)
        self.second_button_row_layout.addWidget(self.button_duplicate)
        self.second_button_row_layout.addWidget(self.button_delete)

        self.left_layout.addLayout(self.first_button_row_layout)
        self.left_layout.addLayout(self.second_button_row_layout)

        # Create a button group for feed & washing
        self.bgroup1_1 = QButtonGroup(self)
        # self.bgroup1_1.setExclusive(False)
        self.button_feeding = QRadioButton("Feeding and washing", self)
        self.button_feeding.setCheckable(True)
        self.button_feeding.setChecked(True)
        self.button_washing = QRadioButton("Only washing", self)
        self.button_washing.setCheckable(True)

        self.bgroup1_1.addButton(self.button_feeding, 1)
        self.bgroup1_1.addButton(self.button_washing, 2)
        self.bgroup1_1.buttonClicked.connect(lambda: self.record_log("Type", self.bgroup1_1))

        # Create a group box for feeding & washing
        gpbox1_1 = QGroupBox("Program Type")
        grid = QVBoxLayout()
        grid.addWidget(self.button_feeding)
        grid.addWidget(self.button_washing)
        grid.setAlignment(Qt.AlignLeft)
        gpbox1_1.setLayout(grid)
        self.left_layout.addWidget(gpbox1_1)

        # Create a button group for day of week
        self.button_dow = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
            'Everyday',
        ]
        self.bgroup1_2 = QButtonGroup(self)
        self.bgroup1_2.setExclusive(False)
        for id, name in enumerate(self.button_dow):
            button = QCheckBox(name, self)
            button.stateChanged.connect(lambda: self.update_active_days())
            if name == 'Everyday':
                button.clicked.connect(lambda: self.check_everyday())
            self.bgroup1_2.addButton(button, id)

        # adds each button to the layout
        gpbox1_2 = QGroupBox("Select day of week")
        gpbox1_2.setAlignment(Qt.AlignLeft)
        grid = QGridLayout()
        grid.setSpacing(5)
        for i, button in enumerate(self.bgroup1_2.buttons()):
            grid.addWidget(button, i % 4, i // 4)
        gpbox1_2.setLayout(grid)
        self.left_layout.addWidget(gpbox1_2)

        # Add time pulldown
        gpbox1_2_1 = QGroupBox("Select time")
        self.pd_time = QComboBox(self)
        for h in range(24):
            for m in range(2):
                self.pd_time.addItem(f'{h // 12 * 12 + h % 12} : {m * 30 :02d} {"AM" if h < 12 else "PM"}')
        self.pd_time.currentIndexChanged.connect(lambda: self.update_active_days())
        gpbox1_2_1_layout = QVBoxLayout()
        gpbox1_2_1_layout.addWidget(self.pd_time)
        gpbox1_2_1.setLayout(gpbox1_2_1_layout)
        self.left_layout.addWidget(gpbox1_2_1)

        # Group box right
        # Box for food quantity =================================================
        gpbox2 = QGroupBox("Food Quantity")
        gpbox2.setStyleSheet(
            'QGroupBox:title {'
            'subcontrol-origin: margin;'
            'subcontrol-position: top center;'
            'padding-left: 10px;'
            'padding-right: 10px; }'
        )
        gpbox2_layout = QVBoxLayout()
        gpbox2.setLayout(gpbox2_layout)

        gpbox2_1 = QGroupBox()
        grid = QGridLayout()
        grid.setSpacing(15)
        scroll = QScrollArea()
        scroll.setWidget(gpbox2_1)
        # scroll.setFixedWidth(470)
        scroll.setWidgetResizable(True)

        self.bgroup2_1 = QButtonGroup(self)  # buttn gp of tank selecetion
        self.bgroup2_1.setExclusive(False)
        self.bgroup2_2 = []  # QButtonGroup(self)  # buttn gp of food amount selecetion

        # Select/Unselect all tanks
        self.select_unselect_all_checkbox = QCheckBox(f'All Tanks', self)
        self.select_unselect_all_checkbox.toggled.connect(self.select_unselect_all_tanks)
        self.select_unselect_all_checkbox.setChecked(True)
        self.bgroup2_1.addButton(self.select_unselect_all_checkbox, 1)
        grid.addWidget(self.select_unselect_all_checkbox, 0, 0)
        bg = QButtonGroup(self)
        for j, name in enumerate(self.num_quantity):
            b = QRadioButton(name, self)
            b.setFixedSize(QtCore.QSize(40, 20))
            b.setCheckable(True)
            bg.addButton(b, j + 1)
            grid.addWidget(b, 0, j + 1)
        bg.buttonClicked.connect(lambda: self.select_unselect_food_amount())
        self.bgroup2_2.append(bg)

        # Populate tank rows
        for i in range(1, self.num_tanks + 1):
            cb = QCheckBox(f'Tank {i}', self)
            cb.setChecked(True)
            self.bgroup2_1.addButton(cb, i + 1)
            grid.addWidget(cb, i, 0)
            bg = QButtonGroup(self)
            for j, name in enumerate(self.num_quantity):
                b = QRadioButton(name, self)
                b.setFixedSize(QtCore.QSize(40, 20))
                b.setCheckable(True)
                bg.addButton(b, j + 1)
                grid.addWidget(b, i, j + 1)
            bg.buttonClicked.connect(lambda: self.record_log())
            self.bgroup2_2.append(bg)
        self.bgroup2_1.buttonClicked.connect(lambda: self.record_log())
        grid.setAlignment(Qt.AlignCenter)
        gpbox2_1.setLayout(grid)
        gpbox2_layout.addWidget(scroll)

        # Add to layout
        self.layout.addLayout(self.left_layout)
        self.layout.addWidget(gpbox2)
        self.setLayout(self.layout)

        self.update_json()

    @property
    def json_path(self):
        return f'/home/pi/Dev/prod/zaf_data/{self.name}.json'

    def update_isactive(self):
        self.program_settings["Enabled"] = self.is_enabled_checkbox.isChecked()
        self.update_json()

    def check_everyday(self):
        if self.bgroup1_2.buttons()[-1].isChecked():
            for i, bt in enumerate(self.bgroup1_2.buttons()):
                if i != 8:
                    bt.setChecked(True)
        else:
            for i, bt in enumerate(self.bgroup1_2.buttons()):
                if i != 8:
                    bt.setChecked(False)
        self.repaint()
        self.update_active_days()

    def update_active_days(self):
        checked_dow = [i.isChecked() for i in self.bgroup1_2.buttons()]
        dow = [self.button_dow[i][:3] for i, ii in enumerate(checked_dow) if ii and self.button_dow[i] != "Everyday"]
        time = self.pd_time.currentText()
        self.parent.tabs[0].update_program_list()
        self.program_settings["Day"] = dow
        self.program_settings["Time"] = time
        self.update_json()

    def select_unselect_food_amount(self):
        for idx, (tk, bt) in enumerate(zip(self.bgroup2_1.buttons(), self.bgroup2_2)):
            if tk.isChecked():
                for index, i in enumerate(self.bgroup2_2[0].buttons()):
                    if i.isChecked():
                        bt.buttons()[index].setChecked(True)

        self.record_log()

    def select_unselect_all_tanks(self):
        if self.select_unselect_all_checkbox.isChecked():
            for tank in self.bgroup2_1.buttons():
                tank.setChecked(True)
        else:
            for tank in self.bgroup2_1.buttons():
                tank.setChecked(False)

    def record_log(self, key=None, obj=None):
        if isinstance(obj, QButtonGroup):
            # For logging feeding or washing
            for i in obj.buttons():
                if i.isChecked():
                    self.program_settings[key] = i.text()
        elif key == "Enabled":
            self.program_settings[key] = obj
        else:
            # For logging food quantity
            for idx, (tk, bt) in enumerate(zip(self.bgroup2_1.buttons(), self.bgroup2_2)):
                if idx != 0:
                    if tk.isChecked():
                        for i in bt.buttons():
                            if i.isChecked():
                                self.program_settings["Tanks"][int(tk.text().split()[1]) - 1] = i.text()
                    else:
                        self.program_settings["Tanks"][int(tk.text().split()[1]) - 1] = None

        self.update_json()

    def reset(self, preset):
        self.program_settings = copy(preset)
        for key, val in preset.items():
            if key == "Enabled":
                if isinstance(val, str):
                    val = eval(val)
                self.is_enabled_checkbox.setChecked(bool(val))
                # self.button_onoff.setChecked(val)
            elif key == "Type":
                if val == "Feeding and washing":
                    self.button_feeding.setChecked(True)
                    self.button_washing.setChecked(False)
                elif val == "Only washing":
                    self.button_feeding.setChecked(False)
                    self.button_washing.setChecked(True)
                self.record_log("Type", self.bgroup1_1)
            elif key == "Day":
                # Reset all checkboxes
                for bt in self.bgroup1_2.buttons():
                    bt.setChecked(False)
                # Turn on checkboxes
                if val:
                    if isinstance(val, str):
                        val = eval(val)
                    for v in val:
                        for bt in self.bgroup1_2.buttons():
                            if v in bt.text():
                                bt.setChecked(True)
                                break
            elif key == "Time":
                if val:
                    self.pd_time.setCurrentIndex(self.pd_time.findText(val))
                else:
                    self.pd_time.setCurrentIndex(0)
            elif "Tanks" in key:
                for idx, tank in enumerate(val):
                    tankid = idx + 1
                    if tank:
                        self.bgroup2_1.buttons()[tankid].setChecked(True)
                        bg = self.bgroup2_2[tankid]
                        for bt in bg.buttons():
                            if tank == bt.text():
                                bt.setChecked(True)
                                break
                    else:
                        self.bgroup2_1.buttons()[tankid].setChecked(True)
                        bg = self.bgroup2_2[tankid]
                        bg.setExclusive(False)
                        for bt in bg.buttons():
                            bt.setChecked(False)
                        bg.setExclusive(True)

    def duplicate(self):
        self.parent.addprogramtab()
        self.parent.tabs[-1].reset(self.program_settings)

    def delete_tab(self):
        # Scan for the current tab
        for id, tab in enumerate(self.parent.tabs):
            if tab.name == self.name:
                del self.parent.tabs[id]
                self.parent.removeTab(id)

                if os.path.isfile(self.json_path):
                    os.remove(self.json_path)
                else:  ## Show an error ##
                    print("Error: %s file not found" % self.json_path)

    def update_json(self):
        # Serializing json
        json_object = json.dumps(self.program_settings, indent=4)

        # Writing to sample.json
        with open(self.json_path, "w") as outfile:
            outfile.write(json_object)

    def progress_fn(self, log_str):
        self.parent.log_tab.infoTextBox.insertPlainText(log_str)

    def thread_complete(self):
        self.is_running = False
        self.button_startstop.setText("Start")
        self.button_startstop.setEnabled(True)
        self.parent.log_tab.program_name_label.setText(f"{self.name} is done")
        self.parent.status_bar.showMessage(f"{self.name} is done.")

    def start_program(self):
        if self.is_running:
            self.early_stop_signal.emit()
            self.is_running = False
        else:
            self.update_json()

            self.worker = Worker(
                run
            )  # Any other args, kwargs are passed to the run function

            self.worker.kwargs['food_amounts'] = self.program_settings["Tanks"]

            # worker.signals.result.connect(self.result_callback)
            self.early_stop_signal.connect(self.worker.set_early_stop)
            self.worker.signals.finished.connect(self.thread_complete)
            self.worker.signals.progress.connect(self.progress_fn)

            self.parent.log_tab.clear_activity()

            # Execute
            self.parent.threadpool.start(self.worker)

            self.is_running = True
            self.parent.log_tab.program_name_label.setText(f"{self.name} is running now")
            self.parent.status_bar.showMessage(f"{self.name} is running now...")
            self.button_startstop.setText("Stop")
            # self.button_startstop.setEnabled(False)
