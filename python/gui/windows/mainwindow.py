from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar)

from python.gui.widgets.tabmanager import TabManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ZAF 2.0')
        self.setGeometry(0, 0, 800, 480)
        self.setFixedSize(800, 480)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.content = TabManager(self.statusBar)
        self.setCentralWidget(self.content)

        self.show()
