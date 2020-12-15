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

    def activity_print(self, string2print):
        self.infoTextBox.insertPlainText(string2print)

    def clear_activity(self):
        self.infoTextBox.clear()

