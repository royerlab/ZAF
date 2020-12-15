import os
from PyQt5.QtWidgets import (
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
    QWidget)

import csv

from python.gui.widgets.tabs.protocoltab import ProgramTab


class DashboardTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.tab_name = "Dashboard"

        self.layout = QVBoxLayout()

        # GroupBox1 (Left half)
        # Add_program button
        self.button_addtab = QPushButton("Add program", self)
        self.button_addtab.clicked.connect(lambda : parent.addprogramtab())

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
        gpbox2 = QGroupBox()
        gpbox2_layout = QVBoxLayout()
        gpbox2.setLayout(gpbox2_layout)

        # Active program monitor
        gpbox2_1 = QGroupBox("Active programs")
        self.active_prg_list = []
        for tb in parent.tabs:
            if "Program" in tb.objectName():
                if tb.is_active:
                    self.active_prg_text.append(tb.objectName())

        self.active_prg_text = QLabel("\n".join(self.active_prg_list) if self.active_prg_list else "None")
        self.active_prg_text.setWordWrap(True)
        gpbox2_1_layout = QVBoxLayout()
        gpbox2_1.setLayout(gpbox2_1_layout)
        gpbox2_1_layout.addWidget(self.active_prg_text)
        gpbox2_layout.addWidget(gpbox2_1)

        # Add to layout
        self.layout.addWidget(gpbox1)
        self.layout.addWidget(gpbox2)
        self.setLayout(self.layout)

    def update_active_pgm(self):
        self.active_prg_list = []
        for i, tb in enumerate(self.parent.active_tabs):
            if list(tb.values())[0]:
                for tab in self.parent.tabs:
                    if list(tb.keys())[0] == tab.objectName():
                        time = tab.dialogbox.text()
                        self.active_prg_list.append(f"Program {i + 1}:   " + time)
        self.active_prg_text.setText(
            "\n".join(self.active_prg_list) if self.active_prg_list else "None"
        )

    def save_pgm_tocsv(self):
        logdata = []
        for pg in self.parent.tabs:
            if isinstance(pg, ProgramTab):
                logdata.append(pg.program_log)

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


