from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class ReminderWidget(QWidget):
    def __init__(self, message, font_height, parent=None):
        super(ReminderWidget, self).__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(message)
        label.setStyleSheet("background-color: #F5F5F5; border-radius: 5px; color: black;")
        label.setFont(QFont("Arial", font_height))
        label.setMinimumHeight(30)
        layout.addWidget(label)
