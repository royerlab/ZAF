from copy import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QPushButton,
    QButtonGroup,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QGridLayout,
    QCheckBox,
    QComboBox,
    QScrollArea,
    QTabBar,
    QHBoxLayout, QRadioButton)
from PyQt5.QtCore import Qt


class ProgramTab(QTabBar):
    def __init__(self, parent):
        super().__init__()
        self.tab_name = "Program1"

        self.layout = QHBoxLayout()

        self.setMovable(True)
        self.parent = parent
        self.is_active = False
        self.num_tanks = 30
        self.num_quantity = ["1", "2", "3", "4"]
        self.program_log = {
            "Program": "ProgramTab",
            "Active": False,
            "Type": None,
            "Day": None,
            "Time": None,
        }
        for i in range(self.num_tanks):
            self.program_log.update({f"Tank {i + 1}": None})
        program_default = copy(self.program_log)

        # Layout left
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)

        # Create an ON/OFF button
        self.button_onoff = QPushButton("On / Off", self)
        self.button_onoff.setFixedSize(QtCore.QSize(100, 35))
        self.button_onoff.setCheckable(True)
        self.button_onoff.clicked.connect(lambda: self.set_isacive())
        self.button_reset = QPushButton("Reset", self)
        self.button_reset.setFixedSize(QtCore.QSize(100, 35))
        self.button_reset.clicked.connect(lambda: self.reset(program_default))
        self.button_reset.clicked.connect(lambda: self.tab.repaint())
        self.button_duplicate = QPushButton("Duplicate", self)
        self.button_duplicate.setFixedSize(QtCore.QSize(100, 35))
        self.button_duplicate.clicked.connect(lambda: self.duplicate())
        self.button_delete = QPushButton("Delete", self)
        self.button_delete.setFixedSize(QtCore.QSize(100, 35))
        self.button_delete.clicked.connect(lambda: self.remove_tab())

        self.first_button_row_layout = QHBoxLayout()
        self.first_button_row_layout.setAlignment(Qt.AlignLeft)
        self.first_button_row_layout.addWidget(self.button_onoff)
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
        self.button_feeding = QRadioButton("Feeding&Washing", self)
        self.button_feeding.setCheckable(True)
        self.button_washing = QRadioButton("Only Washing", self)
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


        # Create a button group for day of week =============================
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
            button.stateChanged.connect(lambda: self.get_active_day())
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
        self.pd_time.currentIndexChanged.connect(lambda: self.get_active_day())
        gpbox1_2_1_layout = QVBoxLayout()
        gpbox1_2_1_layout.addWidget(self.pd_time)
        gpbox1_2_1.setLayout(gpbox1_2_1_layout)
        self.left_layout.addWidget(gpbox1_2_1)


        # Group box right
        # Box for food quantity =================================================
        gpbox2 = QGroupBox("Food Quantity")
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
        for i in range(self.num_tanks):
            cb = QCheckBox(f'Tank {i + 1}', self)
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


    def set_isacive(self):
        self.is_active = self.button_onoff.isChecked()
        self.program_log["Active"] = self.button_onoff.isChecked()

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

    def get_active_day(self):
        checked_dow = [i.isChecked() for i in self.bgroup1_2.buttons()]
        dow = [self.button_dow[i][:3] for i, ii in enumerate(checked_dow) if ii and self.button_dow[i] != "Everyday"]
        time = self.pd_time.currentText()
        self.dialogbox.setText(" ".join(dow) + "  " + time)
        self.parent.tabs[0].update_active_pgm()
        self.program_log["Day"] = dow
        self.program_log["Time"] = time

    def record_log(self, key=None, obj=None):
        if isinstance(obj, QButtonGroup):
            # For logging feedin or washing
            for i in obj.buttons():
                if i.isChecked():
                    self.program_log[key] = i.text()
        else:
            # For logging food quantity
            for tk, bt in zip(self.bgroup2_1.buttons(), self.bgroup2_2):
                if tk.isChecked():
                    for i in bt.buttons():
                        if i.isChecked():
                            self.program_log[tk.text()] = i.text()
                else:
                    self.program_log[tk.text()] = None


    def reset(self, preset):
        self.program_log = copy(preset)
        for key, val in preset.items():
            if key == "Active":
                if isinstance(val, str):
                    val = eval(val)
                self.is_active = val
                self.button_onoff.setChecked(val)
            elif key == "Type":
                if val == "Feeding":
                    self.button_feeding.setChecked(True)
                    self.button_washing.setChecked(False)
                elif val == "Washing":
                    self.button_feeding.setChecked(False)
                    self.button_washing.setChecked(True)
                else:
                    self.bgroup1_1.setExclusive(False)
                    self.button_feeding.setChecked(False)
                    self.button_washing.setChecked(False)
                    self.bgroup1_1.setExclusive(True)
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
            elif "Tank" in key:
                tankid = int(key.split(' ')[-1]) - 1
                if val:
                    self.bgroup2_1.buttons()[tankid].setChecked(True)
                    bg = self.bgroup2_2[tankid]
                    for bt in bg.buttons():
                        if val == bt.text():
                            bt.setChecked(True)
                            break
                else:
                    self.bgroup2_1.buttons()[tankid].setChecked(True)
                    bg = self.bgroup2_2[tankid]
                    bg.setExclusive(False)
                    for bt in bg.buttons():
                        bt.setChecked(False)
                    bg.setExclusive(True)
        # self.tab.repaint()

    def duplicate(self):
        self.parent.addprogramtab()
        self.parent.tabs[-1].reset(self.program_log)


    def remove_tab(self):
        # Scan for the current tab
        for id, tab in enumerate(self.parent.tabs):
            if tab.objectName() == self.tab.objectName():
                del self.parent.tabs[id]
                self.parent.removeTab(id)

