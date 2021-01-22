from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QGroupBox,
    QWidget, QHBoxLayout, QCheckBox
)


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

        # # Emergency Stop
        # self.button_emstop = QPushButton("Emergency\nStop", self)
        # self.button_emstop.setStyleSheet("QPushButton {color: red; font: bold;}")
        # self.button_emstop.clicked.connect(lambda: self.status_bar.setText("Emergency Stop!"))
        # gpbox1_layout.addWidget(self.button_emstop)

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
                checkbox.stateChanged.connect(tab.toggle_program_enabled)

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
                checkbox.stateChanged.connect(tab.toggle_program_enabled)
                # checkbox.stateChanged.connect(lambda: tab.is_enabled_checkbox.setChecked(checkbox.isChecked()))
                self.program_checkboxes_list.append(checkbox)
                self.program_checkboxes_layout.addWidget(checkbox)

        self.repaint()
