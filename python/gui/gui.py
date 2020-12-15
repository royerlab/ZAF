import sys
from PyQt5.QtWidgets import QApplication

from python.gui.windows.mainwindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.processEvents()
    ctrl = MainWindow(app)
    sys.exit(app.exec_())
