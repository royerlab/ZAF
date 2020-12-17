import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
    QWidget, QHBoxLayout, QCheckBox)

import csv

from python.gui.widgets.tabs.program import ProgramTab


class DashboardTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.name = "Dashboard"

        self.layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignTop)

        # GroupBox1 (Left half)
        # Add_program button
        self.button_addtab = QPushButton("Add program", self)
        self.button_addtab.clicked.connect(lambda: parent.addprogramtab())

        gpbox1 = QGroupBox("Control Panel")
        # gpbox1.setMinimumSize(380, 420)  # (width, height)
        gpbox1_layout = QVBoxLayout()
        gpbox1.setLayout(gpbox1_layout)
        gpbox1_layout.addWidget(self.button_addtab)

        gpbox1_1 = QGroupBox("Save && Load")
        grid = QGridLayout()
        # grid.addWidget(QLabel("Save"), 1, 0)
        # grid.addWidget(QLabel("Load"), 2, 0)
        self.save_buttons = []
        self.load_buttons = []
        for i in range(5):
            grid.addWidget(QLabel(f"Preset {i + 1}"), 0, i)
            btn = QPushButton("Save")
            btn.setCheckable(True)
            # btn.setObjectName(f"SaveBtn{i}")
            btn.clicked.connect(lambda: self.save_pgm_tocsv())
            grid.addWidget(btn, 1, i)
            self.save_buttons.append(btn)
            btn = QPushButton("Load")
            btn.setCheckable(True)
            # btn.setObjectName(f"LoadBtn{i}")
            btn.clicked.connect(lambda: self.load_pgm_fromcsv())
            grid.addWidget(btn, 2, i)
            self.load_buttons.append(btn)
        gpbox1_1.setLayout(grid)
        gpbox1_layout.addWidget(gpbox1_1)

        # Emergency Stop
        self.button_emstop = QPushButton("Emergency\nStop", self)
        self.button_emstop.setStyleSheet("QPushButton {color: red; font: bold;}")
        self.button_emstop.clicked.connect(lambda: self.status_bar.setText("Emergency Stop!"))
        gpbox1_layout.addWidget(self.button_emstop)

        self.exit_button = QPushButton("Exit ZAF", self)
        self.exit_button.clicked.connect(lambda: self.parent.parent.app.quit())
        gpbox1_layout.addWidget(self.exit_button)

        # GroupBox2 (Right half)
        self.program_checkboxes_layout = QVBoxLayout()
        self.program_checkboxes_layout.setAlignment(Qt.AlignTop)
        self.right_layout.addWidget(QGroupBox("Programs"))

        self.programs_list = []
        self.program_checkboxes_list = []
        for tab in parent.tabs:
            if "Program" in tab.name:
                self.programs_list.append(tab.name)
                checkbox = QCheckBox(tab.name)
                checkbox.setChecked(tab.is_enabled_checkbox.isChecked())
                checkbox.stateChanged.connect(lambda: tab.is_enabled_checkbox.setChecked(checkbox.isChecked()))
                self.program_checkboxes_list.append(checkbox)
                self.program_checkboxes_layout.addWidget(checkbox)

        # Add to layout
        self.left_layout.addWidget(gpbox1)
        self.layout.addLayout(self.left_layout)
        self.right_layout.addLayout(self.program_checkboxes_layout)
        self.layout.addLayout(self.right_layout)
        self.setLayout(self.layout)

    def update_program_list(self):
        for i in reversed(range(self.program_checkboxes_layout.count())):
            self.program_checkboxes_layout.itemAt(i).widget().close()
            self.program_checkboxes_layout.takeAt(i)

        for tab in self.parent.tabs:
            if "Program" in tab.name:
                self.programs_list.append(tab.name)
                checkbox = QCheckBox(tab.name)
                checkbox.setChecked(tab.is_enabled_checkbox.isChecked())
                checkbox.stateChanged.connect(lambda: tab.is_enabled_checkbox.setChecked(checkbox.isChecked()))
                self.program_checkboxes_list.append(checkbox)
                self.program_checkboxes_layout.addWidget(checkbox)

        self.repaint()

    def save_pgm_tocsv(self):
        logdata = []
        for pg in self.parent.tabs:
            if isinstance(pg, ProgramTab):
                logdata.append(pg.program_settings)

        # Scan the checked button
        for id, bt in enumerate(self.save_buttons):
            if bt.isChecked():
                bt.setChecked(False)
                break

        filename = f"Preset{id + 1}"
        filepath = os.path.join("saved_files", filename + ".csv")
        with open(filepath, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=list(logdata[0].keys()))
            writer.writeheader()
            for data in logdata:
                writer.writerow(data)

        self.dialogbox.setText(f"Preset {id + 1} is saved.")
        self.statusBar.showMessage(f"Preset {id + 1} is saved.")
        self.repaint()

    def load_pgm_fromcsv(self):
        # Scan the checked button
        for id, bt in enumerate(self.load_buttons):
            if bt.isChecked():
                bt.setChecked(False)
                break

        filename = f"Preset{id + 1}"
        filepath = os.path.join("saved_files", filename + ".csv")
        data = []
        # try:
        with open(filepath, newline="") as file:
            reader = csv.DictReader(file)
            for i in reader:
                data.append(i)

        # Reconstruct program
        self.parent.reconstruct_program(data)

        self.dialogbox.setText(f"Preset {id + 1} is loaded.")
        self.statusBar.showMessage(f"Preset {id + 1} is loaded.")
        # except:
        #     self.dialogbox.setText(f"{filename} was not found.")

        self.repaint()


