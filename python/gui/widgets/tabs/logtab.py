import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QTextEdit,
    QWidget,
    QHBoxLayout
)
from PyQt5.QtCore import Qt


class LogTab(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.name = "Log"

        self.layout = QVBoxLayout()

        # Add information
        self.infoTextBox = QTextEdit()
        self.infoTextBox.verticalScrollBar().rangeChanged.connect(
            lambda min, max: self.infoTextBox.verticalScrollBar().setSliderPosition(max)
        )
        # Log.gui_print = self.activity_print
        self.infoTextBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.infoTextBox.setLineWrapMode(QTextEdit.NoWrap)

        # Add text copy button
        self.info_layout = QHBoxLayout()
        self.info_layout.addWidget(self.infoTextBox, 1)
        self.info_layout.setAlignment(Qt.AlignTop)
        self.layout.addLayout(self.info_layout)

        self.setLayout(self.layout)

        stdout = OutputWrapper(self, True)
        stdout.outputWritten.connect(self.activity_print)
        stderr = OutputWrapper(self, False)
        stderr.outputWritten.connect(self.activity_print)

    def activity_print(self, string2print, stdout):
        self.infoTextBox.insertPlainText(string2print)
        self.repaint()

    def clear_activity(self):
        self.infoTextBox.clear()


class OutputWrapper(QtCore.QObject):
    outputWritten = QtCore.pyqtSignal(object, object)

    def __init__(self, parent, stdout=True):
        QtCore.QObject.__init__(self, parent)
        if stdout:
            self._stream = sys.stdout
            sys.stdout = self
        else:
            self._stream = sys.stderr
            sys.stderr = self
        self._stdout = stdout

    def write(self, text):
        self._stream.write(text)
        self.outputWritten.emit(text, self._stdout)

    def __getattr__(self, name):
        return getattr(self._stream, name)

    def __del__(self):
        try:
            if self._stdout:
                sys.stdout = self._stream
            else:
                sys.stderr = self._stream
        except AttributeError:
            pass
