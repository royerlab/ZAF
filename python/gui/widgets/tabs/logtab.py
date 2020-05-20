from copy import copy
from PyQt5.QtWidgets import (
    QPushButton,
    QButtonGroup,
    QTabWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QGridLayout,
    QCheckBox,
    QComboBox,
    QScrollArea,
    QTabBar,
)
from PyQt5.QtCore import Qt


class LogTab(QTabBar):
    def __init__(self, parent, tab):
        super().__init__()
        self.tab = tab
        self.button = QPushButton(self)
        self.cb = QCheckBox(self)
        self.button.clicked.connect(lambda: self.checkcb())


        self.tab.layout.addWidget(self.button)
        self.tab.layout.addWidget(self.cb)

        self.tab.setLayout(self.tab.layout)

    def checkcb(self):
        if self.cb.isChecked():
            self.cb.setChecked(False)
        else:
            self.cb.setChecked(True)
        self.tab.repaint()

