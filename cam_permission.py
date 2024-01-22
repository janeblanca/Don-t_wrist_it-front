from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont


class CamPermission(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Camera Access Permission')
        self.setStyleSheet("background-color: #F6F5F5;")
        self.setText('Allow Don’t Wrist It! to access your camera?')

        self.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        self.button(QMessageBox.Yes).setText('Allow')
        self.button(QMessageBox.No).setText("Don't Allow")

        # Font size of window title
        title_font = QFont()
        title_font.setPointSize(8)
        self.setFont(title_font)

        # Font size of Message Box text
        text_font = QFont()
        text_font.setPointSize(10)
        self.setFont(text_font)

        # Font size of Buttons
        button_font = QFont()
        button_font.setPointSize(9)
        self.button(QMessageBox.Yes).setFont(button_font)
        self.button(QMessageBox.No).setFont(button_font)