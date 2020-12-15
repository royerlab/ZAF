from PyQt5.QtWidgets import (
    QMainWindow,
    QStatusBar)

from python.gui.widgets.tabmanager import TabManager


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setWindowTitle('ZAF+')
        self.setGeometry(0, 0, 640, 455)
        self.setFixedSize(640, 455)

        self.statusBar = QStatusBar()
        self.statusBar.showMessage("Welcome to ZAF+")
        self.setStatusBar(self.statusBar)

        self.tab_manager = TabManager(self, self.statusBar)
        self.setCentralWidget(self.tab_manager)

        self.show()
